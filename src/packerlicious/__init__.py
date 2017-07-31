from thirdparty.troposphere import AWSHelperFn
from thirdparty.troposphere import AWSProperty as PackerProperty
from thirdparty.troposphere import BaseAWSObject as BasePackerObject

from template import Template


class PackerVariable(AWSHelperFn):
    def __init__(self, data):
        self.data = self.getdata(data)


# TODO finish variable implementation
class TemplateVar(PackerVariable):
    """
    Template Variables
    https://www.packer.io/docs/templates/engine.html#template-variables
    """
    def __init__(self, data):
        self.data = self.getdata(data)


class UserVar(PackerVariable):
    """
    User Variables
    https://www.packer.io/docs/templates/user-variables.html
    """
    def __init__(self, data):
        self.data = self.getdata(data)


class EnvVar(UserVar):
    """
    Environment Variables
    https://www.packer.io/docs/templates/user-variables.html#environment-variables
    """
    def __init__(self, data):
        self.data = self.getdata(data)
