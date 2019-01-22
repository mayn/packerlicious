import pytest

import packerlicious.builder as builder


class TestOpenStackBuilder(object):

    def test_required_fields_missing(self):
        b = builder.OpenStack()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_validate(self):
        b = builder.OpenStack(
            image_name="test image",
            flavor="2"
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert "OpenStack: one of the following must be specified: source_image, source_image_name, source_image_filter" == str(excinfo.value)
