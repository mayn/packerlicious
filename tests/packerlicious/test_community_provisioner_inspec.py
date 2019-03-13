import pytest

import packerlicious.community.provisioner as provisioner


class TestCommunityInspecProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.Inspec()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
