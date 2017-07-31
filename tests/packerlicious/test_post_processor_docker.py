import pytest

import packerlicious.post_processor as post_processor


class TestDockerImportPostProcessor(object):

    def test_required_fields_missing(self):
        b = post_processor.DockerImport()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)


class TestDockerPushPostProcessor(object):

    def test_no_required_fields(self):
        b = post_processor.DockerPush()

        b.to_dict()


class TestDockerSavePostProcessor(object):

    def test_required_fields_missing(self):
        b = post_processor.DockerSave()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)


class TestDockerTagPostProcessor(object):

    def test_required_fields_missing(self):
        b = post_processor.DockerTag()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
