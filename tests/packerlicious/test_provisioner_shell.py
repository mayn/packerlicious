import pytest

import packerlicious.provisioner as provisioner


class TestShellProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.Shell()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'must be specified' in str(excinfo.value)


class TestShellLocalProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.ShellLocal()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

