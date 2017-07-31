from . import BasePackerObject, TemplateVar
import validator


class PackerPostProcessor(BasePackerObject):

    def __init__(self, title=None, **kwargs):
        super(PackerPostProcessor, self).__init__(title, **kwargs)


class Checksum(PackerPostProcessor):
    """
    Checksum Post-Processor
    https://www.packer.io/docs/post-processors/checksum.html
    """
    resource_type = "checksum"

    # Checksum Post Processor constants
    MD5 = "md5"
    SHA1 = "sha1"
    SHA224 = "sha224"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"

    # Checksum Template Variables
    BuildName = TemplateVar("BuildName")
    BuilderType = TemplateVar("BuilderType")
    ChecksumType = TemplateVar("ChecksumType")

    props = {
        'checksum_types': ([basestring], False),
        'output': (basestring, False),
    }

    def validate(self):
        valid_checksum_types = [Checksum.MD5, Checksum.SHA1, Checksum.SHA224,
                                Checksum.SHA256, Checksum.SHA384, Checksum.SHA512]
        checksum_types = self.properties.get('checksum_types', [])
        if len([x for x in checksum_types if x not in valid_checksum_types]) > 0:
            raise ValueError('%s: only one of the following can be specified: %s' % (
                                 self.__class__.__name__, ', '.join(valid_checksum_types)))


class DockerImport(PackerPostProcessor):
    """
    Docker Import Post-Processor
    https://www.packer.io/docs/post-processors/docker-import.html
    """
    resource_type = "docker-import"

    props = {
        'repository': (basestring, True),
        'tag': (basestring, False),
    }


class DockerPush(PackerPostProcessor):
    """
    Docker Push Post-Processor
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


class DockerSave(PackerPostProcessor):
    """
    Docker Save Post-Processor
    https://www.packer.io/docs/post-processors/docker-save.html
    """
    resource_type = "docker-save"

    props = {
        'path': (basestring, True),
    }


class DockerTag(PackerPostProcessor):
    """
    Docker Tag Post-Processor
    https://www.packer.io/docs/post-processors/docker-tag.html
    """
    resource_type = "docker-tag"

    props = {
        'repository': (basestring, True),
        'tag': (basestring, False),
        'force': (basestring, False),
    }


class GoogleComputeExport(PackerPostProcessor):
    """
    Google Compute Image Exporter Post-Processor
    https://www.packer.io/docs/post-processors/googlecompute-export.html
    """
    resource_type = "googlecompute-export"

    props = {
        'paths': ([basestring], True),
        'keep_input_artifact': (validator.boolean, False),
    }


class Manifest(PackerPostProcessor):
    """
    Manifest Post-Processor
    https://www.packer.io/docs/post-processors/manifest.html
    """
    resource_type = "manifest"

    props = {
        'output': (basestring, False),
        'strip_path': (validator.boolean, False),
    }
