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

from ..provisioner import PackerProvisioner as PackerProvisioner


class Inspec(PackerProvisioner):
    """
    Inspec Provisioner
    https://github.com/jrbeilke/packer-provisioner-inspec
    """
    resource_type = "inspec"

    props = {
        'test_path': (str, True),
        'attrs': ([str], False),
        'controls': ([str], False),
        'extra_arguments': ([str], False),
        'json_config': (str, False),
        'local_port': (str, False),
        'profiles_path': ([str], False),
        'reporter': ([str], False),
        'ssh_host_key_file': (str, False),
        'ssh_authorized_key_file': (str, False),
        'user': (str, False),
    }
