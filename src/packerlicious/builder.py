import warnings

from . import BasePackerObject, TemplateVar
import validator


class PackerBuilder(BasePackerObject):

    def __init__(self, title=None, **kwargs):
        super(PackerBuilder, self).__init__(title, **kwargs)


class Docker(PackerBuilder):
    """
    Docker Builder
    https://www.packer.io/docs/builders/docker.html
    """
    resource_type = "docker"

    """
    Docker Template Variables
    see https://www.packer.io/docs/builders/docker.html#run_command
    """
    Image = TemplateVar("Image")

    props = {
        'commit': (validator.boolean, False),
        'discard': (validator.boolean, False),
        'export_path': (basestring, False),
        'image': (basestring, True),
        'author': (basestring, False),
        'aws_access_key': (basestring, False),
        'aws_secret_key': (basestring, False),
        'aws_token': (basestring, False),
        'changes': ([basestring], False),
        'ecr_login': (validator.boolean, False),
        'login': (validator.boolean, False),
        'login_email': (basestring, False),
        'login_username': (basestring, False),
        'login_password': (basestring, False),
        'login_server': (basestring, False),
        'message': (basestring, False),
        'privileged': (validator.boolean, False),
        'pull': (validator.boolean, False),
        'run_command': (basestring, False),
        'volumes': (dict, False),
    }

    def validate(self):
        conds = [
            'commit',
            'discard',
            'export_path',
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)


class File(PackerBuilder):
    """
    File Builder
    https://www.packer.io/docs/builders/file.html
    """
    resource_type = "file"

    props = {
        'target': (basestring, True),
        'source': (basestring, False),
        'content': (basestring, False),
    }

    def validate(self):

        conds = [
            'source',
            'content',
        ]
        specified_count = validator.mutually_exclusive(self.__class__.__name__, self.properties, conds)
        if specified_count == 0:
            warnings.warn("Both source and content not specified, artifact will be empty.")
