import pytest

import packerlicious.post_processor as post_processor


class TestGoogleComputeImportPostProcessor(object):

    def test_required_fields_missing(self):
        b = post_processor.GoogleComputeImport()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)


class TestGoogleComputeExportPostProcessor(object):

    def test_required_fields_missing(self):
        b = post_processor.GoogleComputeExport()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
