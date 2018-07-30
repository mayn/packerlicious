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


from . import BasePackerObject, PackerProperty, EnvVar, TemplateVar, validator

# guest_os_type options for Chef and Puppet
UNIX = "unix"
WINDOWS = "windows"


class PackerProvisioner(BasePackerObject):
    """
    packer provisioner
    https://www.packer.io/docs/templates/provisioners.html
    TODO attribute validation
    """
    provisioner_props = {
        'pause_before': (str, False),
        'only': ([str], False),
        'except': ([str], False),
    }

    def __init__(self, title=None, **kwargs):

        for k, v in list(self.provisioner_props.items()):
            self.props[k] = v
        super(PackerProvisioner, self).__init__(title, **kwargs)


class AnsibleLocal(PackerProvisioner):
    """
    Ansible Local Provisioner
    https://www.packer.io/docs/provisioners/ansible-local.html
    TODO inventory_file validation of --limit
    """
    resource_type = "ansible-local"

    props = {
        'playbook_file': (str, False),
        'playbook_files': ([str], False),
        'clean_staging_directory': (validator.boolean, False),
        'command': (str, False),
        'extra_arguments': ([str], False),
        'inventory_groups': (str, False),
        'inventory_file': (str, False),
        'playbook_dir': (str, False),
        'playbook_paths': ([str], False),
        'galaxy_file': (str, False),
        'group_vars': (str, False),
        'host_vars': (str, False),
        'role_paths': ([str], False),
        'staging_directory': (str, False),
    }

    def validate(self):
        conds = [
            'playbook_file',
            'playbook_files',
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)


class Ansible(PackerProvisioner):
    """
    Ansible Provisioner
    https://www.packer.io/docs/provisioners/ansible.html
    """
    resource_type = "ansible"

    props = {
        'playbook_file': (str, True),
        'ansible_env_vars': ([str], False),
        'command': (str, False),
        'empty_groups': ([str], False),
        'extra_arguments': ([str], False),
        'groups': ([str], False),
        'host_alias': (str, False),
        'inventory_file': (str, False),
        'inventory_directory': (str, False),
        'local_port': (str, False),
        'sftp_command': (str, False),
        'skip_version_check': (validator.boolean, False),
        'ssh_host_key_file': (str, False),
        'ssh_authorized_key_file': (str, False),
        'user': (str, False),
    }


class ChefClient(PackerProvisioner):
    """
    Chef Client Provisioner
    https://www.packer.io/docs/provisioners/chef-client.html
    """
    resource_type = "chef-client"

    props = {
        'chef_environment': (str, False),
        'config_template': (str, False),
        'encrypted_data_bag_secret_path': (str, False),
        'execute_command': (str, False),
        'guest_os_type': (validator.string_list_item([UNIX, WINDOWS]), False),
        'install_command': (str, False),
        'json': (str, False),
        'knife_command': (str, False),
        'node_name': (str, False),
        'policy_group': (str, False),
        'policy_name': (str, False),
        'prevent_sudo': (validator.boolean, False),
        'run_list': ([str], False),
        'server_url': (str, False),
        'skip_clean_client': (validator.boolean, False),
        'skip_clean_node': (validator.boolean, False),
        'skip_clean_staging_directory': (validator.boolean, False),
        'skip_install': (validator.boolean, False),
        'staging_directory': (str, False),
        'trusted_certs_dir': (str, False),
        'client_key': (str, False),
        'validation_client_name': (str, False),
        'validation_key_path': (str, False),
    }


class ChefSolo(PackerProvisioner):
    """
    Chef Solo Provisioner
    https://www.packer.io/docs/provisioners/chef-solo.html
    """
    resource_type = "chef-solo"

    props = {
        'chef_environment': (str, False),
        'config_template': (str, False),
        'cookbook_paths': (str, False),
        'data_bags_path': (str, False),
        'encrypted_data_bag_secret_path': (str, False),
        'environments_path': (str, False),
        'execute_command': (str, False),
        'guest_os_type': (validator.string_list_item([UNIX, WINDOWS]), False),
        'install_command': (str, False),
        'json': (str, False),
        'prevent_sudo': (validator.boolean, False),
        'remote_cookbook_paths': ([str], False),
        'roles_path': (str, False),
        'run_list': ([str], False),
        'skip_install': (validator.boolean, False),
        'staging_directory': (str, False),
        'version': (str, False),
    }


