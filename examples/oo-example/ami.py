#!/usr/bin/env python
import os

from magicdict import MagicDict
from packervars import Mappings
from packerlicious import builder, Ref, Join

class Ami(MagicDict):
    def __init__(self, variables):
        super(Ami, self).__init__()

        packer_defaults = Mappings()


        self.BaselineAMI = builder.AmazonEbs(
            "BaselineAMI",
            associate_public_ip_address=True,
            ami_name="packer_baseline_ami_{{ isotime \"2006_01_02_03_04\" }}",
            ami_regions=packer_defaults.ec2_regions,
            instance_type=packer_defaults.default_build_instance_type,
            profile=os.getenv("AWS_PROFILE", "default"),
            region=packer_defaults.default_ec2_region,
            run_tags=dict(
                Name="packer_baseline_ami_{{ isotime \"2006_01_02_03_04\" }}",
            ),
            source_ami_filter=builder.AmazonSourceAmiFilter(
                filters={
                    "virtualization-type": "hvm",
                    "name": "CentOS Linux 7 x86_64 HVM EBS *",
                    "root-device-type": "ebs",
                    "architecture": "x86_64",
                },
                owners=[packer_defaults.centos_aws_owner_id],
                most_recent=True,
            ),
            ssh_username="centos",
            subnet_id=Ref(variables.SubnetId),
            tags=dict(
                OS_Version="CentOS",
                Release="Latest",
                Base_AMI_Name="{{ .SourceAMIName }}",
                Owner="packer",
                Environment=Ref(variables.Environment),
                Name="packer_baseline_ami_{{ isotime \"2006_01_02_03_04\" }}",
            ),
            vpc_id=Ref(variables.VpcId),
        )
