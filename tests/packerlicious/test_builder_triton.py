import pytest

import packerlicious.builder as builder


class TestTritonBuilder(object):

    def test_required_fields_missing(self):
        b = builder.Triton()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_validate(self):
        b = builder.Triton(
            triton_account="triton_username",
            triton_key_id="6b:95:03:3d",
            source_machine_package="g4-highcpu-128M",
            image_name="my image",
            image_version="1.0"

        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert "Triton: one of the following must be specified: source_machine_image, source_machine_image_filter" == str(excinfo.value)
