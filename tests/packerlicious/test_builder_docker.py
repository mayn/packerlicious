import pytest

import packerlicious.builder as builder


class TestDockerBuilder(object):

    def test_required_fields_missing(self):
        b = builder.Docker()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_source_and_content_mutually_exclusive(self):
            b = builder.Docker(
                image="nginx",
                commit=True,
                discard=False,
                export_path="/dummy/export/path",
            )

            with pytest.raises(ValueError) as excinfo:
                b.to_dict()
            assert 'only one of the following can be specified: commit, discard, export_path' in str(excinfo.value)
