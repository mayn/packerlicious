import pytest

import packerlicious.builder as builder


class TestVMwareIsoBuilder(object):

    def test_required_fields_missing(self):
        b = builder.VMwareIso()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_iso_checksum_mutually_exclusive(self):
        b = builder.VMwareIso(
            iso_url="/url/to/iso",
            iso_checksum_type=builder.VirtualboxIso.MD5,
            iso_checksum="my_checksum",
            iso_checksum_url="my_checksum_url",
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'VMwareIso: only one of the following can be specified: iso_checksum, iso_checksum_url' == str(
            excinfo.value)


class TestVMwareVmxBuilder(object):

    def test_required_fields_missing(self):
        b = builder.VMwareVmx()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
