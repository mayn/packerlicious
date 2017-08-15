import pytest

import packerlicious.provisioner as provisioner


class TestWindowsShellProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.WindowsShell()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'WindowsShell: one of the following must be specified: inline, script, scripts' == str(excinfo.value)


class TestWindowsRestartProvisioner(object):

    def test_no_required_fields(self):
        b = provisioner.WindowsRestart()

        b.to_dict()
