from packerlicious import builder, provisioner, Template
from variables import Variables
from ami import Ami
from ansible import Ansible


class Stack(object):
    def __init__(self):
        self.template = Template()

        variables = Variables()
        ami = Ami(variables=variables)
        ansible = Ansible(variables=variables)

        for var in variables.values():
            self.template.add_variable(var)

        for builder in ami.values():
            self.template.add_builder(builder)

        for provisioner in ansible.values():
            self.template.add_provisioner(provisioner)
