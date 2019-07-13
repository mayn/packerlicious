"""
Copyright 2018 Matthew Aynalem

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

from .. import validator
from ..builder import PackerBuilder


class ArmImage(PackerBuilder):
    """
    ARM Builder
    https://github.com/solo-io/packer-builder-arm-image
    """
    resource_type = "arm-image"

    props = {
        'iso_url': (str, True),
        'iso_checksum_type': (str, True),
        'iso_checksum': (str, True),
        'last_partition_extra_size': (int, False)
    }


class VsphereBase(PackerBuilder):
    """
    JetBrains vSphere ISO Builder
    https://github.com/jetbrains-infra/packer-builder-vsphere#parameter-reference
    """

    network_adapter_types = ['vlance', 'vmxnet', 'flexible', 'e1000', 'e1000e', 'vmxnet2', 'vmxnet3']

    base_props = {
        # Connection
        'vcenter_server':           (str, True),
        'username':                 (str, True),
        'password':                 (str, True),
        'insecure_connection':      (validator.boolean, False),
        'datacenter':               (str, False),

        # VM location
        'vm_name':                  (str, True),
        'notes':                    (str, False),
        'folder':                   (str, False),
        'host':                     (str, False),
        'cluster':                  (str, True),
        'resource_pool':            (str, False),
        'datastore':                (str, True),

        # hardware
        'CPUs':                     (validator.integer, False),
        'cpu_cores':                (validator.integer, False),
        'CPU_limit':                (validator.integer, False),
        'CPU_reservation':          (validator.integer, False),
        'CPU_hot_plug':             (validator.boolean, False),
        'RAM':                      (validator.integer, False),
        'RAM_reservation':          (validator.integer, False),
        'RAM_reserve_all':          (validator.boolean, False),
        'RAM_hot_plug':             (validator.boolean, False),
        'NestedHV':                 (validator.boolean, False),
        'video_ram':                (validator.integer, False),
        'firmware':                 (str, False),
        'network':                  (str, False),
        'network_card':             (validator.string_list_item(network_adapter_types), False),

        # VM
        'configuration_parameters': (dict, False),
        'boot_order':               (str, False),

        # provisioning
        'communicator':             (str, False),
        'ssh_username':             (str, True),
        'ssh_password':             (str, False),
        'ssh_private_key_file':     (str, False),
        'winrm_username':           (str, False),
        'winrm_password':           (str, False),
        'shutdown_command':         (str, False),
        'shutdown_timeout':         (str, False),

        # post-processing
        'create_snapshot':          (validator.boolean, False),
        'convert_to_template':      (validator.boolean, False)
    }

    def __init__(self, title=None, **kwargs):
        for k, v in list(self.base_props.items()):
            self.props[k] = v
        super(VsphereBase, self).__init__(title, **kwargs)


class VsphereClone(VsphereBase):
    """
    JetBrains vSphere Clone Builder
    https://github.com/jetbrains-infra/packer-builder-vsphere#parameter-reference
    """
    resource_type = 'vsphere-clone'

    props = {
        # VM location
        'template':     (str, True),
        'linked_clone': (validator.boolean, False),
    }


class VsphereIso(VsphereBase):
    """
    JetBrains vSphere ISO Builder
    https://github.com/jetbrains-infra/packer-builder-vsphere#parameter-reference
    """
    resource_type = "vsphere-iso"

    disk_controller_types = ['lsilogic', 'lsilogic-sas', 'pvscsi', 'nvme']

    props = {
        # Hardware
        'vm_version':            (int, False),
        # https://pubs.vmware.com/vsphere-6-5/index.jsp?topic=%2Fcom.vmware.wssdk.apiref.doc%2Fvim.vm.GuestOsDescriptor.GuestOsIdentifier.html
        'guest_os_type':         (str, False),
        'disk_size':             (validator.integer, True),
        'disk_controller_type':  (validator.string_list_item(disk_controller_types), False),
        'disk_thin_provisioned': (validator.boolean, False),
        'disk_controller_type':  (str, False),
        'usb_controller':        (validator.boolean, False),
        'cdrom_type':            (str, False),

        # Boot and media
        'boot_wait':             (str, False),
        'boot_command':          ([str], False),
        'floppy_dirs':           ([str], False),
        'floppy_files':          ([str], False),
        'floppy_img_path':       (str, False),
        'iso_paths':             ([str], False),
        'iso_url':               (str, False),
        'iso_urls':              ([str], False),
        'iso_checksum':          (str, False),
        'iso_checksum_type':     (str, False),
        'iso_checksum_url':      (str, False),
        'http_directory':        (str, False),
        'http_ip':               (str, False),
        'http_port_min':         (validator.integer, False),
        'http_port_max':         (validator.integer, False),
    }

    def validate(self):
        conds = [
            'iso_url',
            'iso_urls',
        ]
        validator.mutually_exclusive(self.__class__.__name__, self.properties, conds)


