import pytest

import packerlicious.builder as builder


class TestAzureBuilder(object):

    def test_required_fields_missing(self):
        b = builder.Cloudstack()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
