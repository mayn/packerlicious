from .. import BasePackerObject


class PackerBuilder(BasePackerObject):

    def __init__(self, title=None, **kwargs):
        super(PackerBuilder, self).__init__(title, **kwargs)
