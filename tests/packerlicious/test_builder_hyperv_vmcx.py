import pytest

import packerlicious.builder as builder


class TestHyperVvmcxBuilder(object):

    def test_required_fields_missing(self):
        b = builder.HyperVvmcx()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_exactly_one_clone(self):
        b = builder.HyperVvmcx(
            clone_from_vmxc_path="c:\\virtual machines\\ubuntu-12.04.5-server-amd64",
            clone_from_vm_name="ubuntu-12.04.5-server-amd64"
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'HyperVvmcx: only one of the following can be specified: clone_from_vmxc_path, clone_from_vm_name' == str(
            excinfo.value)
