import pytest

import packerlicious.builder as builder


class TestVirtualBoxOvfBuilder(object):

    def test_required_fields_missing(self):
        b = builder.VirtualboxOvf()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)


class TestVirtualBoxIsoBuilder(object):

    def test_required_fields_missing(self):
        b = builder.VirtualboxIso()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_is_checksum_mutually_exclusive(self):
        b = builder.VirtualboxIso(
            iso_url="/url/to/iso",
            iso_checksum_type=builder.VirtualboxIso.MD5,
            iso_checksum="my_checksum",
            iso_checksum_url="my_checksum_url",
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'VirtualboxIso: only one of the following can be specified: iso_checksum, iso_checksum_url' == str(excinfo.value)
