from . import BasePackerObject


class PackerProvisioner(BasePackerObject):

    def __init__(self, title=None, **kwargs):
        super(PackerProvisioner, self).__init__(title, **kwargs)


def direction(x):
    if x not in [File.Upload, File.Download]:
        raise ValueError(x)
    return x


class File(PackerProvisioner):
    """
    File Provisioner
    https://www.packer.io/docs/provisioners/file.html
    """
    resource_type = "file"

    props = {
        'source': (basestring, True),
        'destination': (basestring, True),
        'direction': (direction, True),
    }

    # File Provisioner constants
    Upload = "upload"
    Download = "download"
