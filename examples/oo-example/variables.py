#!/usr/bin/env python
import os

from magicdict import MagicDict
from packerlicious import UserVar

class Variables(MagicDict):
    def __init__(self):
        super(Variables, self).__init__()

        self.AnsiblePlaybookPath = UserVar(
            "AnsiblePlaybookPath",
            "/home/test/ansible",
        )

        self.AnsibleUser = UserVar(
            "AnsibleUser",
            "testuser",
        )

        self.AnsibleVaultPasswordFile = UserVar(
            "AnsibleVaultPasswordFile",
            "/home/test/staging",
        )

        self.Environment = UserVar(
            "Environment",
            "staging",
        )
        
        self.VpcId = UserVar(
            "VpcId",
            "vpc-abcd1234",
        )
        
        self.SubnetId = UserVar(
            "SubnetId",
            "subnet-abcd1234",
        )
