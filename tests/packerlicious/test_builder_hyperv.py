import pytest

import packerlicious.builder as builder


class TestHypervIsoBuilder(object):

    def test_required_fields_missing(self):
        b = builder.HypervIso()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)


class TestHypervVmcxBuilder(object):

    def test_required_fields_missing(self):
        b = builder.HypervVmcx()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'HypervVmcx: one of the following must be specified: clone_from_vmxc_path, clone_from_vm_name' == str(excinfo.value)

    def test_exactly_one_clone_from_required(self):
        b = builder.HypervVmcx(
            clone_from_vmcx_path="c:\\virtual machines\\ubuntu-12.04.5-server-amd64",
            clone_from_vm_name="ubuntu-12.04.5-server-amd64"
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'HypervVmcx: only one of the following can be specified: clone_from_vmxc_path, clone_from_vm_name' == str(
            excinfo.value)

    def test_exactly_one_clone_from_specified(self):
        b = builder.HypervVmcx(
            clone_from_vmcx_path="c:\\virtual machines\\ubuntu-12.04.5-server-amd64",
        )

        b.to_dict()
