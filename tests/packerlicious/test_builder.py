import pytest

import packerlicious.builder as builder
from packerlicious import Template
import json


class TestBuilderAttributes(object):

    def test_support_named_builds(self):
        expected_json = """
                {
                  "builders": [
                    {
                      "type": "file",
                      "name": "linuxFileBuilder",
                      "source": "/tmp/source/path",
                      "target": "/tmp/target/path"
                    },
                    {
                      "type": "file",
                      "name": "windowsFileBuilder",
                      "source": "C:/Source/Path",
                      "target": "C:/Target/Path"
                    }
                  ]
                }
                """

        b = [
            builder.File(
                name="linuxFileBuilder",
                source="/tmp/source/path",
                target="/tmp/target/path",
            ),
            builder.File(
                name="windowsFileBuilder",
                source='C:/Source/Path',
                target='C:/Target/Path',
            )
        ]

        t = Template()
        t.add_builder(b)

        to_json = t.to_json()
        assert to_json == json.dumps(json.loads(expected_json), sort_keys=True, indent=2,
                                     separators=(',', ': '))
