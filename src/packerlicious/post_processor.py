from . import BasePackerObject


class PackerPostProcessor(BasePackerObject):

    def __init__(self, title=None, **kwargs):
        super(PackerPostProcessor, self).__init__(title, **kwargs)


class DockerImport(PackerPostProcessor):
    """
    Docker Import Processor
    https://www.packer.io/docs/post-processors/docker-import.html
    """
    resource_type = "docker-import"

    props = {
        'repository': (basestring, True),
        'tag': (basestring, False),
    }
