# Copyright (c) 2012-2013, Mark Peek <mark@peek.org>
# All rights reserved.

import os
import re
import sys

try:
    import StringIO as io
except ImportError:
    import io

try:
    u = unicode
except NameError:
    u = str


class TestFileExamples(object):

    def pytest_generate_tests(self, metafunc):
        if self.__class__ == metafunc.cls:
            # Filter out all *.py files from the examples directory
            examples = os.path.dirname(os.path.realpath(__file__)) + '/../../' + 'examples'
            regex = re.compile(r'.py$', re.I)
            example_filenames = list(filter(regex.search, os.listdir(examples)))
            assert len(example_filenames) > 0

            metafunc.parametrize('example_file', [examples + '/' + f for f in example_filenames])

    def test_examples(self, example_file):
        saved = sys.stdout
        stdout = io.StringIO()
        try:
            sys.stdout = stdout
            with open(example_file) as f:
                code = compile(f.read(), example_file, 'exec')
                exec (code, {'__name__': '__main__'})
        finally:
            sys.stdout = saved
        # rewind fake stdout so we can read it
        stdout.seek(0)
        actual_output = stdout.read()
        example_file_name = (os.path.basename(example_file))[:-3]
        output_file_path = os.path.dirname(os.path.realpath(__file__)) + '/../' + 'examples_output/%s.template' % example_file_name
        expected_output = open(output_file_path).read()

        assert u(expected_output) == u(actual_output)
