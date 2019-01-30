import pytest

import packerlicious.community.builder as builder


class TestArmImageBuilder(object):

    def test_required_fields_missing(self):
        b = builder.ArmImage()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
