import pytest

import packerlicious.post_processor as post_processor


class TestChecksumPostProcessor(object):
    def test_no_required_fields(self):
        b = post_processor.Checksum()

        b.to_dict()

    def test_checksum_types_valid(self):
        b = post_processor.Checksum(
            checksum_types=[
                "md5", "sha1", "sha224", "sha256", "sha384", "sha512"
            ],
        )

        assert b.to_dict()

    def test_checksum_types_invalid(self):
        b = post_processor.Checksum(
            checksum_types=[
                "md5", "sha123",
            ],
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'only one of the following can be specified: md5, sha1, sha224, sha256, sha384, sha512' in str(excinfo.value)
