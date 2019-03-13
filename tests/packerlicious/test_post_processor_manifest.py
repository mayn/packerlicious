import packerlicious.post_processor as post_processor
from packerlicious.template import Template
import json


class TestManifestPostProcessor(object):

    def test_no_required_fields(self):
        b = post_processor.Manifest()

        b.to_dict()

    def test_custom_data(self):
        expected_json = """
        {
          "post-processors": [
            {
              "type": "manifest",
              "output": "manifest.json",
              "strip_path": "true",
              "custom_data": {
                "my_custom_data": "example"
              }
            }
          ]
        }
        """
        p = post_processor.Manifest(
            output="manifest.json",
            strip_path=True,
            custom_data={'my_custom_data': 'example'}
        )
        t = Template()
        t.add_post_processor(p)

        to_json = t.to_json()
        assert to_json == json.dumps(json.loads(expected_json), sort_keys=True, indent=2,
                                     separators=(',', ': '))
