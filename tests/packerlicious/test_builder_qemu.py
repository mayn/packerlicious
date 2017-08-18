import pytest

import packerlicious.builder as builder


class TestQemuBuilder(object):

    def test_required_fields_missing(self):
        b = builder.Qemu()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_iso_checksum_mutually_exclusive(self):
        b = builder.Qemu(
            iso_url="/url/to/iso",
            iso_checksum_type=builder.Qemu.MD5,
            iso_checksum="my_checksum",
            iso_checksum_url="my_checksum_url",
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'Qemu: only one of the following can be specified: iso_checksum, iso_checksum_url' == str(excinfo.value)
