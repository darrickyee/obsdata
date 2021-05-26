from core import ObsMixin


class ObsSet(ObsMixin, set):

    _mutators = ('__iand__',
                 '__ior__',
                 '__isub__',
                 '__ixor__',
                 'add',
                 'clear',
                 'difference_update',
                 'discard',
                 'intersection_update',
                 'pop',
                 'remove',
                 'symmetric_difference_update',
                 'update')

    def values(self):
        return self
