# Copyright (c) 2012-2017, Mark Peek <mark@peek.org>
# All rights reserved.
#


class Template(object):
    props = {
        'AWSTemplateFormatVersion': (basestring, False),
        'Transform': (basestring, False),
        'Description': (basestring, False),
        'Parameters': (dict, False),
        'Mappings': (dict, False),
        'Resources': (dict, False),
        'Outputs': (dict, False),
    }

    def __init__(self, Description=None, Metadata=None):  # noqa: N803
        self.description = Description
        self.metadata = {} if Metadata is None else Metadata
        self.conditions = {}
        self.mappings = {}
        self.outputs = {}
        self.parameters = {}
        self.resources = {}
        self.version = None
        self.transform = None

    def add_description(self, description):
        self.description = description

    def add_metadata(self, metadata):
        self.metadata = metadata

    def add_condition(self, name, condition):
        self.conditions[name] = condition

    def handle_duplicate_key(self, key):
        raise ValueError('duplicate key "%s" detected' % key)

    def _update(self, d, values):
        if isinstance(values, list):
            for v in values:
                if v.title in d:
                    self.handle_duplicate_key(v.title)
                d[v.title] = v
        else:
            if values.title in d:
                self.handle_duplicate_key(values.title)
            d[values.title] = values
        return values

    def add_output(self, output):
        if len(self.outputs) >= MAX_OUTPUTS:
            raise ValueError('Maximum outputs %d reached' % MAX_OUTPUTS)
        return self._update(self.outputs, output)

    def add_mapping(self, name, mapping):
        if len(self.mappings) >= MAX_MAPPINGS:
            raise ValueError('Maximum mappings %d reached' % MAX_MAPPINGS)
        self.mappings[name] = mapping

    def add_parameter(self, parameter):
        if len(self.parameters) >= MAX_PARAMETERS:
            raise ValueError('Maximum parameters %d reached' % MAX_PARAMETERS)
        return self._update(self.parameters, parameter)

    def add_resource(self, resource):
        if len(self.resources) >= MAX_RESOURCES:
            raise ValueError('Maximum number of resources %d reached'
                             % MAX_RESOURCES)
        return self._update(self.resources, resource)

    def add_version(self, version=None):
        if version:
            self.version = version
        else:
            self.version = "2010-09-09"

    def add_transform(self, transform):
        self.transform = transform

    def to_dict(self):
        t = {}
        if self.description:
            t['Description'] = self.description
        if self.metadata:
            t['Metadata'] = self.metadata
        if self.conditions:
            t['Conditions'] = self.conditions
        if self.mappings:
            t['Mappings'] = self.mappings
        if self.outputs:
            t['Outputs'] = self.outputs
        if self.parameters:
            t['Parameters'] = self.parameters
        if self.version:
            t['AWSTemplateFormatVersion'] = self.version
        if self.transform:
            t['Transform'] = self.transform
        t['Resources'] = self.resources

        return encode_to_dict(t)

    def to_json(self, indent=4, sort_keys=True, separators=(',', ': ')):
        return json.dumps(self.to_dict(), indent=indent,
                          sort_keys=sort_keys, separators=separators)

    def to_yaml(self):
        return cfn_flip.to_yaml(self.to_json())
