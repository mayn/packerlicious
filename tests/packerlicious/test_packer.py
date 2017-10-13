import pytest
import unittest

from packerlicious import packer
from packerlicious import builder, Ref, Template, UserVar

class TestPacker(unittest.TestCase):

    aws_access_key = UserVar("aws_access_key", "")
    aws_secret_key = UserVar("aws_secret_key", "")
    user_variables = [
        aws_access_key,
        aws_secret_key
    ]
    builders = [
        builder.AmazonEbs(
            access_key=Ref(aws_access_key),
            secret_key=Ref(aws_secret_key),
            region="us-east-1",
            source_ami_filter=builder.AmazonSourceAmiFilter(
                filters={
                    "virtualization-type": "hvm",
                    "name": "*ubuntu-xenial-16.04-amd64-server-*",
                    "root-device-type": "ebs"
                },
                owners=["099720109477"],
                most_recent=True
            ),
            instance_type="t2.micro",
            ami_name="packer-example {{timestamp}}",
            ssh_username="ubuntu"
        )
    ]
    template = Template()
    template.add_variable(user_variables)
    template.add_builder(builders)

    def test_validate(self):
        output = packer.validate(TestPacker.template)
        assert output.return_code == 0
        assert "successfully" in output.output

    def test_build(self):
        output = packer.build(TestPacker.template)
        assert output.return_code == 0
        assert "successful" in output.output

    def test_inspect(self):
        output = packer.inspect(TestPacker.template)
        assert output.return_code == 0

if __name__ == '__main__':
    unittest.main()