import pytest

import packerlicious.post_processor as post_processor


class TestVagrantPostProcessor(object):

    def test_no_required_fields(self):
        b = post_processor.Vagrant()

        b.to_dict()


class TestVagrantCloudPostProcessor(object):

    def test_required_fields_missing(self):
        b = post_processor.VagrantCloud()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
