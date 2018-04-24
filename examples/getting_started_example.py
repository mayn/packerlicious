# https://www.packer.io/intro/getting-started/build-image.html#the-template
from packerlicious import builder, Ref, Template, UserVar

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


t = Template()
t.add_variable(user_variables)
t.add_builder(builders)

print(t.to_json())
