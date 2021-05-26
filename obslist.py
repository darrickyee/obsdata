from core import ObsMixin


class ObsList(ObsMixin, list):

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
