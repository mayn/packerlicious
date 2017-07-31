from . import BasePackerObject
import validator


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


class DockerPush(PackerPostProcessor):
    """
    Docker Push Processor
    https://www.packer.io/docs/post-processors/docker-push.html
    """
    resource_type = "docker-push"

    props = {
        'aws_access_key': (basestring, False),
        'aws_secret_key': (basestring, False),
        'aws_token': (basestring, False),
        'ecr_login': (validator.boolean, False),
        'login': (validator.boolean, False),
        'login_email': (basestring, False),
        'login_username': (basestring, False),
        'login_password': (basestring, False),
        'login_server': (basestring, False),
    }
