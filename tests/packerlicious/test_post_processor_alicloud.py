import pytest

import packerlicious.post_processor as post_processor


class TestAlicloudImportPostProcessor(object):
    def test_required_fields(self):
        b = post_processor.AlicloudImport()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
