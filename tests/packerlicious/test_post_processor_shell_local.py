import pytest

import packerlicious.post_processor as post_processor


class TestShellLocalPostProcessor(object):

    def test_required_fields(self):
        b = post_processor.ShellLocal()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert u'one of the following must be specified: command, inline, script, scripts' in str(excinfo.value)
