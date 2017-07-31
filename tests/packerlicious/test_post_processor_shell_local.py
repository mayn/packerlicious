import pytest

import packerlicious.post_processor as post_processor


class TestShellLocalPostProcessor(object):

    def test_no_required_fields(self):
        b = post_processor.ShellLocal()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'one of the following must be specified: inline, script, scripts' in str(excinfo.value)
