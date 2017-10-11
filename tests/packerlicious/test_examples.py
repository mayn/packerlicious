# Copyright (c) 2012-2013, Mark Peek <mark@peek.org>
# All rights reserved.

import os
import re
from importlib import import_module


class TestFileExamples(object):

    output_files = None

    def load_output_files(self):
        self.output_files = {}
        regex = re.compile(r'.template', re.I)
        current_directory = os.path.dirname(os.path.realpath(__file__)) + '/../' + 'examples_output'
        example_filenames = filter(regex.search, os.listdir(current_directory))
        for example_filename in example_filenames:
            with open(current_directory + '/' + example_filename) as f:
                self.output_files[example_filename] = f.read()

    def load_example_file(self, example_output_filename):
        original_example = example_output_filename.split('.')[0]
        example_module = import_module('examples.' + original_example)
        assert self.output_files[original_example + '.template'].rstrip() == example_module.t.to_json()

    def test_examples(self):
        self.load_output_files()
        for file_name in self.output_files.keys():
            self.load_example_file(file_name)





