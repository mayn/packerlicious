# Copyright (c) 2012-2013, Mark Peek <mark@peek.org>
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
from re import compile


def boolean(x):
    if x in [True, 1, '1', 'true', 'True']:
        return "true"
    if x in [False, 0, '0', 'false', 'False']:
        return "false"
    raise ValueError


def integer(x):
    try:
        int(x)
    except (ValueError, TypeError):
        raise ValueError("%r is not a valid integer" % x)
    else:
        return x


def integer_range(minimum_val, maximum_val):
    def integer_range_checker(x):
        i = int(x)
        if i < minimum_val or i > maximum_val:
            raise ValueError('Integer must be between %d and %d' % (
                minimum_val, maximum_val))
        return x

    return integer_range_checker


def network_port(x):
    from thirdparty.troposphere import AWSHelperFn

    # Network ports can be Ref items
    if isinstance(x, AWSHelperFn):
        return x

    i = integer(x)
    if int(i) < -1 or int(i) > 65535:
        raise ValueError("network port %r must been between 0 and 65535" % i)
    return x


def tg_healthcheck_port(x):
    if isinstance(x, str) and x == "traffic-port":
        return x
    return network_port(x)


def s3_bucket_name(b):

    # consecutive periods not allowed

    if '..' in b:
        raise ValueError("%s is not a valid s3 bucket name" % b)

    # IP addresses not allowed

    ip_re = compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if ip_re.match(b):
        raise ValueError("%s is not a valid s3 bucket name" % b)

    s3_bucket_name_re = compile(r'^[a-z\d][a-z\d\.-]{1,61}[a-z\d]$')
    if s3_bucket_name_re.match(b):
        return b
    else:
        raise ValueError("%s is not a valid s3 bucket name" % b)


def elb_name(b):
    elb_name_re = compile(r'^[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,30}[a-zA-Z0-9]{1})?$')  # noqa
    if elb_name_re.match(b):
        return b
    else:
        raise ValueError("%s is not a valid elb name" % b)


def encoding(encoding):
    valid_encodings = ['plain', 'base64']
    if encoding not in valid_encodings:
        raise ValueError('Encoding needs to be one of %r' % valid_encodings)
    return encoding


def status(status):
    valid_statuses = ['Active', 'Inactive']
    if status not in valid_statuses:
        raise ValueError('Status needs to be one of %r' % valid_statuses)
    return status


def iam_names(b):
    iam_name_re = compile(r'^[a-zA-Z0-9_\.\+\=\@\-\,]+$')
    if iam_name_re.match(b):
        return b
    else:
        raise ValueError("%s is not a valid iam name" % b)


def iam_user_name(user_name):
    if not user_name:
        raise ValueError(
            "AWS::IAM::User property 'UserName' may not be empty")

    if len(user_name) > 64:
        raise ValueError(
            "AWS::IAM::User property 'UserName' may not exceed 64 characters")

    iam_user_name_re = compile(r'^[\w+=,.@-]+$')
    if iam_user_name_re.match(user_name):
        return user_name
    else:
        raise ValueError(
            "%s is not a valid value for AWS::IAM::User property 'UserName'",
            user_name)


def iam_path(path):
    if len(path) > 512:
        raise ValueError('IAM path %s may not exceed 512 characters', path)

    iam_path_re = compile(r'^\/.*\/$|^\/$')
    if not iam_path_re.match(path):
        raise ValueError("%s is not a valid iam path name" % path)
    return path


def iam_role_name(role_name):
    if len(role_name) > 64:
        raise ValueError('IAM Role Name may not exceed 64 characters')
    iam_names(role_name)
    return role_name


def iam_group_name(group_name):
    if len(group_name) > 128:
        raise ValueError('IAM Role Name may not exceed 128 characters')
    iam_names(group_name)
    return group_name


def count(properties, conditionals):
    found_list = []
    for c in conditionals:
        if c in properties:
            found_list.append(c)
    seen = set(found_list)
    specified_count = len(seen)

    return specified_count


def all_or_nothing(class_name, properties, conditionals):
    specified_count = count(properties, conditionals)
    if specified_count != 0 and specified_count != len(conditionals):
        raise ValueError(('%s: Either all or none of following'
                          ' must be specified: %s') % (
                          class_name, ', '.join(conditionals)))
    return specified_count


def mutually_exclusive(class_name, properties, conditionals):
    specified_count = count(properties, conditionals)
    if specified_count > 1:
        raise ValueError(('%s: only one of the following'
                          ' can be specified: %s') % (
                          class_name, ', '.join(conditionals)))
    return specified_count


def exactly_one(class_name, properties, conditionals):
    specified_count = mutually_exclusive(class_name, properties, conditionals)
    if specified_count != 1:
        raise ValueError(('%s: one of the following'
                          ' must be specified: %s') % (
                          class_name, ', '.join(conditionals)))
    return specified_count


def string_list_item(allowed_values):
    def string_list_item_checker(x):
        s = str(x)
        if s in allowed_values:
            return s
        raise ValueError('String must be one of following: %s' %
                         ', '.join(str(j) for j in allowed_values))

    return string_list_item_checker


def jagged_array(expected_type):
    def jagged_array_checker(x):
        # ensure outer list is present
        if not isinstance(x, list):
            raise ValueError("%r is not a valid array of array of %r" % (x, expected_type))

        try:
            l = list(x)
            for sub_list in l:
                # ensure inner sublist also exists
                if not isinstance(sub_list, list):
                    raise ValueError("%r is not a valid array of array of %r" % (x, expected_type))

                for value in sub_list:
                    if not isinstance(value, expected_type):
                        raise TypeError

            return l
        except(ValueError, TypeError):
            raise ValueError("%r is not a valid array of array of %r" % (x, expected_type))

    return jagged_array_checker
