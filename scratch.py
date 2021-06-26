# %%
from dataclasses import dataclass
from core import ObsMixin, observe_path
from obsdict import ObsDict

# %%

od = ObsDict(player=ObsDict(location='Home'), visits=0)


def report_loc(loc: str):
    print(f'Location changed to {loc}')

# %%


def inc_visit(loc: str):
    if loc == 'Home':
        od['visits'] += 1
# %%


# %%


class Notifier:

    def __init__(self, value=None) -> None:
        self._name = ''
        self._value = value

    def __set_name__(self, owner, name: str):
        self._name = '_' + name
        setattr(owner, self._name, self._value)

    def __get__(self, obj, objtype=None):
        return getattr(obj, self._name)

    def __set__(self, obj: ObsMixin, value):
        setattr(obj, self._name, value)
        if hasattr(obj, '_notify') and callable(obj._notify):
            obj._notify()


# %%

def _obs_property(name: str):

    def _fget(obj):
        try:
            return obj._obsdict[name]
        except KeyError:
            return getattr(obj, name)

    def _fset(obj, value):
        obj._obsdict[name] = value

    return property(_fget, _fset)


class ObsModel:

    def __init__(self) -> None:
        self._obsdict = ObsDict()
        self.subscribe = self._obsdict.subscribe
        self.pipe = self._obsdict.pipe

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({", ".join(f"{k}={v}" for k, v in self._obsdict.items())})'


def make_model(cls_name: str, **fields):
    init_params = ', '.join(f'{k}={v}' for k, v in fields.items())
    return f"""
    def __init__(self, {init_params}):
        super().__init__()
        self._obsdict.update({fields})
    """
