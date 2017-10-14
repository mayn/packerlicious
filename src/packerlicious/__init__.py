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
from thirdparty.troposphere import AWSHelperFn
from thirdparty.troposphere import AWSProperty as PackerProperty
from thirdparty.troposphere import BaseAWSObject as BasePackerObject

from .template import Template
from .version import __version__ as version

__version__ = version


class Ref(AWSHelperFn):
    def __init__(self, data):
        if isinstance(data, EnvVar):
            self.data = "{{env `%s`}}" % data.data
        elif isinstance(data, TemplateVar):
            self.data = "{{.%s}}" % data.data
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

    def __init__(self, name, default_value=""):
        self.title = name
        self.data = self.getdata(default_value)


class EnvVar(PackerVariable):
    """
    Environment Variables
    https://www.packer.io/docs/templates/user-variables.html#environment-variables
    """

    def __init__(self, data):
        self.data = self.getdata(data)
