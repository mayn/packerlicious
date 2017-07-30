# Copyright (c) 2012-2017, Mark Peek <mark@peek.org>
# All rights reserved.
#
import json

from thirdparty.troposphere import AWSObject as PackerObject, encode_to_dict


class Builder(PackerObject):
    props = {
        'type2': (basestring, True),
    }



class PostProcessor(PackerObject):
    props = {}


class Provisioner(PackerObject):
    props = {}


class Variables(PackerObject):
    props = {}


class Template(object):
    """
    Packer Template Structure
    https://www.packer.io/docs/templates/index.html
    """

    props = {
        'description': (basestring, False),
        'min_packer_version': (basestring, False),
        'variables': (list, False),
        'builders': (list, True),
        'provisioners': (list, False),
        'post-processors': (list, False),
    }

    def __init__(self, description=None, min_packer_version=None):
        self.description = description
        self.min_packer_version = min_packer_version
        self.variables = list()
        self.builders = list()
        self.provisioners = list()
        self.post_processors = list()

    def add_description(self, description):
        self.description = description

    def add_min_packer_version(self, min_packer_version):
        self.min_packer_version = min_packer_version

    def handle_duplicate_key(self, key):
        raise ValueError('duplicate key "%s" detected' % key)

    def _update(self, l, values):
        if isinstance(values, list):
            l.extend(values)
        else:
            l.append(values)
        return values

    def add_variable(self, variable):
        return self._update(self.variables, variable)

    def add_builder(self, builder):
        return self._update(self.builders, builder)

    def add_provisioner(self, provisioner):
        return self._update(self.provisioners, provisioner)

    def add_post_processor(self, post_processor):
        return self._update(self.post_processors, post_processor)

    def to_dict(self):
        t = {}
        if self.description:
            t['description'] = self.description
        if self.min_packer_version:
            t['min_packer_version'] = self.min_packer_version
        if self.variables:
            t['variables'] = self.variables
        if self.provisioners:
            t['provisioners'] = self.provisioners
        if self.post_processors:
            t['post-processors'] = self.post_processors
        t['builders'] = self.builders

        return encode_to_dict(t)

    def to_json(self, indent=4, sort_keys=True, separators=(',', ': ')):
        return json.dumps(self.to_dict(), indent=indent,
                          sort_keys=sort_keys, separators=separators)

