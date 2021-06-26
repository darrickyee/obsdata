from core import ObsMixin


class ObsDict(ObsMixin, dict):
    """Observable `dict` class.

    See `help(dict)` for initialization signatures.
    """

    _mutators = ('__delitem__',
                 '__ior__',
                 '__setitem__',
                 'clear',
                 'pop',
                 'popitem',
                 'setdefault',
                 'update')
