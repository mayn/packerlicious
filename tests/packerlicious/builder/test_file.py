import pytest
import packerlicious.builder.file as builder


class TestFileBuilder(object):

    def test_required_fields_missing(self):
        b = builder.File()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_source_and_content_mutually_exclusive(self):
            b = builder.File(
                target="dummy_artifact",
                source="/tmp/source.txt",
                content="Lorem ipsum dolor sit amet",
            )

            with pytest.raises(ValueError) as excinfo:
                b.to_dict()
            assert 'only one of the following can be specified: source, content' in str(excinfo.value)

    def test_source_and_content_missing(self):
            b = builder.File(
                target="dummy_artifact",
            )

            with pytest.warns(UserWarning) as record:
                b.to_dict()
            assert len(record) == 1
            assert 'Both source and content not specified, artifact will be empty.' == str(record[0].message)

