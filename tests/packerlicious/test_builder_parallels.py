import pytest

import packerlicious.builder as builder


class TestParallelsIsoBuilder(object):

    def test_required_fields_missing(self):
        b = builder.ParallelsIso()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_iso_checksum_mutually_exclusive(self):
        b = builder.ParallelsIso(
            iso_url="/url/to/iso",
            iso_checksum_type="md5",
            parallels_tools_flavor="other",
            iso_checksum="my_checksum",
            iso_checksum_url="my_checksum_url",
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'ParallelsIso: only one of the following can be specified: iso_checksum, iso_checksum_url' == str(
            excinfo.value)


class TestParallelsPvmBuilder(object):

    def test_required_fields_missing(self):
        b = builder.ParallelsPvm()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
