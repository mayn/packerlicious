# Copyright (c) 2012-2017, Mark Peek <mark@peek.org>
# All rights reserved.
#
# See LICENSE file for full license.


from future import standard_library
standard_library.install_aliases()
from future.utils import native
from collections import OrderedDict
import json
import re
import sys
import types


__version__ = "1.9.4"

# Template Limits
MAX_MAPPINGS = 100
MAX_OUTPUTS = 60
MAX_PARAMETERS = 60
MAX_RESOURCES = 200
PARAMETER_TITLE_MAX = 255

valid_names = re.compile(r'^[a-zA-Z0-9]+$')


def is_aws_object_subclass(cls):
    is_aws_object = False
    try:
        is_aws_object = issubclass(cls, BaseAWSObject)
    # prop_type isn't a class
    except TypeError:
        pass
    return is_aws_object


def encode_to_dict(obj):
    if hasattr(obj, 'to_dict'):
        # Calling encode_to_dict to ensure object is
        # normalized to a base dictionary all the way down.
        return encode_to_dict(obj.to_dict())
    elif isinstance(obj, (list, tuple)):
        new_lst = []
        for o in list(obj):
            new_lst.append(encode_to_dict(o))
        return new_lst
    elif isinstance(obj, dict):
        props = OrderedDict()
        for name, prop in list(obj.items()):
            props[name] = encode_to_dict(prop)

        return props
    # This is useful when dealing with external libs using
    # this format. Specifically awacs.
    elif hasattr(obj, 'JSONrepr'):
        return encode_to_dict(obj.JSONrepr())
    return obj


