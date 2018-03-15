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


from . import BasePackerObject, PackerProperty, TemplateVar, validator


class PackerCommunicator(BasePackerObject):
    """
    packer communicator
    https://www.packer.io/docs/templates/communicator.html
    TODO attribute validation
    """
    communicator_props = {
        'communicator': (str, False),
        # ssh communicator props
        'ssh_bastion_agent_auth': (validator.boolean, False),
        'ssh_bastion_host': (str, False),
        'ssh_bastion_password': (str, False),
        'ssh_bastion_port': (validator.integer, False),
        'ssh_bastion_private_key_file': (str, False),
        'ssh_bastion_username': (str, False),
        'ssh_disable_agent': (validator.boolean, False),
        'ssh_file_transfer_method': (str, False),
        'ssh_handshake_attempts': (validator.integer, False),
        'ssh_host': (str, False),
        'ssh_password': (str, False),
        'ssh_port': (validator.integer, False),
        'ssh_private_key_file': (str, False),
        'ssh_pty': (validator.boolean, False),
        'ssh_timeout': (str, False),
        'ssh_username': (str, False),
        # WinRM communicator props
        'winrm_host': (str, False),
        'winrm_port': (validator.integer, False),
        'winrm_username': (str, False),
        'winrm_password': (str, False),
        'winrm_timeout': (str, False),
        'winrm_use_ssl': (validator.boolean, False),
        'winrm_insecure': (validator.boolean, False),
        'winrm_use_ntlm': (validator.boolean, False),

    }

    def __init__(self, title=None, **kwargs):

        for k, v in list(self.communicator_props.items()):
            self.props[k] = v
        # for k, (_, required) in self.communicator_props.items():
        #     v = getattr(type(self), k, None)
        #     if v is not None:
        #         pass
        super(PackerCommunicator, self).__init__(title, **kwargs)


class PackerBuilder(PackerCommunicator):

    def __init__(self, title=None, **kwargs):
        super(PackerBuilder, self).__init__(title, **kwargs)


class Alicloud(PackerBuilder):
    """
    Alicloud Image Builder
    https://www.packer.io/docs/builders/alicloud-ecs.html
    """
    resource_type = "alicloud-ecs"

    props = {
        'access_key': (str, True),
        'instance_type': (str, True),
        'image_name': (str, True),
        'region': (str, True),
        'secret_key': (str, True),
        'source_image': (str, True),
        'skip_region_validation': (validator.boolean, False),
        'image_description': (str, False),
        'image_version': (str, False),
        'image_share_account': ([str], False),
        'image_copy_regions': ([str], False),
        'image_copy_names': ([str], False),
        'image_force_delete': (validator.boolean, False),
        'image_force_delete_snapshots': (validator.boolean, False),
        'disk_name': (str, False),
        'disk_category': (str, False),
        'disk_size': (int, False),
        'disk_snapshot_id': (str, False),
        'disk_description': (str, False),
        'disk_delete_with_instance': (str, False),
        'disk_device': (str, False),
        'zone_id': (str, False),
        'io_optimized': (str, False),
        'force_stop_instance': (validator.boolean, False),
        'security_group_id': (str, False),
        'security_group_name': (str, False),
        'user_data': (str, False),
        'user_data_file': (str, False),
        'vpc_id': (str, False),
        'vpc_name': (str, False),
        'vpc_cidr_block': (str, False),
        'vswitch_id': (str, False),
        'instance_name': (str, False),
        'internet_charge_type': (str, False),
        'internet_max_bandwidth_out': (str, False),
        'temporary_key_pair_name': (str, False),
    }


class AmazonSourceAmiFilter(PackerProperty):
    """
    https://www.packer.io/docs/builders/amazon-ebs.html#source_ami_filter
    """
    props = {
        'filters': (dict, False),
        'owners': ([str], False),
        'most_recent': (validator.boolean, False),
    }


