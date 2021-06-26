from core import ObsMixin


class ObsList(ObsMixin, list):
    """Observable `list` class.

    See `help(list)` for initialization signatures.
    """

    _mutators = ('__delitem__',
                 '__iadd__',
                 '__imul__',
                 '__setitem__',
                 'append',
                 'clear',
                 'extend',
                 'insert',
                 'pop',
                 'remove',
                 'sort')

    def values(self):
        return self
