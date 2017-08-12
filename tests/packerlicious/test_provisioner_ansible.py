import pytest

import packerlicious.provisioner as provisioner


class TestAnsibleLocalProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.AnsibleLocal()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)


class TestAnsibleProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.Ansible()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
