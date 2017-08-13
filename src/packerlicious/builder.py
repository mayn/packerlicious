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
import warnings

from . import BasePackerObject, PackerProperty, TemplateVar
import validator


class PackerCommunicator(BasePackerObject):
    """
    packer communicator
    https://www.packer.io/docs/templates/communicator.html
    TODO attribute validation
    """
    communicator_props = {
        'communicator': (basestring, False),
        # ssh communicator props
        'ssh_bastion_agent_auth': (validator.boolean, False),
        'ssh_bastion_host': (basestring, False),
        'ssh_bastion_password': (basestring, False),
        'ssh_bastion_port': (validator.integer, False),
        'ssh_bastion_private_key_file': (basestring, False),
        'ssh_bastion_username': (basestring, False),
        'ssh_disable_agent': (validator.boolean, False),
        'ssh_file_transfer_method': (basestring, False),
        'ssh_handshake_attempts': (validator.integer, False),
        'ssh_host': (basestring, False),
        'ssh_password': (basestring, False),
        'ssh_port': (validator.integer, False),
        'ssh_private_key_file': (basestring, False),
        'ssh_pty': (validator.boolean, False),
        'ssh_timeout': (basestring, False),
        'ssh_username': (basestring, False),
        # WinRM communicator props
        'winrm_host': (basestring, False),
        'winrm_port': (validator.integer, False),
        'winrm_username': (basestring, False),
        'winrm_password': (basestring, False),
        'winrm_timeout': (basestring, False),
        'winrm_use_ssl': (validator.boolean, False),
        'winrm_insecure': (validator.boolean, False),
        'winrm_use_ntlm': (validator.boolean, False),

    }

    def __init__(self, title=None, **kwargs):

        for k, v in self.communicator_props.items():
            self.props[k] = v
        # for k, (_, required) in self.communicator_props.items():
        #     v = getattr(type(self), k, None)
        #     if v is not None:
        #         pass
        super(PackerCommunicator, self).__init__(title, **kwargs)


class PackerBuilder(PackerCommunicator):

    def __init__(self, title=None, **kwargs):
        super(PackerBuilder, self).__init__(title, **kwargs)


class AmazonSourceAmiFilter(PackerProperty):
    """
    https://www.packer.io/docs/builders/amazon-ebs.html#source_ami_filter
    """
    props = {
        'filters': (dict, False),
        'owners': ([basestring], False),
        'most_recent': (validator.boolean, False),
    }


class AmazonEbs(PackerBuilder):
    """
    Amazon EBS Builder
    https://www.packer.io/docs/builders/amazon-ebs.html
    """
    resource_type = "amazon-ebs"

    """
    AWS EBS Template Variables
    https://www.packer.io/docs/builders/amazon-ebs.html#ami_description
    TODO impl launch_block_device_mappings, ami_block_device_mappings types
        impl validation ami_virtualization_type region_kms_key_ids run_volume_tags shutdown_behavior
            spot_price_auto_product ssh_keypair_name
    """
    SourceAMI = TemplateVar("SourceAMI")
    BuildRegion = TemplateVar("BuildRegion")

    props = {
        'access_key': (basestring, True),
        'ami_name': (basestring, True),
        'instance_type': (basestring, True),
        'region': (basestring, True),
        'secret_key': (basestring, True),
        'source_ami': (basestring, False),
        'source_ami_filter': (AmazonSourceAmiFilter, False),
        'ami_block_device_mappings': (basestring, False),
        'ami_description': (basestring, False),
        'ami_groups': ([basestring], False),
        'ami_product_codes': (basestring, False),
        'ami_regions': ([basestring], False),
        'ami_users': ([basestring], False),
        'ami_virtualization_type': (basestring, False),
        'associate_public_ip_address': (validator.boolean, False),
        'availability_zone': (basestring, False),
        'custom_endpoint_ec2': (basestring, False),
        'disable_stop_instance': (validator.boolean, False),
        'ebs_optimized': (validator.boolean, False),
        'enhanced_networking': (validator.boolean, False),
        'force_deregister': (validator.boolean, False),
        'force_delete_snapshot': (validator.boolean, False),
        'encrypt_boot': (validator.boolean, False),
        'kms_key_id': (basestring, False),
        'iam_instance_profile': (basestring, False),
        'launch_block_device_mappings': (basestring, False),
        'mfa_code': (basestring, False),
        'profile': (basestring, False),
        'region_kms_key_ids': (dict, False),
        'run_tags': (dict, False),
        'run_volume_tags': (dict, False),
        'security_group_id': (basestring, False),
        'security_group_ids': ([basestring], False),
        'shutdown_behavior': ([basestring], False),
        'skip_region_validation': (validator.boolean, False),
        'snapshot_groups': (basestring, False),
        'snapshot_users': (dict, False),
        'spot_price': (basestring, False),
        'spot_price_auto_product': (basestring, False),
        'ssh_keypair_name': (basestring, False),
        'ssh_agent_auth': (validator.boolean, False),
        'ssh_private_ip': (validator.boolean, False),
        'subnet_id': (basestring, False),
        'tags': (dict, False),
        'temporary_key_pair_name': (basestring, False),
        'token': (basestring, False),
        'user_data': (basestring, False),
        'user_data_file': (basestring, False),
        'vpc_id': (basestring, False),
        'windows_password_timeout': (basestring, False),
    }

    def validate(self):
        conds = [
            'source_ami',
            'source_ami_filter',
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)

        conds = [
            'security_group_id',
            'security_group_ids',
        ]
        validator.mutually_exclusive(self.__class__.__name__, self.properties, conds)


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
