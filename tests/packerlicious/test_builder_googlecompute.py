import pytest

import packerlicious.builder as builder


class TestGoogleComputeBuilder(object):

    def test_required_fields_missing(self):
        b = builder.GoogleCompute()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_validate(self):
        b = builder.GoogleCompute(
            project_id="my project",
            zone="us-central1-a"
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert "GoogleCompute: one of the following must be specified: source_image, source_image_family" == str(excinfo.value)
