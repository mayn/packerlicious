import pytest

import packerlicious.builder as builder


class TestHyperOneBuilder(object):

    def test_no_required_fields(self):
        b = builder.HyperOne()

        b.to_dict()
