#!/usr/bin/env python
import os

from magicdict import MagicDict
from packervars import Mappings
from packerlicious import provisioner, Ref, Join

class Ansible(MagicDict):
    def __init__(self, variables):
        super(Ansible, self).__init__()

        packer_defaults = Mappings()

        self.AnsibleProvisioner = provisioner.Ansible(
            "AnsibleProvisioner",
            playbook_file=Join("", [Ref(variables.AnsiblePlaybookPath), "/playbook.yml"]),
            user=Ref(variables.AnsibleUser),
            ansible_env_vars=[
                "ANSIBLE_TIMEOUT=3000"
            ],
            extra_arguments=[
                "-b",
                Join("", ["-e env=", Ref(variables.Environment)]),
                Join("", ["-e vault=", Ref(variables.Environment)]),
                Join("", ["--vault-password-file=", Ref(variables.AnsibleVaultPasswordFile)]),
            ],
        )
