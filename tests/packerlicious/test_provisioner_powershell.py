import pytest

import packerlicious.provisioner as provisioner


class TestPowerShellProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.PowerShell()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'PowerShell: one of the following must be specified: inline, script, scripts' == str(excinfo.value)

