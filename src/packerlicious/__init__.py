from thirdparty.troposphere import AWSHelperFn
from thirdparty.troposphere import AWSProperty as PackerProperty
from thirdparty.troposphere import BaseAWSObject as BasePackerObject

from template import Template

__version__ = "0.2.0"

class Ref(AWSHelperFn):
    def __init__(self, data):
        if isinstance(data, EnvVar):
            self.data = "{{env `%s`}}" % data
        elif isinstance(data, TemplateVar):
            self.data = "`{{.%s}}`" % data
        elif isinstance(data, UserVar):
            self.data = "{{user `%s`}}" % data.title
        else:
            self.data = self.getdata(data)


class PackerVariable(AWSHelperFn):
    def __init__(self, data):
        self.data = self.getdata(data)

    def ref(self):
        return Ref(self)

    Ref = ref


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
    variable_type = "user"

    def __init__(self, name, default_value=""):
        self.title = name
        self.data = self.getdata(default_value)


class EnvVar(UserVar):
    """
    Environment Variables
    https://www.packer.io/docs/templates/user-variables.html#environment-variables
    """

    variable_type = "env"

    def __init__(self, data):
        self.data = self.getdata(data)