class ModuleDirectory(PackerProperty):
    """
    https://www.packer.io/docs/provisioners/converge.html#module-directories
    """
    props = {
        'source': (str, True),
        'destination': (str, True),
        'exclude': ([str], False),
    }


class Converge(PackerProvisioner):
    """
    Converge Provisioner
    https://www.packer.io/docs/provisioners/converge.html
    """
    resource_type = "converge"

    # Converge Template Variables
    WorkingDirectory = TemplateVar("WorkingDirectory")
    Sudo = TemplateVar("Sudo")
    ParamsJSON = TemplateVar("ParamsJSON")
    Module = TemplateVar("Module")
    Version = TemplateVar("Version")

    props = {
        'module': (str, True),
        'bootstrap': (validator.boolean, False),
        'bootstrap_command': (str, False),
        'execute_command': (str, False),
        'module_dirs': ([ModuleDirectory], False),
        'params': (dict, False),
        'prevent_bootstrap_sudo': (validator.boolean, False),
        'prevent_sudo': (validator.boolean, False),
        'version': (str, False),
        'working_directory': (str, False),
    }


class File(PackerProvisioner):
    """
    File Provisioner
    https://www.packer.io/docs/provisioners/file.html
    """
    resource_type = "file"

    # File Provisioner constants
    Upload = "upload"
    Download = "download"

    props = {
        'source': (str, True),
        'destination': (str, True),
        'direction': (validator.string_list_item([Upload, Download]), True),
        'generated': (validator.boolean, False),
    }


class PowerShell(PackerProvisioner):
    """
    PowerShell Provisioner
    https://www.packer.io/docs/provisioners/powershell.html
    """
    resource_type = "powershell"

    # PowerShell Template Variables
    Path = TemplateVar("Path")
    Vars = TemplateVar("Vars")

    # PowerShell Environment Variables
    PackerBuildName = EnvVar("PACKER_BUILD_NAME")
    PackerBuilderType = EnvVar("PACKER_BUILDER_TYPE")
    PackerHttpAddr = EnvVar("PACKER_HTTP_ADDR")

    props = {
        'inline': ([str], False),
        'script': (str, False),
        'scripts': ([str], False),
        'binary': (validator.boolean, False),
        'environment_vars': ([str], False),
        'execute_command': (str, False),
        'elevated_user': (str, False),
        'elevated_password': (str, False),
        'remote_path': (str, False),
        'remote_env_var_path': (str, False),
        'skip_clean': (validator.boolean, False),
        'start_retry_timeout': (str, False),
        'valid_exit_codes': ([int], False),
    }

    def validate(self):
        conds = [
            'inline',
            'script',
            'scripts'
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)


class PuppetMasterless(PackerProvisioner):
    """
    Puppet Masterless
    https://www.packer.io/docs/provisioners/puppet-server.html
    """
    resource_type = "puppet-masterless"

    props = {
        'manifest_file': (str, True),
        'execute_command': (str, False),
        'extra_arguments': ([str], False),
        'guest_os_type': (validator.string_list_item([UNIX, WINDOWS]), False),
        'facter': (dict, False),
        'hiera_config_path': (str, False),
        'ignore_exit_codes': (validator.boolean, False),
        'manifest_dir': (str, False),
        'module_paths': ([str], False),
        'prevent_sudo': (validator.boolean, False),
        'puppet_bin_dir': (str, False),
        'staging_directory': (str, False),
        'working_directory': (str, False),
    }


class PuppetServer(PackerProvisioner):
    """
    Puppet Server
    https://www.packer.io/docs/provisioners/puppet-server.html
    """
    resource_type = "puppet-server"

    props = {
        'client_cert_path': (str, False),
        'client_private_key_path': (str, False),
        'execute_command': (str, False),
        'facter': (dict, False),
        'guest_os_type': (validator.string_list_item([UNIX, WINDOWS]), False),
        'ignore_exit_codes': (validator.boolean, False),
        'options': (str, False),
        'prevent_sudo': (validator.boolean, False),
        'puppet_bin_dir': (str, False),
        'puppet_node': (str, False),
        'puppet_server': (str, False),
        'staging_dir': (str, False),
        'working_directory': (str, False),
    }


