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

from . import BasePackerObject, EnvVar, PackerProperty, TemplateVar, validator


class PackerPostProcessorChain(BasePackerObject):
    """
    TODO define what a chain is, see https://www.packer.io/docs/post-processors/artifice.html#configuration
    for example
    """


class PackerPostProcessor(BasePackerObject):

    def __init__(self, title=None, **kwargs):
        super(PackerPostProcessor, self).__init__(title, **kwargs)


class AliCloudImport(PackerPostProcessor):
    """
    Alibaba Cloud Import Post-Processor
    https://www.packer.io/docs/post-processors/alicloud-import.html
    TODO add image_name, image_description, image_system_size format validation.
    """
    resource_type = "alicloud-import"

    props = {
        'access_key': (str, True),
        'secret_key': (str, True),
        'region': (str, True),
        'image_name': (str, True),
        'oss_bucket_name': (str, True),
        'image_os_type': ([str], True),
        'image_platform': (str, True),
        'image_architecture': ([str], True),
        'format': (str, True),
        'oss_key_name': (str, False),
        'skip_clean': (validator.boolean, False),
        'image_description': (str, False),
        'image_force_delete': (validator.boolean, False),
        'image_system_size': (str, False),
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
        'access_key': (str, False),
        'region': (str, True),
        's3_bucket_name': (str, True),
        'secret_key': (str, False),
        'ami_description': (str, False),
        'ami_groups': ([str], False),
        'ami_name': (str, False),
        'ami_users': ([str], False),
        'custom_endpoint_ec2': (str, False),
        'license_type': (validator.string_list_item([LicenseAWS, LicenseBYOL]), False),
        'mfa_code': (str, False),
        'profile': (str, False),
        'role_name': (str, False),
        's3_key_name': (str, False),
        'skip_clean': (validator.boolean, False),
        'skip_region_validation': (validator.boolean, False),
        'tags': (dict, False),
        'token': (str, False),
    }

    def validate(self):
        conds = [
            'access_key',
            'secret_key',
        ]
        validator.all_or_nothing(self.__class__.__name__, self.properties, conds)


class Artifice(PackerPostProcessor):
    """
    Artifice Post-Processor
    https://www.packer.io/docs/post-processors/artifice.html
    """
    resource_type = "artifice"

    props = {
        'files': ([str], True),
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
        'artifact': (str, True),
        'artifact_type': (str, True),
        'token': (str, False),
        'atlas_url': (str, False),
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
        'checksum_types': ([str], False),
        'output': (str, False),
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
        'output': (str, False),
        'format': (str, False),
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
        'repository': (str, True),
        'tag': (str, False),
    }


class DockerPush(PackerPostProcessor):
    """
    Docker Push Post-Processor
    https://www.packer.io/docs/post-processors/docker-push.html
    """
    resource_type = "docker-push"

    props = {
        'aws_access_key': (str, False),
        'aws_secret_key': (str, False),
        'aws_profile': (str, False),
        'aws_token': (str, False),
        'ecr_login': (validator.boolean, False),
        'login': (validator.boolean, False),
        'login_username': (str, False),
        'login_password': (str, False),
        'login_server': (str, False),
    }


class DockerSave(PackerPostProcessor):
    """
    Docker Save Post-Processor
    https://www.packer.io/docs/post-processors/docker-save.html
    """
    resource_type = "docker-save"

    props = {
        'path': (str, True),
    }


class DockerTag(PackerPostProcessor):
    """
    Docker Tag Post-Processor
    https://www.packer.io/docs/post-processors/docker-tag.html
    """
    resource_type = "docker-tag"

    props = {
        'repository': (str, True),
        'tag': (str, False),
        'force': (str, False),
    }


class GoogleComputeImport(PackerPostProcessor):
    """
    Google Compute Image Import Post-Processor
    https://www.packer.io/docs/post-processors/googlecompute-import.html
    """
    resource_type = "googlecompute-import"

    props = {
        'account_file': (str, True),
        'bucket': (str, True),
        'image_name': (str, True),
        'project_id': (str, True),
        'gcs_object_name': (str, False),
        'image_description': (str, False),
        'image_family': (str, False),
        'image_labels': (dict, False),
        'keep_input_artifact': (validator.boolean, False),
        'skip_clean': (validator.boolean, False),
    }


class GoogleComputeExport(PackerPostProcessor):
    """
    Google Compute Image Exporter Post-Processor
    https://www.packer.io/docs/post-processors/googlecompute-export.html
    """
    resource_type = "googlecompute-export"

    props = {
        'paths': ([str], True),
        'keep_input_artifact': (validator.boolean, False),
    }


class Manifest(PackerPostProcessor):
    """
    Manifest Post-Processor
    https://www.packer.io/docs/post-processors/manifest.html
    """
    resource_type = "manifest"

    props = {
        'output': (str, False),
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
        'command': (str, False),
        'inline': ([str], False),
        'script': (str, False),
        'scripts': ([str], False),
        'environment_vars': ([str], False),
        'execute_command': ([str], False),
        'inline_shebang': (str, False),
        'use_linux_pathing': (validator.boolean, False),
    }

    def validate(self):
        conds = [
            'command',
            'inline',
            'script',
            'scripts',
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)


class VagrantProviderOverride(PackerProperty):
    props = {
        'compression_level': (validator.integer_range(0, 9), False),
        'include': ([str], False),
        'keep_input_artifact': (validator.boolean, False),
        'output': (str, False),
        'vagrantfile_template': (str, False),
    }


class VagrantOverrides(PackerProperty):
    props = {
        'aws': (VagrantProviderOverride, False),
        'digitalocean': (VagrantProviderOverride, False),
        'google': (VagrantProviderOverride, False),
        'hyperv': (VagrantProviderOverride, False),
        'libvirt': (VagrantProviderOverride, False),
        'lxc': (VagrantProviderOverride, False),
        'parallels': (VagrantProviderOverride, False),
        'scaleway': (VagrantProviderOverride, False),
        'virtualbox': (VagrantProviderOverride, False),
        'vmware': (VagrantProviderOverride, False),
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
        'include': ([str], False),
        'keep_input_artifact': (validator.boolean, False),
        'output': (str, False),
        'vagrantfile_template': (str, False),
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
        'access_token': (str, True),
        'box_tag': (str, True),
        'version': (str, True),
        'no_release': (str, False),
        'vagrant_cloud_url': (str, False),
        'version_description': (str, False),
        'box_download_url': (str, False),
    }


class VSphere(PackerPostProcessor):
    """
    vSphere Post-Processor
    https://www.packer.io/docs/post-processors/vsphere.html
    """

    resource_type = "vsphere"

    props = {
        'cluster': (str, True),
        'datacenter': (str, True),
        'host': (str, True),
        'password': (str, True),
        'username': (str, True),
        'vm_name': (str, True),
        'datastore': (str, False),
        'disk_mode': (str, False),
        'insecure': (validator.boolean, False),
        'resource_pool': (str, False),
        'vm_folder': (str, False),
        'vm_network': (str, False),
        'overwrite': (validator.boolean, False),
        'options': ([str], False),
    }


class VSphereTemplate(PackerPostProcessor):
    """
    vSphere Template Post-Processor
    https://www.packer.io/docs/post-processors/vsphere-template.html
    """

    resource_type = "vsphere-template"

    props = {
        'host': (str, True),
        'password': (str, True),
        'username': (str, True),
        'datacenter': (str, False),
        'folder': (str, False),
        'insecure': (validator.boolean, False),
    }
