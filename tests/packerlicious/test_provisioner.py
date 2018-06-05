
from packerlicious import Template
import packerlicious.provisioner as provisioner
import json


class TestProvisionerAttributes(object):

    def test_support_only(self):
        expected_json = """
        {
          "provisioners": [
            {
              "type": "shell-local",
              "inline": [ "ls" ],
              "only": [ "azure-arm" ]
            }
          ]
        }
        """

        p = provisioner.ShellLocal(
            inline=["ls"],
            only=["azure-arm"]
        )

        t = Template()
        t.add_provisioner(p)

        to_json = t.to_json()
        assert to_json == json.dumps(json.loads(expected_json), sort_keys=True, indent=2,
                                     separators=(',', ': '))

    def test_support_only(self):
        expected_json = """
        {
          "provisioners": [
            {
              "type": "shell",
              "inline": [ "ls" ],
              "except": [ "azure-arm" ]
            }
          ]
        }
        """

        p = provisioner.Shell(
            inline=["ls"])

        p.__setattr__('except', ["azure-arm"])

        t = Template()
        t.add_provisioner(p)

        to_json = t.to_json()
        assert to_json == json.dumps(json.loads(expected_json), sort_keys=True, indent=2,
                                     separators=(',', ': '))



    def test_support_pause_before(self):
        expected_json = """
        {
          "provisioners": [
            {
              "type": "shell",
              "inline": [ "ls" ],
              "pause_before": "10s"
            }
          ]
        }
        """

        p = provisioner.Shell(
            inline=["ls"],
            pause_before="10s"
        )

        t = Template()
        t.add_provisioner(p)

        to_json = t.to_json()
        assert to_json == json.dumps(json.loads(expected_json), sort_keys=True, indent=2,
                                     separators=(',', ': '))


