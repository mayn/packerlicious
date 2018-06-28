import boto3

class Mappings:
    def __init__(self):
        self.default_ec2_region = "ap-southeast-2"
        self.ec2_regions = ["ap-southeast-2", "eu-central-1"]

        self.default_build_instance_type = "t2.medium"

        self.centos_aws_owner_id = "679593333241"

    def latest_centos_ami(self):
        EC2 = boto3.client('ec2', region_name=self.default_ec2_region)
        response = EC2.describe_images(
            Owners=[self.centos_aws_owner_id], # CentOS Owner ID
            Filters=[
              {'Name': 'name', 'Values': ['CentOS Linux 7 x86_64 HVM EBS *']},
              {'Name': 'architecture', 'Values': ['x86_64']},
              {'Name': 'root-device-type', 'Values': ['ebs']},
            ],  
        )   

        amis = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
        return str(amis[0]['ImageId'])