class BaseAWSObject(object):
    def __init__(self, title, template=None, **kwargs):
        self.title = title
        self.template = template
        # Cache the keys for validity checks
        self.propnames = list(self.props.keys())
        self.attributes = ['DependsOn', 'DeletionPolicy',
                           'Metadata', 'UpdatePolicy',
                           'Condition', 'CreationPolicy']

        # try to validate the title if its there
        if self.title:
            self.validate_title()

        # Create the list of properties set on this object by the user
        self.properties = OrderedDict()
        dictname = getattr(self, 'dictname', None)
        if dictname:
            self.resource = {
                dictname: self.properties,
            }
        else:
            self.resource = self.properties
        if hasattr(self, 'resource_type') and self.resource_type is not None:
            self.resource['type'] = self.resource_type
        self.__initialized = True

        # Check for properties defined in the class
        for k, (_, required) in list(self.props.items()):
            v = getattr(type(self), k, None)
            if v is not None and k not in kwargs:
                self.__setattr__(k, v)

        # Now that it is initialized, populate it with the kwargs
        for k, v in list(kwargs.items()):
            self.__setattr__(k, v)

        # Bound it to template if we know it
        if self.template is not None:
            self.template.add_resource(self)

    def __getattr__(self, name):
        try:
            if name in self.attributes:
                return self.resource[name]
            else:
                return self.properties.__getitem__(name)
        except KeyError:
            # Fall back to the name attribute in the object rather than
            # in the properties dict. This is for non-OpenStack backwards
            # compatibility since OpenStack objects use a "name" property.
            if name == 'name':
                return self.__getattribute__('title')
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in list(self.__dict__.keys()) \
                or '_BaseAWSObject__initialized' not in self.__dict__:
            return dict.__setattr__(self, name, value)
        elif name in self.attributes:
            self.resource[name] = value
            return None
        elif name in self.propnames:
            # Check the type of the object and compare against what we were
            # expecting.
            expected_type = self.props[name][0]

            # If the value is a AWSHelperFn we can't do much validation
            # we'll have to leave that to Amazon.  Maybe there's another way
            # to deal with this that we'll come up with eventually.
            # We'll do validation below if there are AWSHelperFn in a
            # list context.
            if isinstance(value, AWSHelperFn) and \
                    not isinstance(expected_type, list):
                return self.properties.__setitem__(name, value)

            # If it's a function, call it...
            elif isinstance(expected_type, types.FunctionType):
                try:
                    value = expected_type(value)
                except Exception:
                    # TODO fix this, title is none. ie. output = None.method function validator
                    sys.stderr.write(
                        "%s: %s.%s function validator '%s' threw "
                        "exception:\n" % (self.__class__,
                                          self.title,
                                          name,
                                          expected_type.__name__))
                    raise
                return self.properties.__setitem__(name, value)

            # If it's a list of types, check against those types...
            elif isinstance(expected_type, list):
                # If we're expecting a list, then make sure it is a list
                if not isinstance(value, list):
                    self._raise_type(name, value, expected_type)

                # Iterate over the list and make sure it matches our
                # type checks (as above accept AWSHelperFn because
                # we can't do the validation ourselves)
                for v in value:
                    if not isinstance(v, tuple(expected_type)) \
                       and not isinstance(v, AWSHelperFn):
                        self._raise_type(name, v, expected_type)
                # Validated so assign it
                return self.properties.__setitem__(name, value)

            # Final validity check, compare the type of value against
            # expected_type which should now be either a single type or
            # a tuple of types.
            elif isinstance(value, expected_type):
                return self.properties.__setitem__(name, value)
            else:
                self._raise_type(name, value, expected_type)

        type_name = getattr(self, 'resource_type', self.__class__.__name__)

        if type_name == 'AWS::CloudFormation::CustomResource' or \
                type_name.startswith('Custom::'):
            # Add custom resource arguments to the dict without any further
            # validation. The properties of a CustomResource is not known.
            return self.properties.__setitem__(name, value)

        raise AttributeError("%s object does not support attribute %s" %
                             (type_name, name))

    def _raise_type(self, name, value, expected_type):
        raise TypeError('%s: %s.%s is %s, expected %s' % (self.__class__,
                                                          self.title,
                                                          name,
                                                          type(value),
                                                          expected_type))

    def validate_title(self):
        if not valid_names.match(self.title):
            raise ValueError('Name "%s" not alphanumeric' % self.title)

    def validate(self):
        pass

    def to_dict(self):
        self._validate_props()
        self.validate()

        if self.properties:
            return encode_to_dict(self.resource)
        elif hasattr(self, 'resource_type'):
            d = {}
            for k, v in list(self.resource.items()):
                if k != 'Properties':
                    d[k] = v
            return d
        else:
            return {}

    @classmethod
    def _from_dict(cls, title=None, **kwargs):
        props = {}
        for prop_name, value in list(kwargs.items()):
            try:
                prop_attrs = cls.props[prop_name]
            except KeyError:
                raise AttributeError("Object type %s does not have a "
                                     "%s property." % (cls.__name__,
                                                       prop_name))
            prop_type = prop_attrs[0]
            value = kwargs[prop_name]
            is_aws_object = is_aws_object_subclass(prop_type)
            if is_aws_object:
                if not isinstance(value, collections.Mapping):
                    raise ValueError("Property definition for %s must be "
                                     "a Mapping type" % prop_name)
                value = prop_type._from_dict(**value)

            if isinstance(prop_type, list):
                if not isinstance(value, list):
                    raise TypeError("Attribute %s must be a "
                                    "list." % prop_name)
                new_value = []
                for v in value:
                    new_v = v
                    if is_aws_object_subclass(prop_type[0]):
                        if not isinstance(v, collections.Mapping):
                            raise ValueError(
                                "Property definition for %s must be "
                                "a list of Mapping types" % prop_name)
                        new_v = prop_type[0]._from_dict(**v)
                    new_value.append(new_v)
                value = new_value
            props[prop_name] = value
        if title:
            return cls(title, **props)
        return cls(**props)

    @classmethod
    def from_dict(cls, title, d):
        return cls._from_dict(title, **d)

    def _validate_props(self):
        for k, (_, required) in list(self.props.items()):
            if required and k not in self.properties:
                rtype = getattr(self, 'resource_type', "<unknown type>")
                title = getattr(self, 'title')
                msg = "Resource %s required in type %s" % (k, rtype)
                if title:
                    msg += " (title: %s)" % title
                raise ValueError(msg)


class AWSObject(BaseAWSObject):
    # dictname = 'Properties'

    def ref(self):
        return Ref(self)

    Ref = ref

    def get_att(self, value):
        return GetAtt(self, value)

    GetAtt = get_att


