import pytest

import packerlicious.builder as builder


class TestCloudStackBuilder(object):

    def test_required_fields_missing(self):
        b = builder.CloudStack()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_validate(self):
        b = builder.CloudStack(
            api_url="http://api.url",
            api_key="YOUR_API_KEY",
            secret_key="YOUR_SECRET_KEY",
            network="management",
            service_offering="small",
            template_os="new os id",
            zone="NL1"
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert "CloudStack: one of the following must be specified: source_iso, source_template" == str(excinfo.value)
