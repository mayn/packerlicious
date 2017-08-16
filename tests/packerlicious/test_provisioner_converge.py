import pytest

import packerlicious.provisioner as provisioner


class TestConvergeProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.Converge()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_module_directory_required_fields_missing(self):
        b = provisioner.ModuleDirectory()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
