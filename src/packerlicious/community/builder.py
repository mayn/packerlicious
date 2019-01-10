"""
Copyright 2018 Matthew Aynalem
Copyright 2018 Thor K. Høgås <thor at roht no>

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

    base_props = {
        # Connection
        'vcenter_server':           (str, True),
        'username':                 (str, True),
        'password':                 (str, True),
        'insecure_connection':      (validator.boolean, False),
        'datacenter':               (str, True),

        # VM location
        'vm_name':                  (str, True),
        'notes':                    (str, True),
        'folder':                   (str, False),
        'host':                     (str, False),
        'cluster':                  (str, True),
        'resource_pool':            (str, False),
        'datastore':                (str, True),

        # hardware
        'CPUs':                     (validator.integer, True),
        'CPU_limit':                (validator.integer, False),
        'CPU_reservation':          (validator.integer, False),
        'CPU_hot_plug':             (validator.boolean, False),
        'RAM':                      (validator.integer, True),
        'RAM_reservation':          (validator.integer, False),
        'RAM_reserve_all':          (validator.boolean, True),
        'RAM_hot_plug':             (validator.boolean, False),
        'disk_size':                (validator.integer, True),
        'NestedHV':                 (validator.boolean, False),

        # VM
        'create_snapshot':          (validator.boolean, False),
        'configuration_parameters': (map, False),
        'boot_order':               (str, False),

        # provisioning
        'communicator':             (str, False),
        'ssh_username':             (str, True),
        'ssh_password':             (str, False),
        'ssh_private_key_file':     (str, False),
        'winrm_username':           (str, False),
        'winrm_password':           (str, False),
        'shutdown_command':         (str, False),
        'shutdown_timeout':         (str, False)
    }

    def validate(self):
        conds = [
                'ssh_password',
                'ssh_private_key_file'
        ]
        validator.mutually_exclusive(self.__class__.__name__, self.properties, conds)

    def __init__(self, title=None, **kwargs):
        for k, v in list(self.base_props.items()):
            self.props[k] = v
        super().__init__(title, **kwargs)


class VsphereClone(VsphereBase):
    """
    JetBrains vSphere Clone Builder
    https://github.com/jetbrains-infra/packer-builder-vsphere#parameter-reference
    """
    resource_type = 'vsphere-clone'

    _props = {
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

    props                        = {
        # Hardware
        'vm_version':            (int, False),
        # https://pubs.vmware.com/vsphere-6-5/index.jsp?topic=%2Fcom.vmware.wssdk.apiref.doc%2Fvim.vm.GuestOsDescriptor.GuestOsIdentifier.html
        'guest_os_type':         (str, True),
        'disk_controller_type':  (str, False),
        'disk_thin_provisioned': (validator.boolean, False),
        'disk_controller_type':  (str, False),
        'network':               (str, True),
        'network_card':          (str, False),
        'usb_controller':        (validator.boolean, False),
        'cdrom_type':            (str, False),
        'firmware':              (str, False),

        # Boot and media
        'boot_wait':             (int, False),
        'boot_command':          ([str], False),
        'floppy_dirs':           ([str], False),
        'floppy_files':          ([str], False),
        'floppy_img_path':       (str, False),
        'iso_paths':             ([str], False),
        'iso_urls':              ([str], False),
        'iso_checksum':          (str, False),
        'iso_checksum_type':     (str, False),
        'iso_checksum_url':      (str, False),
        'http_directory':        (str, False),
        'http_ip':               (str, False)
    }

