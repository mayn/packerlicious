# Copyright (c) 2012-2017, Mark Peek <mark@peek.org>
# All rights reserved.
#
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
import json


from thirdparty.troposphere import encode_to_dict


class Template(object):
    """
    Packer Template Structure
    https://www.packer.io/docs/templates/index.html
    """

    props = {
        'description': (str, False),
        'min_packer_version': (str, False),
        'variables': (dict, False),
        'builders': (list, True),
        'provisioners': (list, False),
        'post-processors': (list, False),
    }

    def __init__(self, description=None, min_packer_version=None):
        self.description = description
        self.min_packer_version = min_packer_version
        self.variables = dict()
        self.builders = list()
        self.provisioners = list()
        self.post_processors = list()

    def add_description(self, description):
        self.description = description

    def add_min_packer_version(self, min_packer_version):
        self.min_packer_version = min_packer_version

    def handle_duplicate_key(self, key):
        raise ValueError('duplicate key "%s" detected' % key)

    def _update(self, c, values):
        if isinstance(c, list):
            if isinstance(values, list):
                c.extend(values)
            else:
                c.append(values)
        elif isinstance(c, dict): # pragma: no branch
            if isinstance(values, list):
                for v in values:
                    if v.title in c:
                        self.handle_duplicate_key(v.title)
                    c[v.title] = v
            else:
                if values.title in c:
                    self.handle_duplicate_key(values.title)
                c[values.title] = values
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
        if self.builders:
            t['builders'] = self.builders
        if self.provisioners:
            t['provisioners'] = self.provisioners
        if self.post_processors:
            t['post-processors'] = self.post_processors
        if self.variables:
            t['variables'] = self.variables

        return encode_to_dict(t)

    def to_json(self, indent=2, sort_keys=True, separators=(',', ': ')):
        return json.dumps(self.to_dict(), indent=indent,
                          sort_keys=sort_keys, separators=separators)
