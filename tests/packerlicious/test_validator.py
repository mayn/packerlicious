# Copyright (c) 2012-2013, Mark Peek <mark@peek.org>
# All rights reserved.
#
import pytest

from thirdparty.troposphere import Parameter, Ref
from packerlicious.validator import boolean, integer, integer_range
from packerlicious.validator import network_port
from packerlicious.validator import tg_healthcheck_port
from packerlicious.validator import s3_bucket_name, encoding, status
from packerlicious.validator import iam_path, iam_names, iam_role_name
from packerlicious.validator import iam_group_name, iam_user_name, elb_name
from packerlicious.validator import jagged_array
from packerlicious.validator import all_or_nothing, mutually_exclusive
from packerlicious.validator import integer_list_item


class TestValidator(object):

    def test_boolean(self):
        for x in [True, "True", "true", 1, "1"]:
            assert boolean(x) == "true", repr(x)
        for x in [False, "False", "false", 0, "0"]:
            assert boolean(x) == "false", repr(x)
        for x in ["000", "111", "abc"]:
            with pytest.raises(ValueError):
                boolean(x)

    def test_integer(self):
        assert integer(-1) == -1
        assert integer("-1") == "-1"
        assert integer(0) == 0
        assert integer("0") == "0"
        assert integer(65535) == 65535
        assert integer("65535") == "65535"
        assert integer(1.0) == 1.0
        with pytest.raises(ValueError):
            integer("string")
        with pytest.raises(ValueError):
            integer(object)
        with pytest.raises(ValueError):
            integer(None)

    def test_integer_range(self):
        between_ten_and_twenty = integer_range(10, 20)
        assert between_ten_and_twenty(10) == 10
        assert between_ten_and_twenty(15) == 15
        assert between_ten_and_twenty(20) == 20
        for i in (-1, 9, 21, 1111111):
            with pytest.raises(ValueError):
                between_ten_and_twenty(i)

    def test_network_port(self):
        for x in [-1, 0, 1, 1024, 65535]:
            network_port(x)
        for x in [-2, -10, 65536, 100000]:
            with pytest.raises(ValueError):
                network_port(x)

    def test_network_port_ref(self):
        p = Parameter('myport')
        network_port(Ref(p))

    def test_tg_healthcheck_port(self):
        for x in ["traffic-port"]:
            tg_healthcheck_port(x)
        for x in [-1, 0, 1, 1024, 65535]:
            tg_healthcheck_port(x)
        for x in [-2, -10, 65536, 100000]:
            with pytest.raises(ValueError):
                tg_healthcheck_port(x)

    def test_tg_healthcheck_port_ref(self):
        p = Parameter('myport')
        tg_healthcheck_port(Ref(p))

    def test_s3_bucket_name(self):
        for b in ['a'*3, 'a'*63, 'wick3d-sweet.bucket']:
            s3_bucket_name(b)
        for b in ['a'*2, 'a'*64, 'invalid_bucket', 'InvalidBucket']:
            with pytest.raises(ValueError):
                s3_bucket_name(b)
        for b in ['.invalid', 'invalid.', 'invalid..bucket']:
            with pytest.raises(ValueError):
                s3_bucket_name(b)
        for b in ['1.2.3.4', '11.22.33.44', '111.222.333.444']:
            with pytest.raises(ValueError):
                s3_bucket_name(b)

    def test_elb_name(self):
        for b in ['a', 'a-a', 'aaa', 'a'*32,
                  'wick3d-elb-name', 'Wick3d-ELB-Name']:
            elb_name(b)
        for b in ['a'*33, 'invalid_elb', '-invalid-elb',
                  'invalid-elb-', '-elb-', '-a', 'a-']:
            with pytest.raises(ValueError):
                elb_name(b)

    def test_encoding(self):
        for e in ['plain', 'base64']:
            encoding(e)
        for e in ['wrong_encdoing', 'base62']:
            with pytest.raises(ValueError):
                encoding(e)

    def test_status(self):
        for s in ['Active', 'Inactive']:
            status(s)
        for s in ['active', 'idle']:
            with pytest.raises(ValueError):
                status(s)

    def test_iam_names(self):
        for s in ['foobar.+=@-,', 'BARfoo789.+=@-,']:
            iam_names(s)
        for s in ['foo%', 'bar$']:
            with pytest.raises(ValueError):
                iam_names(s)

    def test_iam_path(self):
        for s in ['/%s/' % ('a'*30), '/%s/' % ('a'*510)]:
            iam_path(s)
        for s in ['/%s/' % ('a'*511), '/%s/' % ('a'*1025)]:
            with pytest.raises(ValueError):
                iam_path(s)
        for s in ['%s' % ('a'*5)]:
            with pytest.raises(ValueError):
                iam_path(s)

    def test_iam_role_name(self):
        for s in ['a'*30, 'a'*64]:
            iam_role_name(s)
        for s in ['a'*65, 'a'*128]:
            with pytest.raises(ValueError):
                iam_role_name(s)

    def test_iam_group_name(self):
        for s in ['a'*64, 'a'*128]:
            iam_group_name(s)
        for s in ['a'*129, 'a'*256]:
            with pytest.raises(ValueError):
                iam_group_name(s)

    def test_iam_user_name(self):
        for s in ['a', 'a'*64, 'A', 'Aa', 'A=,.@-']:
            iam_user_name(s)
        for s in ['', 'a'*65, 'a%', 'a#', 'A a']:
            with pytest.raises(ValueError):
                iam_user_name(s)

    def test_all_or_nothing(self):
        conds = ['a', 'b', 'c']
        all_or_nothing('z', ['z'], conds)
        all_or_nothing('abc', ['a', 'b', 'c'], conds)
        all_or_nothing('abcd', ['a', 'b', 'c', 'd'], conds)
        with pytest.raises(ValueError):
            all_or_nothing('ac', ['a', 'c'], conds)
        with pytest.raises(ValueError):
            all_or_nothing('b', ['b'], conds)

    def test_mutually_exclusive(self):
        conds = ['a', 'b', 'c']
        mutually_exclusive('a', ['a'], conds)
        mutually_exclusive('b', ['b'], conds)
        mutually_exclusive('c', ['c'], conds)
        with pytest.raises(ValueError):
            mutually_exclusive('ac', ['a', 'c'], conds)
        with pytest.raises(ValueError):
            mutually_exclusive('abc', ['a', 'b', 'c'], conds)

    @pytest.mark.parametrize('test_value', [
            'a_string_value',
            1234,
            ['a_list_0', 'a_list_1'],
            [['jagged_array_0,0'], 1234],
            [['jagged_array_0,0'], [1234]],
    ])
    def test_jagged_array_failure(self, test_value):
        jagged_array_validator = jagged_array(str)
        with pytest.raises(ValueError):
            jagged_array_validator(test_value)

    @pytest.mark.parametrize('test_value', [
            [['jagged_array_0,0', 'jagged_array_0,1'], ['jagged_array_1,0']],
    ])
    def test_jagged_array_success(self, test_value):
        jagged_array_validator = jagged_array(str)
        validator_return_value = jagged_array_validator(test_value)

        for i, sub_list in enumerate(test_value):
            for j, value in enumerate(sub_list):
                assert validator_return_value[i][j] == value

    def test_integer_list_item(self):
        allowed_values = [1, 3, 5]
        int_list_item_validator = integer_list_item('prop_name', allowed_values)

        int_list_item_validator(1)
        int_list_item_validator(3)
        int_list_item_validator(5)

        with pytest.raises(ValueError):
            int_list_item_validator('not_an_integer')
        with pytest.raises(ValueError):
            int_list_item_validator(0)
        with pytest.raises(ValueError):
            int_list_item_validator(2)
        with pytest.raises(ValueError):
            int_list_item_validator(6)
