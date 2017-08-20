import pytest

import packerlicious.builder as builder


class TestNullBuilder(object):

    def test_no_required_fields(self):
        b = builder.Null()

        b.to_dict()
