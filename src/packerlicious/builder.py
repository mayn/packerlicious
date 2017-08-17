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


class VirtualboxIso(PackerBuilder):
    """
    VirtualBox ISO Builder
    https://www.packer.io/docs/builders/virtualbox-iso.html
    """
    resource_type = "virtualbox-iso"

    # VirtualBox OVF checksum types
    NONE = "none"
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"
    OVF = "ovf"
    OVA = "ova"

    props = {
        'iso_checksum': (basestring, False),
        'iso_checksum_type': (validator.string_list_item([NONE, MD5, SHA1, SHA256, SHA512]), True),
        'iso_checksum_url': (basestring, False),
        'iso_url': (basestring, True),
        'boot_command': ([basestring], False),
        'boot_wait': (basestring, False),
        'disk_size': (int, False),
        'export_opts': ([basestring], False),
        'floppy_files': ([basestring], False),
        'floppy_dirs': ([basestring], False),
        'format': (validator.string_list_item([OVF, OVA]), False),
        'guest_additions_mode': (validator.string_list_item(["upload", "attach", "disable"]), False),
        'guest_additions_path': (basestring, False),
        'guest_additions_sha256': (basestring, False),
        'guest_additions_url': (basestring, False),
        'guest_additions_url': (basestring, False),
        'guest_os_type': (basestring, False),
        'hard_drive_interface': (basestring, False),
        'sata_port_count': (int, False),
        'hard_drive_nonrotational': (validator.boolean, False),
        'hard_drive_discard': (validator.boolean, False),
        'headless': (validator.boolean, False),
        'http_directory': (basestring, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'iso_interface': (basestring, False),
        'iso_target_extension': (basestring, False),
        'iso_target_path': (basestring, False),
        'iso_urls': ([basestring], False),
        'keep_registered': (validator.boolean, False),
        'output_directory': (basestring, False),
        'post_shutdown_delay': (basestring, False),
        'shutdown_command': (basestring, False),
        'shutdown_timeout': (basestring, False),
        'skip_export': (validator.boolean, False),
        'ssh_host_port_min': (int, False),
        'ssh_host_port_max': (int, False),
        'ssh_skip_nat_mapping': (validator.boolean, False),
        'vboxmanage': ([[basestring]], False),
        'vboxmanage_post': ([[basestring]], False),
        'virtualbox_version_file': (basestring, False),
        'vm_name': (basestring, False),
        'vrdp_bind_address': (basestring, False),
        'vrdp_port_min': (int, False),
        'vrdp_port_max': (int, False),
    }

    def validate(self):
        conds = [
            'iso_checksum',
            'iso_checksum_url',
        ]
        validator.mutually_exclusive(self.__class__.__name__, self.properties, conds)


class VirtualboxOvf(PackerBuilder):
    """
    VirtualBox OVF Builder
    https://www.packer.io/docs/builders/virtualbox-ovf.html
    """
    resource_type = "virtualbox-ovf"

    # VirtualBox OVF checksum types
    NONE = "none"
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"
    OVF = "ovf"
    OVA = "ova"

    props = {
        'source_path': (basestring, True),
        'boot_command': ([basestring], False),
        'boot_wait': (basestring, False),
        'checksum': (basestring, False),
        'checksum_type': (validator.string_list_item([NONE, MD5, SHA1, SHA256, SHA512]), False),
        'export_opts': ([basestring], False),
        'floppy_files': ([basestring], False),
        'floppy_dirs': ([basestring], False),
        'format': (validator.string_list_item([OVF, OVA]), False),
        'guest_additions_mode': (validator.string_list_item(["upload", "attach", "disable"]), False),
        'guest_additions_path': (basestring, False),
        'guest_additions_sha256': (basestring, False),
        'guest_additions_url': (basestring, False),
        'headless': (validator.boolean, False),
        'http_directory': (basestring, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'import_flags': ([basestring], False),
        'import_opts': (basestring, False),
        'output_directory': (basestring, False),
        'post_shutdown_delay': (basestring, False),
        'shutdown_command': (basestring, False),
        'shutdown_timeout': (basestring, False),
        'skip_export': (validator.boolean, False),
        'ssh_host_port_min': (int, False),
        'ssh_host_port_max': (int, False),
        'ssh_skip_nat_mapping': (validator.boolean, False),
        'target_path': (basestring, False),
        'vboxmanage': ([[basestring]], False),
        'vboxmanage_post': ([[basestring]], False),
        'virtualbox_version_file': (basestring, False),
        'vm_name': (basestring, False),
        'vrdp_bind_address': (basestring, False),
        'vrdp_port_min': (int, False),
        'vrdp_port_max': (int, False),
    }


class VMwareIso(PackerBuilder):
    """
    VMware ISO Builder
    https://www.packer.io/docs/builders/vmware-iso.html
    """
    resource_type = "vmware-iso"

    # VMWARE ISO checksum types
    NONE = "none"
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"

    props = {
        'iso_checksum': (basestring, False),
        'iso_checksum_type': (validator.string_list_item([NONE, MD5, SHA1, SHA256, SHA512]), True),
        'iso_checksum_url': (basestring, False),
        'iso_url': (basestring, True),
        'boot_command': ([basestring], False),
        'boot_wait': (basestring, False),
        'disk_additional_size': ([int], False),
        'disk_size': (int, False),
        'disk_type_id': (basestring, False),
        'floppy_files': ([basestring], False),
        'floppy_dirs': ([basestring], False),
        'fusion_app_path': (basestring, False),
        'guest_os_type': (basestring, False),
        'headless': (validator.boolean, False),
        'http_directory': (basestring, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'iso_target_extension': (basestring, False),
        'iso_target_path': (basestring, False),
        'iso_urls': ([basestring], False),
        'output_directory': (basestring, False),
        'remote_cache_datastore': (basestring, False),
        'remote_cache_directory': (basestring, False),
        'remote_datastore': (basestring, False),
        'remote_host': (basestring, False),
        'remote_password': (basestring, False),
        'remote_private_key_file': (basestring, False),
        'remote_type': (basestring, False),
        'remote_username': (basestring, False),
        'shutdown_command': (basestring, False),
        'shutdown_timeout': (basestring, False),
        'skip_compaction': (validator.boolean, False),
        'skip_export': (validator.boolean, False),
        'keep_registered': (validator.boolean, False),
        'ovftool_options': ([basestring], False),
        'tools_upload_flavor': (basestring, False),
        'tools_upload_path': (basestring, False),
        'version': (basestring, False),
        'vm_name': (basestring, False),
        'vmdk_name': (basestring, False),
        'vmx_data': (dict, False),
        'vmx_data_post': (dict, False),
        'vmx_remove_ethernet_interfaces': (validator.boolean, False),
        'vmx_template_path': (basestring, False),
        'vnc_bind_address': (basestring, False),
        'vnc_disable_password': (validator.boolean, False),
        'vnc_port_min': (int, False),
        'vnc_port_max': (int, False),
    }

    def validate(self):
        conds = [
            'iso_checksum',
            'iso_checksum_url',
        ]
        validator.mutually_exclusive(self.__class__.__name__, self.properties, conds)


class VMwareVmx(PackerBuilder):
    """
    VMware VMX Builder
    https://www.packer.io/docs/builders/vmware-vmx.html
    """
    resource_type = "vmware-vmx"

    props = {
        'source_path': (basestring, True),
        'boot_command': ([basestring], False),
        'boot_wait': (basestring, False),
        'floppy_files': ([basestring], False),
        'floppy_dirs': ([basestring], False),
        'fusion_app_path': (basestring, False),
        'headless': (validator.boolean, False),
        'http_directory': (basestring, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'output_directory': (basestring, False),
        'shutdown_command': (basestring, False),
        'shutdown_timeout': (basestring, False),
        'skip_compaction': (validator.boolean, False),
        'tools_upload_flavor': (basestring, False),
        'tools_upload_path': (basestring, False),
        'vm_name': (basestring, False),
        'vmx_data': (dict, False),
        'vmx_data_post': (dict, False),
        'vmx_remove_ethernet_interfaces': (validator.boolean, False),
        'vnc_bind_address': (basestring, False),
        'vnc_disable_password': (validator.boolean, False),
        'vnc_port_min': (int, False),
        'vnc_port_max': (int, False),
    }
