import pytest

import packerlicious.post_processor as post_processor


class TestAmazonImportPostProcessor(object):
    def test_required_fields(self):
        b = post_processor.AmazonImport()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_required_fields(self):
        b = post_processor.AmazonImport(
            region="us-west-1",
            s3_bucket_name='a bucket',
            access_key="dummy-access-key"
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonImport: Either all or none of following must be specified: access_key, secret_key' == str(excinfo.value)
