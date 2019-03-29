import pytest
import packerlicious.provisioner as provisioner
from packerlicious import Template
import json


class TestInspecProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.Inspec()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_property_attributes_renders(self):
        expected_json = """
                        {
                          "provisioners": [
                            {
                              "attributes": ["examples/linux.yml"],
                              "profile": "a_profile",
                              "type": "inspec"
                            }
                          ]
                        }
                        """

        t = Template()
        p = provisioner.Inspec(
                attributes=["examples/linux.yml"],
                profile="a_profile"
            )

        t.add_provisioner(p)

        to_json = t.to_json()
        assert to_json == json.dumps(json.loads(expected_json), sort_keys=True, indent=2,
                                     separators=(',', ': '))
