import pytest

import packerlicious.provisioner as provisioner


class TestFileProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.File()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    @pytest.mark.parametrize("input_direction", [
        provisioner.File.Download,
        provisioner.File.Upload,

    ])
    def test_direction_valid(self, input_direction):
        b = provisioner.File(
            source="dummy_source",
            destination="dummy_target",
            direction=input_direction,
        )

        assert b.to_dict()

    def test_direction_invalid(self):
        with pytest.raises(ValueError) as excinfo:
            provisioner.File(
                source="dummy_source",
                destination="dummy_target",
                direction="upload2",
            )

        assert 'String must be one of following: upload, download' == str(excinfo.value)

