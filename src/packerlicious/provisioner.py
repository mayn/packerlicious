from . import BasePackerObject, EnvVar, TemplateVar
import validator


class PackerProvisioner(BasePackerObject):

    def __init__(self, title=None, **kwargs):
        super(PackerProvisioner, self).__init__(title, **kwargs)


def valid_file_direction(x):
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
        'direction': (valid_file_direction, True),
    }

    # File Provisioner constants
    Upload = "upload"
    Download = "download"


class Shell(PackerProvisioner):
    """
    Shell Provisioner
    https://www.packer.io/docs/provisioners/shell.html
    """
    resource_type = "shell"

    # Shell Local Template Variables
    Path = TemplateVar("Path")
    Vars = TemplateVar("Vars")

    # Shell Local Environment Variables
    PackerBuildName = EnvVar("PACKER_BUILD_NAME")
    PackerBuilderType = EnvVar("PACKER_BUILDER_TYPE")
    PackerHttpAddr = EnvVar("PACKER_HTTP_ADDR")

    props = {
        'inline': ([basestring], True),
        'script': (basestring, True),
        'scripts': ([basestring], True),
        'binary': (validator.boolean, False),
        'environment_vars': ([basestring], False),
        'execute_command': (basestring, False),
        'expect_disconnect': (validator.boolean, False),
        'inline_shebang': (basestring, False),
        'remote_folder': (basestring, False),
        'remote_file': (basestring, False),
        'remote_path': (basestring, False),
        'skip_clean': (validator.boolean, False),
        'start_retry_timeout': (basestring, False),
    }

    def validate(self):
        conds = [
            'inline',
            'script',
            'scripts',
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)


class ShellLocal(PackerProvisioner):
    """
    Shell Local Provisioner
    https://www.packer.io/docs/provisioners/shell-local.html
    """
    resource_type = "shell-local"

    # Shell Local Template Variables
    Command = TemplateVar("Command")

    props = {
        'command': (basestring, True),
        'execute_command': ([basestring], False),
    }