class SaltMasterless(PackerProvisioner):
    """
    Salt Masterless Provisioner
    https://www.packer.io/docs/provisioners/salt-masterless.html
    """
    resource_type = "salt-masterless"

    props = {
        'local_state_tree': (str, True),
        'bootstrap_args': (str, False),
        'disable_sudo': (validator.boolean, False),
        'remote_pillar_roots': (str, False),
        'remote_state_tree': (str, False),
        'local_pillar_roots': (str, False),
        'custom_state': (str, False),
        'minion_config': (str, False),
        'grains_file': (str, False),
        'guest_os_type': (validator.string_list_item([UNIX, WINDOWS]), False),
        'skip_bootstrap': (validator.boolean, False),
        'temp_config_dir': (str, False),
        'no_exit_on_failure': (validator.boolean, False),
        'log_level': (str, False),
        'salt_call_args': (str, False),
        'salt_bin_dir': (str, False),
    }

    def validate(self):
        conds = [
            'remote_pillar_roots',
            'remote_state_tree',
            ]

        if 'minion_config' in self.properties and validator.count(self.properties, conds) > 0:
            # TODO should this just be an error?
            warnings.warn("'minion_config' is present, 'remote_pillar_roots' and 'remote_state_tree' will be ignored.")


class Shell(PackerProvisioner):
    """
    Shell Provisioner
    https://www.packer.io/docs/provisioners/shell.html
    """
    resource_type = "shell"

    # Shell Local Template Variables
    Path = TemplateVar("Path")
    Vars = TemplateVar("Vars")

    # Shell Local Environment Variables
    PackerBuildName = EnvVar("PACKER_BUILD_NAME")
    PackerBuilderType = EnvVar("PACKER_BUILDER_TYPE")
    PackerHttpAddr = EnvVar("PACKER_HTTP_ADDR")

    props = {
        'inline': ([str], False),
        'script': (str, False),
        'scripts': ([str], False),
        'binary': (validator.boolean, False),
        'environment_vars': ([str], False),
        'execute_command': (str, False),
        'expect_disconnect': (validator.boolean, False),
        'inline_shebang': (str, False),
        'remote_folder': (str, False),
        'remote_file': (str, False),
        'remote_path': (str, False),
        'skip_clean': (validator.boolean, False),
        'start_retry_timeout': (str, False),
    }

    def validate(self):
        conds = [
            'inline',
            'script',
            'scripts'
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)


class ShellLocal(PackerProvisioner):
    """
    Shell Local Provisioner
    https://www.packer.io/docs/provisioners/shell-local.html
    """
    resource_type = "shell-local"

    # Shell Local Template Variables
    Command = TemplateVar("Command")

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
            'scripts'
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)


class WindowsShell(PackerProvisioner):
    """
    Windows Shell Provisioner
    https://www.packer.io/docs/provisioners/windows-shell.html
    """
    resource_type = "windows-local"

    # Windows Shell Template Variables
    Vars = TemplateVar("Vars")
    Path = TemplateVar("Path")

    props = {
        'inline': ([str], False),
        'script': (str, False),
        'scripts': ([str], False),
        'binary': (validator.boolean, False),
        'environment_vars': ([str], False),
        'execute_command': (str, False),
        'remote_path': (str, False),
        'start_retry_timeout': (str, False),
    }

    def validate(self):
        conds = [
            'inline',
            'script',
            'scripts'
        ]
        validator.exactly_one(self.__class__.__name__, self.properties, conds)


class WindowsRestart(PackerProvisioner):
    """
    Windows Restart Provisioner
    https://www.packer.io/docs/provisioners/windows-restart.html
    """
    resource_type = "windows-restart"

    props = {
        'restart_command': (str, False),
        'restart_check_command': (str, False),
        'restart_timeout': (str, False),
    }
