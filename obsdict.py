from core import ObsMixin


class ObsDict(ObsMixin, dict):

    _mutators = ('__delitem__',
                 '__ior__',
                 '__setitem__',
                 'clear',
                 'pop',
                 'popitem',
                 'setdefault',
                 'update')