class BlockDeviceMapping(PackerProperty):
    """
    https://www.packer.io/docs/builders/amazon-instance.html#ami_block_device_mappings
    """
    props = {
        'delete_on_termination': (validator.boolean, False),
        'device_name': (str, False),
        'encrypted': (validator.boolean, False),
        'iops': (int, False),
        'no_device': (validator.boolean, False),
        'snapshot_id': (str, False),
        'virtual_name': (str, False),
        'volume_size': (int, False),
        'volume_type': (str, False),

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
    TODO impl validation ami_virtualization_type region_kms_key_ids run_volume_tags shutdown_behavior
            spot_price_auto_product ssh_keypair_name
    """
    SourceAMI = TemplateVar("SourceAMI")
    BuildRegion = TemplateVar("BuildRegion")

    props = {
        'access_key': (str, True),
        'ami_name': (str, True),
        'instance_type': (str, True),
        'region': (str, True),
        'secret_key': (str, True),
        'source_ami': (str, False),
        'source_ami_filter': (AmazonSourceAmiFilter, False),
        'ami_block_device_mappings': ([BlockDeviceMapping], False),
        'ami_description': (str, False),
        'ami_groups': ([str], False),
        'ami_product_codes': (str, False),
        'ami_regions': ([str], False),
        'ami_users': ([str], False),
        'ami_virtualization_type': (str, False),
        'associate_public_ip_address': (validator.boolean, False),
        'availability_zone': (str, False),
        'custom_endpoint_ec2': (str, False),
        'disable_stop_instance': (validator.boolean, False),
        'ebs_optimized': (validator.boolean, False),
        'enhanced_networking': (validator.boolean, False),
        'force_deregister': (validator.boolean, False),
        'force_delete_snapshot': (validator.boolean, False),
        'encrypt_boot': (validator.boolean, False),
        'kms_key_id': (str, False),
        'iam_instance_profile': (str, False),
        'launch_block_device_mappings': ([BlockDeviceMapping], False),
        'mfa_code': (str, False),
        'profile': (str, False),
        'region_kms_key_ids': (dict, False),
        'run_tags': (dict, False),
        'run_volume_tags': (dict, False),
        'security_group_id': (str, False),
        'security_group_ids': ([str], False),
        'shutdown_behavior': ([str], False),
        'skip_region_validation': (validator.boolean, False),
        'snapshot_groups': ([str], False),
        'snapshot_users': ([str], False),
        'snapshot_tags': ([str], False),
        'spot_price': (str, False),
        'spot_price_auto_product': (str, False),
        'ssh_keypair_name': (str, False),
        'ssh_agent_auth': (validator.boolean, False),
        'ssh_private_ip': (validator.boolean, False),
        'subnet_id': (str, False),
        'tags': (dict, False),
        'temporary_key_pair_name': (str, False),
        'temporary_security_group_source_cidr': (str, False),
        'token': (str, False),
        'user_data': (str, False),
        'user_data_file': (str, False),
        'vpc_id': (str, False),
        'windows_password_timeout': (str, False),
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


class AmazonChroot(PackerBuilder):
    """
    Amazon Chroot Builder
    https://www.packer.io/docs/builders/amazon-chroot.html
    """
    resource_type = "amazon-chroot"

    SourceAMI = TemplateVar("SourceAMI")
    BuildRegion = TemplateVar("BuildRegion")

    props = {
        'access_key': (str, True),
        'ami_name': (str, True),
        'secret_key': (str, True),
        'source_ami': (str, False),
        'ami_description': (str, False),
        'ami_groups': ([str], False),
        'ami_product_codes': ([str], False),
        'ami_regions': ([str], False),
        'ami_users': ([str], False),
        'ami_virtualization_type': (str, False),
        'chroot_mounts': ([[str]], False),
        'command_wrapper': (str, False),
        'copy_files': ([str], False),
        'custom_endpoint_ec2': (str, False),
        'device_path': (str, False),
        'ena_support': (validator.boolean, False),
        'force_deregister': (validator.boolean, False),
        'force_delete_snapshot': (validator.boolean, False),
        'encrypt_boot': (validator.boolean, False),
        'kms_key_id': (str, False),
        'from_scratch': (validator.boolean, False),
        'ami_block_device_mappings': ([BlockDeviceMapping], False),
        'region_kms_key_ids': (dict, False),
        'root_device_name': (str, False),
        'mfa_code': (str, False),
        'mount_path': (str, False),
        'mount_partition': (int, False),
        'mount_options': ([str], False),
        'pre_mount_commands': ([str], False),
        'profile': (str, False),
        'post_mount_commands': ([str], False),
        'root_volume_size': (int, False),
        'skip_region_validation': (validator.boolean, False),
        'snapshot_tags': ([str], False),
        'snapshot_groups': ([str], False),
        'snapshot_users': ([str], False),
        'source_ami_filter': (AmazonSourceAmiFilter, False),
        'sriov_support': (validator.boolean, False),
        'tags': (dict, False),
    }

    def validate(self):
        conds = [
            'source_ami',
            'source_ami_filter',
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)


class AmazonEbsSurrogate(PackerBuilder):
    """
    Amazon EBS Builder
    https://www.packer.io/docs/builders/amazon-ebssurrogate.html
    """
    resource_type = "amazon-ebssurrogate"

    SourceAMI = TemplateVar("SourceAMI")
    BuildRegion = TemplateVar("BuildRegion")

    props = {
        'access_key': (str, True),
        'instance_type': (str, True),
        'region': (str, True),
        'secret_key': (str, True),
        'ami_root_device': ([BlockDeviceMapping], True),
        'source_device_name': (str, True),
        'source_ami': (str, False),
        'ami_block_device_mappings': ([BlockDeviceMapping], False),
        'ami_description': (str, False),
        'ami_groups': ([str], False),
        'ami_product_codes': ([str], False),
        'ami_regions': ([str], False),
        'ami_users': ([str], False),
        'ami_virtualization_type': (str, False),
        'associate_public_ip_address': (validator.boolean, False),
        'availability_zone': (str, False),
        'custom_endpoint_ec2': (str, False),
        'disable_stop_instance': (validator.boolean, False),
        'ebs_optimized': (validator.boolean, False),
        'ena_support': (validator.boolean, False),
        'force_deregister': (validator.boolean, False),
        'force_delete_snapshot': (validator.boolean, False),
        'encrypt_boot': (validator.boolean, False),
        'kms_key_id': (str, False),
        'iam_instance_profile': (str, False),
        'launch_block_device_mappings': ([BlockDeviceMapping], False),
        'mfa_code': (str, False),
        'profile': (str, False),
        'region_kms_key_ids': (dict, False),
        'run_tags': (dict, False),
        'run_volume_tags': (dict, False),
        'security_group_id': (str, False),
        'security_group_ids': ([str], False),
        'shutdown_behavior': ([str], False),
        'skip_region_validation': (validator.boolean, False),
        'snapshot_groups': ([str], False),
        'snapshot_users': ([str], False),
        'snapshot_tags': ([str], False),
        'source_ami_filter': (AmazonSourceAmiFilter, False),
        'spot_price': (str, False),
        'spot_price_auto_product': (str, False),
        'sriov_support': (validator.boolean, False),
        'ssh_keypair_name': (str, False),
        'ssh_agent_auth': (validator.boolean, False),
        'ssh_private_ip': (validator.boolean, False),
        'subnet_id': (str, False),
        'tags': (dict, False),
        'temporary_key_pair_name': (str, False),
        'temporary_security_group_source_cidr': (str, False),
        'token': (str, False),
        'user_data': (str, False),
        'user_data_file': (str, False),
        'vpc_id': (str, False),
        'windows_password_timeout': (str, False),
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


class AmazonEbsVolume(PackerBuilder):
    """
    Amazon EBS Builder
    https://www.packer.io/docs/builders/amazon-ebsvolume.html
    """
    resource_type = "amazon-ebsvolume"

    SourceAMI = TemplateVar("SourceAMI")
    BuildRegion = TemplateVar("BuildRegion")

    props = {
        'access_key': (str, True),
        'instance_type': (str, True),
        'region': (str, True),
        'secret_key': (str, True),
        'source_ami': (str, False),
        'ebs_volumes': ([BlockDeviceMapping], False),
        'associate_public_ip_address': (validator.boolean, False),
        'availability_zone': (str, False),
        'custom_endpoint_ec2': (str, False),
        'ebs_optimized': (validator.boolean, False),
        'ena_support': (validator.boolean, False),
        'iam_instance_profile': (str, False),
        'mfa_code': (str, False),
        'profile': (str, False),
        'region_kms_key_ids': (dict, False),
        'run_tags': (dict, False),
        'security_group_id': (str, False),
        'security_group_ids': ([str], False),
        'shutdown_behavior': ([str], False),
        'skip_region_validation': (validator.boolean, False),
        'snapshot_groups': ([str], False),
        'snapshot_users': ([str], False),
        'source_ami_filter': (AmazonSourceAmiFilter, False),
        'spot_price': (str, False),
        'spot_price_auto_product': (str, False),
        'sriov_support': (validator.boolean, False),
        'ssh_keypair_name': (str, False),
        'ssh_private_ip': (validator.boolean, False),
        'subnet_id': (str, False),
        'temporary_key_pair_name': (str, False),
        'temporary_security_group_source_cidr': (str, False),
        'token': (str, False),
        'user_data': (str, False),
        'user_data_file': (str, False),
        'vpc_id': (str, False),
        'windows_password_timeout': (str, False),
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


class AmazonInstance(PackerBuilder):
    """
    Amazon Instance Store Builder
    https://www.packer.io/docs/builders/amazon-instance.html
    """
    resource_type = "amazon-instance"

    """
    AWS Instance Template Variables
    https://www.packer.io/docs/builders/amazon-ebs.html#ami_description
    TODO impl validation ami_virtualization_type region_kms_key_ids run_volume_tags shutdown_behavior
            spot_price_auto_product ssh_keypair_name
    """
    SourceAMI = TemplateVar("SourceAMI")
    BuildRegion = TemplateVar("BuildRegion")

    props = {
        'access_key': (str, True),
        'account_id': (str, True),
        'ami_name': (str, True),
        'instance_type': (str, True),
        'region': (str, True),
        's3_bucket': (str, True),
        'secret_key': (str, True),
        'source_ami': (str, False),
        'source_ami_filter': (AmazonSourceAmiFilter, False),
        'x509_cert_path': (str, True),
        'x509_key_path': (str, True),
        'ami_block_device_mappings': ([BlockDeviceMapping], False),
        'ami_description': (str, False),
        'ami_groups': ([str], False),
        'ami_product_codes': (str, False),
        'ami_regions': ([str], False),
        'ami_users': ([str], False),
        'ami_virtualization_type': (str, False),
        'associate_public_ip_address': (validator.boolean, False),
        'availability_zone': (str, False),
        'bundle_destination': (str, False),
        'bundle_prefix': (str, False),
        'bundle_upload_command': (str, False),
        'bundle_vol_command': (str, False),
        'custom_endpoint_ec2': (str, False),
        'ebs_optimized': (validator.boolean, False),
        'enhanced_networking': (validator.boolean, False),
        'force_deregister': (validator.boolean, False),
        'force_delete_snapshot': (validator.boolean, False),
        'iam_instance_profile': (str, False),
        'launch_block_device_mappings': ([BlockDeviceMapping], False),
        'mfa_code': (str, False),
        'profile': (str, False),
        'region_kms_key_ids': (dict, False),
        'run_tags': (dict, False),
        'security_group_id': (str, False),
        'security_group_ids': ([str], False),
        'skip_region_validation': (validator.boolean, False),
        'snapshot_groups': ([str], False),
        'snapshot_users': ([str], False),
        'snapshot_tags': ([str], False),
        'spot_price': (str, False),
        'spot_price_auto_product': (str, False),
        'ssh_keypair_name': (str, False),
        'ssh_agent_auth': (validator.boolean, False),
        'ssh_private_ip': (validator.boolean, False),
        'subnet_id': (str, False),
        'tags': (dict, False),
        'temporary_key_pair_name': (str, False),
        'temporary_security_group_source_cidr': (str, False),
        'user_data': (str, False),
        'user_data_file': (str, False),
        'vpc_id': (str, False),
        'x509_upload_path': (str, False),
        'windows_password_timeout': (str, False),
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


class Azure(PackerBuilder):
    """
    Azure Builder
    https://www.packer.io/docs/builders/azure.html
    TODO better validation for VHD/ Managed Images required fields
    """
    resource_type = "azure-arm"

    props = {
        'client_id': (str, True),
        'client_secret': (str, True),
        'subscription_id': (str, True),
        'capture_container_name': (str, False),
        'capture_name_prefix': (str, False),
        'image_publisher': (str, True),
        'image_offer': (str, True),
        'image_sku': (str, True),
        'location': (str, True),
        'azure_tags': (dict, False),
        'cloud_environment_name': (str, False),
        'custom_data_file': (str, False),
        'custom_managed_image_name': (str, False),
        'custom_managed_image_resource_group_name': (str, False),
        'image_version': (str, False),
        'image_url': (str, False),
        'managed_image_name': (str, False),
        'managed_image_resource_group_name': (str, False),
        'object_id': (str, False),
        'os_disk_size_gb': (int, False),
        'os_type': (str, False),
        'temp_compute_name': (str, False),
        'temp_resource_group_name': (str, False),
        'tenant_id': (str, False),
        'private_virtual_network_with_public_ip': (validator.boolean, False),
        'resource_group_name': (str, False),
        'storage_account': (str, False),
        'virtual_network_name': (str, False),
        'virtual_network_resource_group_name': (str, False),
        'virtual_network_subnet_name': (str, False),
        'vm_size': (str, False),
    }


class CloudStack(PackerBuilder):
    """
    CloudStack Builder
    https://www.packer.io/docs/builders/cloudstack.html
    """
    resource_type = "cloudstack"

    props = {
        'api_url': (str, True),
        'api_key': (str, True),
        'network': (str, True),
        'secret_key': (str, True),
        'service_offering': (str, True),
        'source_iso': (str, False),
        'source_template': (str, False),
        'template_os': (str, True),
        'zone': (str, True),
        'async_timeout': (int, False),
        'cidr_list': ([str], False),
        'disk_offering': (str, False),
        'disk_size': (int, False),
        'expunge': (validator.boolean, False),
        'http_directory': (str, False),
        'http_get_only': (validator.boolean, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'hypervisor': (str, False),
        'keypair': (str, False),
        'instance_name': (str, False),
        'project': (str, False),
        'public_ip_address': (str, False),
        'ssh_agent_auth': (validator.boolean, False),
        'ssl_no_verify': (validator.boolean, False),
        'template_display_text': (str, False),
        'template_featured': (validator.boolean, False),
        'template_name': (str, False),
        'template_public': (validator.boolean, False),
        'template_password_enabled': (validator.boolean, False),
        'template_requires_hvm': (validator.boolean, False),
        'template_scalable': (validator.boolean, False),
        'user_data': (str, False),
        'user_data_file': (str, False),
        'use_local_ip_address': (validator.boolean, False),
    }

    def validate(self):
        conds = [
            'source_iso',
            'source_template',
        ]
        validator.mutually_exclusive(self.__class__.__name__, self.properties, conds)


class DigitalOcean(PackerBuilder):
    """
    Digital Ocean Builder
    https://www.packer.io/docs/builders/digitalocean.html
    """
    resource_type = "digitalocean"

    props = {
        'api_token': (str, True),
        'image': (str, True),
        'region': (str, True),
        'size': (str, True),
        'api_url': (str, False),
        'droplet_name': (str, False),
        'private_networking': (validator.boolean, False),
        'monitoring': (validator.boolean, False),
        'snapshot_name': (str, False),
        'snapshot_regions': ([str], False),
        'state_timeout': (str, False),
        'user_data': (str, False),
        'user_data_file': (str, False),
    }


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
        'export_path': (str, False),
        'image': (str, True),
        'author': (str, False),
        'aws_access_key': (str, False),
        'aws_secret_key': (str, False),
        'aws_token': (str, False),
        'changes': ([str], False),
        'ecr_login': (validator.boolean, False),
        'fix_upload_owner': (validator.boolean, False),
        'login': (validator.boolean, False),
        'login_email': (str, False),
        'login_username': (str, False),
        'login_password': (str, False),
        'login_server': (str, False),
        'message': (str, False),
        'privileged': (validator.boolean, False),
        'pull': (validator.boolean, False),
        'run_command': (str, False),
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
        'target': (str, True),
        'source': (str, False),
        'content': (str, False),
    }

    def validate(self):

        conds = [
            'source',
            'content',
        ]
        specified_count = validator.mutually_exclusive(self.__class__.__name__, self.properties, conds)
        if specified_count == 0:
            warnings.warn("Both source and content not specified, artifact will be empty.")


class GoogleCompute(PackerBuilder):
    """
    Google Compute Builder
    https://www.packer.io/docs/builders/googlecompute.html
    """
    resource_type = "googlecompute"

    props = {
        'project_id': (str, True),
        'source_image': (str, True),
        'source_image_family': (str, True),
        'zone': (str, True),
        'account_file': (str, False),
        'address': (str, False),
        'disk_name': (str, False),
        'disk_size': (int, False),
        'disk_type': (str, False),
        'image_description': (str, False),
        'image_family': (str, False),
        'image_name': (str, False),
        'instance_name': (str, False),
        'machine_type': (str, False),
        'metadata': (dict, False),
        'network': (str, False),
        'network_project_id': (str, False),
        'omit_external_ip': (validator.boolean, False),
        'on_host_maintenance': (str, False),
        'preemptible': (validator.boolean, False),
        'region': (str, False),
        'scopes': ([str], False),
        'source_image_project_id': (str, False),
        'startup_script_file': (str, False),
        'state_timeout': (str, False),
        'subnetwork': (str, False),
        'tags': ([str], False),
        'use_internal_ip': (validator.boolean, False),
    }


class HyperV(PackerBuilder):
    """
    Hyper-V Builder
    https://www.packer.io/docs/builders/hyperv-iso.html
    """
    resource_type = "hyperv-iso"

    props = {
        'iso_checksum': (str, True),
        'iso_checksum_type': (str, True),
        'iso_url': (str, True),
        'boot_command': ([str], False),
        'boot_wait': (str, False),
        'cpu': (int, False),
        'disk_size': (int, False),
        'enable_dynamic_memory': (validator.boolean, False),
        'enable_mac_spoofing': (validator.boolean, False),
        'enable_secure_boot': (validator.boolean, False),
        'enable_virtualization_extensions': (validator.boolean, False),
        'floppy_files': ([str], False),
        'floppy_dirs': ([str], False),
        'generation': (int, False),
        'guest_additions_mode': (str, False),
        'guest_additions_path': (str, False),
        'http_directory': (str, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'iso_urls': ([str], False),
        'iso_target_extension': (str, False),
        'iso_target_path': (str, False),
        'output_directory': (str, False),
        'ram_size': (int, False),
        'secondary_iso_images': ([str], False),
        'shutdown_command': (str, False),
        'shutdown_timeout': (str, False),
        'skip_compaction': (validator.boolean, False),
        'switch_name': (str, False),
        'switch_vlan_id': (str, False),
        'vhd_temp_path': (str, False),
        'vlan_id': (str, False),
        'vm_name': (str, False),
        'temp_path': (str, False),
    }


class HyperVvmcx(PackerBuilder):
    """
    Hyper-V Builder (from a vmcx)
    https://www.packer.io/docs/builders/hyperv-vmcx.html
    """
    resource_type = "hyperv-vmcx"

    props = {
        'clone_from_vmxc_path': (str, False),
        'clone_from_vm_name': (str, False),
        'clone_from_snapshot_name': (str, False),
        'clone_all_snapshots': (validator.boolean, False),
        'boot_command': ([str], False),
        'boot_wait': (str, False),
        'cpu': (int, False),
        'enable_dynamic_memory': (validator.boolean, False),
        'enable_mac_spoofing': (validator.boolean, False),
        'enable_secure_boot': (validator.boolean, False),
        'enable_virtualization_extensions': (validator.boolean, False),
        'floppy_files': ([str], False),
        'floppy_dirs': ([str], False),
        'guest_additions_mode': (str, False),
        'guest_additions_path': (str, False),
        'http_directory': (str, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'iso_checksum': (str, False),
        'iso_checksum_type': (str, False),
        'iso_url': (str, False),
        'iso_urls': ([str], False),
        'iso_target_extension': (str, False),
        'iso_target_path': (str, False),
        'output_directory': (str, False),
        'ram_size': (int, False),
        'secondary_iso_images': ([str], False),
        'shutdown_command': (str, False),
        'shutdown_timeout': (str, False),
        'skip_compaction': (validator.boolean, False),
        'switch_name': (str, False),
        'switch_vlan_id': (str, False),
        'vlan_id': (str, False),
        'vm_name': (str, False),
    }

    def validate(self):
        conds = [
            'clone_from_vmxc_path',
            'clone_from_vm_name'
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)

        iso_url_conds = [
            'iso_url',
            'iso_urls'
        ]
        validator.mutually_exclusive(self.__class__.__name__, self.properties, iso_url_conds)


class LXD(PackerBuilder):
    """
    LXD Builder
    https://www.packer.io/docs/builders/lxd.html
    """
    resource_type = "lxd"

    props = {
        'image': (str, True),
        'name': (str, False),
        'output_image': (str, False),
        'command_wrapper': (str, False),
    }


class LXC(PackerBuilder):
    """
    LXC Builder
    https://www.packer.io/docs/builders/lxc.html
    """
    resource_type = "lxc"

    props = {
        'config_file': (str, True),
        'template_name': (str, True),
        'template_environment_vars': ([str], True),
        'target_runlevel': (int, False),
        'output_directory': (str, False),
        'container_name': (str, False),
        'command_wrapper': (str, False),
        'init_timeout': (str, False),
        'template_parameters': ([str], False),
    }


class Null(PackerBuilder):
    """
    Null Builder
    https://www.packer.io/docs/builders/null.html
    """
    resource_type = "null"

    props = {}


class OneAndOne(PackerBuilder):
    """
    OneAndOne Builder
    https://www.packer.io/docs/builders/oneandone.html
    """
    resource_type = "oneandone"

    props = {
        'source_image_name': (str, True),
        'token': (str, True),
        'data_center_name': (str, False),
        'disk_size': (str, False),
        'image_name': (str, False),
        'retries': (int, False),
        'url': (str, False),
    }


class OpenStack(PackerBuilder):
    """
    OpenStack Builder
    https://www.packer.io/docs/builders/openstack.html
    """
    resource_type = "openstack"

    props = {
        'flavor': (str, True),
        'image_name': (str, True),
        'identity_endpoint': (str, False),
        'source_image': (str, False),
        'source_image_name': (str, False),
        'username': (str, False),
        'user_id': (str, False),
        'password': (str, False),
        'availability_zone': (str, False),
        'cacert': (str, False),
        'config_drive': (validator.boolean, False),
        'cert': (str, False),
        'domain_name': (str, False),
        'domain_id': (str, False),
        'endpoint_type': (str, False),
        'floating_ip': (str, False),
        'floating_ip_pool': (str, False),
        'image_members': ([str], False),
        'image_visibility': (str, False),
        'insecure': (validator.boolean, False),
        'key': (str, False),
        'metadata': (dict, False),
        'instance_metadata': (dict, False),
        'networks': ([str], False),
        'rackconnect_wait': (validator.boolean, False),
        'region': (str, False),
        'reuse_ips': (validator.boolean, False),
        'security_groups': ([str], False),
        'ssh_interface': (str, False),
        'ssh_ip_version': (str, False),
        'ssh_keypair_name': (str, False),
        'ssh_agent_auth': (validator.boolean, False),
        'temporary_key_pair_name': (str, False),
        'tenant_id': (str, False),
        'tenant_name': (str, False),
        'use_floating_ip': (validator.boolean, False),
        'user_data': (str, False),
        'user_data_file': (str, False),

    }

    def validate(self):
        conds = [
            'source_image',
            'source_image_name',
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)


class OracleOCI(PackerBuilder):
    """
    OracleOCI Builder
    https://www.packer.io/docs/builders/oracle-oci.html
    """
    resource_type = "oracle-oci"

    props = {
        'availability_domain': (str, True),
        'base_image_ocid': (str, True),
        'compartment_ocid': (str, True),
        'fingerprint': (str, True),
        'shape': (str, True),
        'subnet_ocid': (str, True),
        'access_cfg_file': (str, False),
        'access_cfg_file_account': (str, False),
        'image_name': (str, False),
        'key_file': (str, False),
        'pass_phrase': (str, False),
        'region': (str, False),
        'tenancy_ocid': (str, False),
        'user_ocid': (str, False),
    }


class ParallelsISO(PackerBuilder):
    """
    ParallelsISO Builder
    https://www.packer.io/docs/builders/parallels-iso.html
    """
    resource_type = "parallels-iso"

    props = {
        'iso_checksum': (str, True),
        'iso_checksum_type': (str, True),
        'iso_checksum_url': (str, True),
        'iso_url': (str, True),
        'parallels_tools_flavour': (str, True),
        'boot_command': ([str], False),
        'boot_wait': (str, False),
        'disk_size': (int, False),
        'disk_type': (str, False),
        'floppy_files': ([str], False),
        'floppy_dirs': ([str], False),
        'guest_os_type': (str, False),
        'hard_drive_interface': (str, False),
        'host_interface': ([str], False),
        'http_directory': (str, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'iso_target_extension': (str, False),
        'iso_target_path': (str, False),
        'iso_urls': ([str], False),
        'output_directory': (str, False),
        'parallels_tools_guest_path': (str, False),
        'parallels_tools_mode': (str, False),
        'prlctl': ([[str]], False),
        'prlctl_post': ([[str]], False),
        'prlctl_version_file': (str, False),
        'shutdown_command': (str, False),
        'shutdown_timeout': (str, False),
        'skip_compaction': (bool, False),
        'vm_name': (str, False),
    }


class ParallelsPVM(PackerBuilder):
    """
    ParallelsPVM Builder
    https://www.packer.io/docs/builders/parallels-pvm.html
    """
    resource_type = "parallels-pvm"

    props = {
        'parallels_tools_flavour': (str, True),
        'source_path': (str, True),
        'boot_command': ([str], False),
        'boot_wait': (str, False),
        'floppy_files': ([str], False),
        'floppy_dirs': ([str], False),
        'output_directory': (str, False),
        'parallels_tools_guest_path': (str, False),
        'parallels_tools_mode': (str, False),
        'prlctl': ([[str]], False),
        'prlctl_post': ([[str]], False),
        'prlctl_version_file': (str, False),
        'reassign_mac': (bool, False),
        'shutdown_command': (str, False),
        'shutdown_timeout': (str, False),
        'skip_compaction': (bool, False),
        'vm_name': (str, False),
    }


class ProfitBricks(PackerBuilder):
    """
    ProfitBricks Builder
    https://www.packer.io/docs/builders/profitbricks.html
    """
    resource_type = "profitbricks"

    props = {
        'image': (str, True),
        'password': (str, True),
        'username': (str, True),
        'cores': (int, False),
        'disk_size': (str, False),
        'disk_type': (str, False),
        'location': (str, False),
        'ram': (int, False),
        'retries': (str, False),
        'snapshot_name': (str, False),
        'snapshot_password': (str, False),
        'url': (str, False),
    }


class Qemu(PackerBuilder):
    """
    QEMU Builder
    https://www.packer.io/docs/builders/qemu.html
    TODO net_device
    """
    resource_type = "qemu"

    # QEMU Checksum TYPES
    NONE = "none"
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"

    props = {
        'iso_checksum': (str, False),
        'iso_checksum_type': (validator.string_list_item([NONE, MD5, SHA1, SHA256, SHA512]), True),
        'iso_checksum_url': (str, False),
        'iso_url': (str, True),
        'accelerator': (str, False),
        'boot_command': ([str], False),
        'boot_wait': (str, False),
        'disk_cache': (str, False),
        'disk_compression': (validator.boolean, False),
        'disk_discard': (str, False),
        'disk_image': (validator.boolean, False),
        'disk_interface': (str, False),
        'disk_size': (int, False),
        'floppy_files': ([str], False),
        'floppy_dirs': ([str], False),
        'format': (validator.string_list_item(["qcow2", "raw"]), False),
        'headless': (validator.boolean, False),
        'http_directory': (str, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'iso_skip_cache': (validator.boolean, False),
        'iso_target_extension': (str, False),
        'iso_urls': ([str], False),
        'machine_type': (str, False),
        'net_device': (str, False),
        'output_directory': (str, False),
        'qemu_binary': (str, False),
        'qemuargs': ([[str]], False),
    }

    def validate(self):
        conds = [
            'iso_checksum',
            'iso_checksum_url',
        ]
        validator.mutually_exclusive(self.__class__.__name__, self.properties, conds)


class Triton(PackerBuilder):
    """
    Triton Builder
    https://www.packer.io/docs/builders/triton.html
    """
    resource_type = "triton"

    props = {
        'triton_account': (str, True),
        'triton_key_id': (str, True),
        'source_machine_image': (str, True),
        'source_machine_package': (str, True),
        'image_name': (str, True),
        'image_version': (str, True),
        'triton_url': (str, False),
        'triton_key_material': (str, False),
        'source_machine_firewall_enabled': (validator.boolean, False),
        'source_machine_metadata': (dict, False),
        'source_machine_name': (str, False),
        'source_machine_networks': ([str], False),
        'source_machine_tags': (dict, False),
        'image_acls': ([str], False),
        'image_description': (str, False),
        'image_eula_url': (str, False),
        'image_homepage': (str, False),
        'image_tags': (dict, False),
    }


class VirtualboxIso(PackerBuilder):
    """
    VirtualBox ISO Builder
    https://www.packer.io/docs/builders/virtualbox-iso.html
    """
    resource_type = "virtualbox-iso"

    # VirtualBox ISO checksum types
    NONE = "none"
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"
    OVF = "ovf"
    OVA = "ova"

    props = {
        'iso_checksum': (str, False),
        'iso_checksum_type': (validator.string_list_item([NONE, MD5, SHA1, SHA256, SHA512]), True),
        'iso_checksum_url': (str, False),
        'iso_url': (str, True),
        'boot_command': ([str], False),
        'boot_wait': (str, False),
        'disk_size': (int, False),
        'export_opts': ([str], False),
        'floppy_files': ([str], False),
        'floppy_dirs': ([str], False),
        'format': (validator.string_list_item([OVF, OVA]), False),
        'guest_additions_mode': (validator.string_list_item(["upload", "attach", "disable"]), False),
        'guest_additions_path': (str, False),
        'guest_additions_sha256': (str, False),
        'guest_additions_url': (str, False),
        'guest_os_type': (str, False),
        'hard_drive_interface': (str, False),
        'sata_port_count': (int, False),
        'hard_drive_nonrotational': (validator.boolean, False),
        'hard_drive_discard': (validator.boolean, False),
        'headless': (validator.boolean, False),
        'http_directory': (str, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'iso_interface': (str, False),
        'iso_target_extension': (str, False),
        'iso_target_path': (str, False),
        'iso_urls': ([str], False),
        'keep_registered': (validator.boolean, False),
        'output_directory': (str, False),
        'post_shutdown_delay': (str, False),
        'shutdown_command': (str, False),
        'shutdown_timeout': (str, False),
        'skip_export': (validator.boolean, False),
        'ssh_host_port_min': (int, False),
        'ssh_host_port_max': (int, False),
        'ssh_skip_nat_mapping': (validator.boolean, False),
        'vboxmanage': ([[str]], False),
        'vboxmanage_post': ([[str]], False),
        'virtualbox_version_file': (str, False),
        'vm_name': (str, False),
        'vrdp_bind_address': (str, False),
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
        'source_path': (str, True),
        'boot_command': ([str], False),
        'boot_wait': (str, False),
        'checksum': (str, False),
        'checksum_type': (validator.string_list_item([NONE, MD5, SHA1, SHA256, SHA512]), False),
        'export_opts': ([str], False),
        'floppy_files': ([str], False),
        'floppy_dirs': ([str], False),
        'format': (validator.string_list_item([OVF, OVA]), False),
        'guest_additions_mode': (validator.string_list_item(["upload", "attach", "disable"]), False),
        'guest_additions_path': (str, False),
        'guest_additions_sha256': (str, False),
        'guest_additions_url': (str, False),
        'headless': (validator.boolean, False),
        'http_directory': (str, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'import_flags': ([str], False),
        'import_opts': (str, False),
        'keep_registered': (validator.boolean, False),
        'output_directory': (str, False),
        'post_shutdown_delay': (str, False),
        'shutdown_command': (str, False),
        'shutdown_timeout': (str, False),
        'skip_export': (validator.boolean, False),
        'ssh_host_port_min': (int, False),
        'ssh_host_port_max': (int, False),
        'ssh_skip_nat_mapping': (validator.boolean, False),
        'target_path': (str, False),
        'vboxmanage': ([[str]], False),
        'vboxmanage_post': ([[str]], False),
        'virtualbox_version_file': (str, False),
        'vm_name': (str, False),
        'vrdp_bind_address': (str, False),
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
        'iso_checksum': (str, False),
        'iso_checksum_type': (validator.string_list_item([NONE, MD5, SHA1, SHA256, SHA512]), True),
        'iso_checksum_url': (str, False),
        'iso_url': (str, True),
        'boot_command': ([str], False),
        'boot_wait': (str, False),
        'disk_additional_size': ([int], False),
        'disk_size': (int, False),
        'disk_type_id': (str, False),
        'disable_vnc': (validator.boolean, False),
        'floppy_files': ([str], False),
        'floppy_dirs': ([str], False),
        'fusion_app_path': (str, False),
        'guest_os_type': (str, False),
        'headless': (validator.boolean, False),
        'http_directory': (str, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'iso_target_extension': (str, False),
        'iso_target_path': (str, False),
        'iso_urls': ([str], False),
        'output_directory': (str, False),
        'remote_cache_datastore': (str, False),
        'remote_cache_directory': (str, False),
        'remote_datastore': (str, False),
        'remote_host': (str, False),
        'remote_password': (str, False),
        'remote_private_key_file': (str, False),
        'remote_type': (str, False),
        'remote_username': (str, False),
        'shutdown_command': (str, False),
        'shutdown_timeout': (str, False),
        'skip_compaction': (validator.boolean, False),
        'skip_export': (validator.boolean, False),
        'keep_registered': (validator.boolean, False),
        'ovftool_options': ([str], False),
        'tools_upload_flavor': (str, False),
        'tools_upload_path': (str, False),
        'version': (str, False),
        'vm_name': (str, False),
        'vmdk_name': (str, False),
        'vmx_data': (dict, False),
        'vmx_data_post': (dict, False),
        'vmx_remove_ethernet_interfaces': (validator.boolean, False),
        'vmx_template_path': (str, False),
        'vnc_bind_address': (str, False),
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
        'source_path': (str, True),
        'boot_command': ([str], False),
        'boot_wait': (str, False),
        'floppy_files': ([str], False),
        'floppy_dirs': ([str], False),
        'fusion_app_path': (str, False),
        'headless': (validator.boolean, False),
        'http_directory': (str, False),
        'http_port_min': (int, False),
        'http_port_max': (int, False),
        'output_directory': (str, False),
        'shutdown_command': (str, False),
        'shutdown_timeout': (str, False),
        'skip_compaction': (validator.boolean, False),
        'tools_upload_flavor': (str, False),
        'tools_upload_path': (str, False),
        'vm_name': (str, False),
        'vmx_data': (dict, False),
        'vmx_data_post': (dict, False),
        'vmx_remove_ethernet_interfaces': (validator.boolean, False),
        'vnc_bind_address': (str, False),
        'vnc_disable_password': (validator.boolean, False),
        'vnc_port_min': (int, False),
        'vnc_port_max': (int, False),
    }
