from functools import wraps
from typing import Callable, Union, cast
from rx.core.typing import Disposable
from rx.subject.subject import Subject


def _mutator(fn: Callable):

    @wraps(fn)
    def _fn(obj: 'ObsMixin', *args, **kwargs):
        old_obj = obj.copy()

        value = fn(obj, *args, **kwargs)

        obj._notify()

        if obj != old_obj:

            for disposer in obj._disposers:
                disposer.dispose()

            obj._disposers = [value.subscribe(lambda _: obj._notify())
                              for value in obj._get_values()
                              if isinstance(value, ObsMixin)]

        return value

    return _fn


class ObsMixin:

    _mutators: tuple[str] = tuple()

    def __new__(cls, *args, **kwargs):
        for method_name in cls._mutators:
            setattr(cls, method_name, _mutator(getattr(super(), method_name)))

        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._subject = Subject()
        self.subscribe = self._subject.subscribe
        self.pipe = self._subject.pipe

        self._disposers: list[Disposable] = list()

    def _get_values(self):
        return list()

    def _notify(self):
        self._subject.on_next(self)

    def copy(self):
        return type(self)(cast(Union[dict, list, set], super()).copy())

    def __repr__(self) -> str:
        # set in CPython is hardcoded to print the class name if class isn't
        # exactly a set
        if isinstance(self, set):
            return super().__repr__()

        return f'{self.__class__.__name__}({super().__repr__()})'
