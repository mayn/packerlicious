import validator
import warnings

from . import BasePackerObject, EnvVar, TemplateVar


class PackerProvisioner(BasePackerObject):

    def __init__(self, title=None, **kwargs):
        super(PackerProvisioner, self).__init__(title, **kwargs)


class AnsibleLocal(PackerProvisioner):
    """
    Ansible Local Provisioner
    https://www.packer.io/docs/provisioners/ansible-local.html
    TODO inventory_file validation of --limit
    """
    resource_type = "ansible-local"

    props = {
        'playbook_file': (basestring, True),
        'command': (basestring, False),
        'extra_arguments': ([basestring], False),
        'inventory_groups': (basestring, False),
        'inventory_file': (basestring, False),
        'playbook_dir': (basestring, False),
        'playbook_paths': ([basestring], False),
        'galaxy_file': (basestring, False),
        'group_vars': (basestring, False),
        'host_vars': (basestring, False),
        'role_paths': ([basestring], False),
        'staging_directory': (basestring, False),
    }


class Ansible(PackerProvisioner):
    """
    Ansible Provisioner
    https://www.packer.io/docs/provisioners/ansible.html
    """
    resource_type = "ansible"

    props = {
        'playbook_file': (basestring, True),
        'ansible_env_vars': ([basestring], False),
        'command': (basestring, False),
        'empty_groups': ([basestring], False),
        'extra_arguments': ([basestring], False),
        'groups': ([basestring], False),
        'host_alias': (basestring, False),
        'inventory_directory': (basestring, False),
        'local_port': (basestring, False),
        'sftp_command': (basestring, False),
        'skip_version_check': (validator.boolean, False),
        'ssh_host_key_file': (basestring, False),
        'ssh_authorized_key_file': (basestring, False),
        'user': (basestring, False),
    }


def valid_file_direction(x):
    if x not in [File.Upload, File.Download]:
        raise ValueError(x)
    return x


class File(PackerProvisioner):
    """
    File Provisioner
    https://www.packer.io/docs/provisioners/file.html
    """
    resource_type = "file"

    props = {
        'source': (basestring, True),
        'destination': (basestring, True),
        'direction': (valid_file_direction, True),
    }

    # File Provisioner constants
    Upload = "upload"
    Download = "download"


class SaltMasterless(PackerProvisioner):
    """
    Salt Masterless Provisioner
    https://www.packer.io/docs/provisioners/salt-masterless.html
    """
    resource_type = "salt-masterless"

    props = {
        'local_state_tree': (basestring, True),
        'bootstrap_args': (basestring, False),
        'disable_sudo': (validator.boolean, False),
        'remote_pillar_roots': (basestring, False),
        'remote_state_tree': (basestring, False),
        'local_pillar_roots': (basestring, False),
        'custom_state': (basestring, False),
        'minion_config': (basestring, False),
        'grains_file': (basestring, False),
        'skip_bootstrap': (validator.boolean, False),
        'temp_config_dir': (basestring, False),
        'no_exit_on_failure': (validator.boolean, False),
        'log_level': (basestring, False),
        'salt_call_args': (basestring, False),
        'salt_bin_dir': (basestring, False),
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
        'inline': ([basestring], False),
        'script': (basestring, False),
        'scripts': ([basestring], False),
        'binary': (validator.boolean, False),
        'environment_vars': ([basestring], False),
        'execute_command': (basestring, False),
        'expect_disconnect': (validator.boolean, False),
        'inline_shebang': (basestring, False),
        'remote_folder': (basestring, False),
        'remote_file': (basestring, False),
        'remote_path': (basestring, False),
        'skip_clean': (validator.boolean, False),
        'start_retry_timeout': (basestring, False),
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
        'command': (basestring, True),
        'execute_command': ([basestring], False),
    }
