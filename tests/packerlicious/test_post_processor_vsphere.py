import pytest

import packerlicious.post_processor as post_processor


class TestVSphereProcessor(object):

    def test_required_fields_missing(self):
        b = post_processor.VSphere()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
