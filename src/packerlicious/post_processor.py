"""
Copyright 2017 Matthew Aynalem

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from . import BasePackerObject, EnvVar, PackerProperty, TemplateVar
import validator


class PackerPostProcessorChain(BasePackerObject):
    """
    TODO define what a chain is, see https://www.packer.io/docs/post-processors/artifice.html#configuration
    for example
    """


class PackerPostProcessor(BasePackerObject):

    def __init__(self, title=None, **kwargs):
        super(PackerPostProcessor, self).__init__(title, **kwargs)


class AlicloudImport(PackerPostProcessor):
    """
    Alicloud Import Post-Processor
    https://www.packer.io/docs/post-processors/alicloud-import.html
    TODO add image_name, image_description, image_system_size format validation.
    """
    resource_type = "alicloud-import"

    props = {
        'access_key': (basestring, True),
        'secret_key': (basestring, True),
        'region': (basestring, True),
        'image_name': (basestring, True),
        'oss_bucket_name': (basestring, True),
        'image_os_type': ([basestring], True),
        'image_platform': (basestring, True),
        'image_architecture': ([basestring], True),
        'format': (basestring, True),
        'oss_key_name': (basestring, False),
        'skip_clean': (validator.boolean, False),
        'image_description': (basestring, False),
        'image_force_delete': (validator.boolean, False),
        'image_system_size': (basestring, False),
    }


class AmazonImport(PackerPostProcessor):
    """
    Amazon Import Post-Processor
    https://www.packer.io/docs/post-processors/amazon-import.html
    """
    resource_type = "amazon-import"

    # TODO implement enum
    LicenseAWS = "AWS"
    LicenseBYOL = "BYOL"

    props = {
        'access_key': (basestring, True),
        'region': (basestring, True),
        's3_bucket_name': (basestring, True),
        'secret_key': (basestring, True),
        'ami_description': (basestring, False),
        'ami_groups': ([basestring], False),
        'ami_name': (basestring, False),
        'ami_users': ([basestring], False),
        'license_type': (validator.string_list_item([LicenseAWS, LicenseBYOL]), False),
        'mfa_code': (basestring, False),
        'skip_clean': (validator.boolean, False),
        'tags': (dict, False),
        'token': (basestring, False),
    }


class Artifice(PackerPostProcessor):
    """
    Artifice Post-Processor
    https://www.packer.io/docs/post-processors/artifice.html
    """
    resource_type = "artifice"

    props = {
        'files': ([basestring], True),
    }


class Atlas(PackerPostProcessor):
    """
    Atlas Post-Processor
    https://www.packer.io/docs/post-processors/atlas.html
    """
    resource_type = "atlas"

    # Checksum Environment Variables
    AtlasCaFile = EnvVar("ATLAS_CAFILE")
    AtlasCaPath = EnvVar("ATLAS_CAPATH")

    props = {
        'artifact': (basestring, True),
        'artifact_type': (basestring, True),
        'token': (basestring, False),
        'atlas_url': (basestring, False),
        'metadata': (dict, False),
    }


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


class Compress(PackerPostProcessor):
    """
    Compress Post-Processor
    https://www.packer.io/docs/post-processors/compress.html
    """
    resource_type = "compress"

    # Checksum Template Variables
    BuildName = TemplateVar("BuildName")
    BuilderType = TemplateVar("BuilderType")

    props = {
        'output': (basestring, False),
        'format': (basestring, False),
        'compression_level': (validator.integer_range(-1, 9), False),
        'keep_input_artifact': (validator.boolean, False),
    }


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


class ShellLocal(PackerPostProcessor):
    """
    Shell Local Post-Processor
    https://www.packer.io/docs/post-processors/shell-local.html
    """
    resource_type = "shell-local"

    # Shell Local Template Variables
    Vars = TemplateVar("Vars")
    Script = TemplateVar("Script")

    # Shell Local Environment Variables
    PackerBuildName = EnvVar("PACKER_BUILD_NAME")
    PackerBuildType = EnvVar("PACKER_BUILD_TYPE")

    props = {
        'inline': ([basestring], False),
        'script': (basestring, False),
        'scripts': ([basestring], False),
        'environment_vars': ([basestring], False),
        'execute_command': (basestring, False),
        'inline_shebang': (basestring, False),
    }

    def validate(self):
        conds = [
            'inline',
            'script',
            'scripts',
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)


class VagrantProviderOverride(PackerProperty):
    props = {
        'compression_level': (validator.integer_range(0, 9), False),
        'include': ([basestring], False),
        'keep_input_artifact': (validator.boolean, False),
        'output': (basestring, False),
        'vagrantfile_template': (basestring, False),
    }


class VagrantOverrides(PackerProperty):
    props = {
        'aws': (VagrantProviderOverride, False),
        'digitalocean': (VagrantProviderOverride, False),
        'virtualbox': (VagrantProviderOverride, False),
        'vmware': (VagrantProviderOverride, False),
        'parallels': (VagrantProviderOverride, False),
    }


class Vagrant(PackerPostProcessor):
    """
    Vagrant Post-Processor
    https://www.packer.io/docs/post-processors/vagrant.html
    """
    resource_type = "vagrant"

    # Shell Local Template Variables
    ArtifactId = TemplateVar("ArtifactId")
    BuildName = TemplateVar("BuildName")
    Provider = TemplateVar("Provider")

    props = {
        'compression_level': (validator.integer_range(0, 9), False),
        'include': ([basestring], False),
        'keep_input_artifact': (validator.boolean, False),
        'output': (basestring, False),
        'vagrantfile_template': (basestring, False),
        'override': (VagrantOverrides, False),
    }


class VagrantCloud(PackerPostProcessor):
    """
    Vagrant Post-Processor
    https://www.packer.io/docs/post-processors/vagrant-cloud.html

    # TODO add support for doubly-nested array.
    see https://www.packer.io/docs/post-processors/vagrant-cloud.html#use-with-vagrant-post-processor
    # TODO semantic versioning validator for version attr
    """

    resource_type = "vagrant-cloud"

    props = {
        'access_token': (basestring, True),
        'box_tag': (basestring, True),
        'version': (basestring, True),
        'no_release': (basestring, False),
        'vagrant_cloud_url': (basestring, False),
        'version_description': (basestring, False),
        'box_download_url': (basestring, False),
    }


class VSphere(PackerPostProcessor):
    """
    vSphere Post-Processor
    https://www.packer.io/docs/post-processors/vsphere.html
    """

    resource_type = "vsphere"

    props = {
        'cluster': (basestring, True),
        'datacenter': (basestring, True),
        'host': (basestring, True),
        'password': (basestring, True),
        'username': (basestring, True),
        'vm_name': (basestring, True),
        'datastore': (basestring, False),
        'disk_mode': (basestring, False),
        'insecure': (validator.boolean, False),
        'resource_pool': (basestring, False),
        'vm_folder': (basestring, False),
        'vm_network': (basestring, False),
        'overwrite': (validator.boolean, False),
        'options': ([basestring], False),
    }