class AWSDeclaration(BaseAWSObject):
    """
    Used for CloudFormation Resource Property objects
    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/
    aws-product-property-reference.html
    """

    def __init__(self, title, **kwargs):
        super(AWSDeclaration, self).__init__(title, **kwargs)


class AWSProperty(BaseAWSObject):
    """
    Used for CloudFormation Resource Property objects
    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/
    aws-product-property-reference.html
    """
    dictname = None

    def __init__(self, title=None, **kwargs):
        super(AWSProperty, self).__init__(title, **kwargs)


class AWSAttribute(BaseAWSObject):
    dictname = None

    """
    Used for CloudFormation Resource Attribute objects
    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/
    aws-product-attribute-reference.html
    """

    def __init__(self, title=None, **kwargs):
        super(AWSAttribute, self).__init__(title, **kwargs)


def validate_delimiter(delimiter):
    if not isinstance(delimiter, str):
        raise ValueError(
            "Delimiter must be a String, %s provided" % type(delimiter)
        )


class AWSHelperFn(object):
    def getdata(self, data):
        if isinstance(data, BaseAWSObject):
            return data.title
        else:
            return data

    def to_dict(self):
        return encode_to_dict(self.data)


class GenericHelperFn(AWSHelperFn):
    """ Used as a fallback for the template generator """
    def __init__(self, data):
        self.data = self.getdata(data)

    def to_dict(self):
        return encode_to_dict(self.data)


class Ref(AWSHelperFn):
    def __init__(self, data):
        self.data = {'Ref': self.getdata(data)}


class Parameter(AWSDeclaration):
    STRING_PROPERTIES = ['AllowedPattern', 'MaxLength', 'MinLength']
    NUMBER_PROPERTIES = ['MaxValue', 'MinValue']
    props = {
        'Type': (str, True),
        'Default': ((str, int, float), False),
        'NoEcho': (bool, False),
        'AllowedValues': (list, False),
        'AllowedPattern': (str, False),
        # 'MaxLength': (validators.positive_integer, False),
        # 'MinLength': (validators.positive_integer, False),
        # 'MaxValue': (validators.integer, False),
        # 'MinValue': (validators.integer, False),
        'Description': (str, False),
        'ConstraintDescription': (str, False),
    }

    def validate_title(self):
        if len(self.title) > PARAMETER_TITLE_MAX:
            raise ValueError("Parameter title can be no longer than "
                             "%d characters" % PARAMETER_TITLE_MAX)
        super(Parameter, self).validate_title()

    def validate(self):
        def check_type(t, v):
            try:
                t(v)
                return True
            except ValueError:
                return False

        # Validate the Default parameter value
        default = self.properties.get('Default')
        if default:
            error_str = ("Parameter default type mismatch: expecting "
                         "type %s got %s with value %r")
            # Get the Type specified and see whether the default type
            # matches (in the case of a String Type) or can be coerced
            # into one of the number formats.
            param_type = self.properties.get('Type')
            if param_type == 'String' and not isinstance(default, str):
                raise ValueError(error_str %
                                 ('String', type(default), default))
            elif param_type == 'Number':
                allowed = [float, int]
                # See if the default value can be coerced into one
                # of the correct types
                if not any([check_type(x, default) for x in allowed]):
                    raise ValueError(error_str %
                                     (param_type, type(default), default))
            elif param_type == 'List<Number>':
                if not isinstance(default, str):
                    raise ValueError(error_str %
                                     (param_type, type(default), default))
                allowed = [float, int]
                dlist = default.split(",")
                for d in dlist:
                    # Verify the split array are all numbers
                    if not any([check_type(x, d) for x in allowed]):
                        raise ValueError(error_str %
                                         (param_type, type(d), dlist))

        if self.properties['Type'] != 'String':
            for p in self.STRING_PROPERTIES:
                if p in self.properties:
                    raise ValueError("%s can only be used with parameters of "
                                     "the String type." % p)
        if self.properties['Type'] != 'Number':
            for p in self.NUMBER_PROPERTIES:
                if p in self.properties:
                    raise ValueError("%s can only be used with parameters of "
                                     "the Number type." % p)
