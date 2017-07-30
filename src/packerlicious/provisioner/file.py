from . import PackerProvisioner
# File Provisioner constants
Upload = "upload"
Download = "download"


def direction(x):
    if x not in [Upload, Download]:
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
