import pytest

import packerlicious.post_processor as post_processor


class TestChecksumPostProcessor(object):
    def test_no_required_fields(self):
        b = post_processor.Compress()

        b.to_dict()
