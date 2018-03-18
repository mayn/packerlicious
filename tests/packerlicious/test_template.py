import json
import pytest

from packerlicious import UserVar, Template
from packerlicious import builder, post_processor, provisioner


class TestPackerTemplate(object):
    def test_template(self):
        t = Template(description="test description", min_packer_version="0.9.0")

        d = t.to_dict()
        assert d['description'] == "test description"
        assert d['min_packer_version'] == "0.9.0"

        t.add_description("new description")
        t.add_min_packer_version("1.0.0")
        d = t.to_dict()
        assert d['description'] == "new description"
        assert d['min_packer_version'] == "1.0.0"

    def test_template_variables(self):
        t = Template()

        t.add_variable(UserVar("my_var", "my_value"))

        d = t.to_dict()
        assert d['variables'] == {'my_var': 'my_value'}

    def test_template_builders(self):
        expected_json = """
        {
          "builders": [
            {
              "source": "/source/path",
              "target": "/target/path",
              "type": "file"
            },
            {
              "source": "/source/path",
              "target": "/target/path",
              "type": "file"
            }
          ]
        }
        """

        t = Template()
        t.add_builder([builder.File(
            target="/target/path",
            source="/source/path",
        ),builder.File(
            target="/target/path",
            source="/source/path",
        )])

        to_json = t.to_json()
        assert to_json == json.dumps(json.loads(expected_json), sort_keys=True, indent=2,
                                     separators=(',', ': '))

    def test_template_provisioners(self):
        expected_json = """
        {
          "provisioners": [
            {
              "source": "/src/path",
              "destination": "/dest/path",
              "direction": "upload",
              "type": "file"
            }
          ]
        }
        """

        t = Template()
        t.add_provisioner(provisioner.File(
            source="/src/path",
            destination="/dest/path",
            direction=provisioner.File.Upload,
        ))

        to_json = t.to_json()
        assert to_json == json.dumps(json.loads(expected_json), sort_keys=True, indent=2,
                                     separators=(',', ': '))

    def test_template_post_processors(self):
        expected_json = """
        {
          "post-processors": [
            {
              "script": "/my/post/script",
              "type": "shell-local"
            }
          ]
        }
        """

        t = Template()
        t.add_post_processor(post_processor.ShellLocal(
            script="/my/post/script",
        ))

        to_json = t.to_json()
        assert to_json == json.dumps(json.loads(expected_json), sort_keys=True, indent=2,
                                     separators=(',', ': '))

    def test_variable_duplicate_entries(self):
        t = Template()
        vars = [
            UserVar("my_var"),
            UserVar("my_var"),
        ]
        with pytest.raises(ValueError) as excinfo:
            t.add_variable(vars)
        assert 'duplicate key "my_var" detected' == str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            t.add_variable(UserVar("my_var"))
        assert 'duplicate key "my_var" detected' == str(excinfo.value)

    def test_variable_no_duplicate_entries(self):
        expected_json = """
                {
                  "variables": {
                     "my_var1": "a value",
                     "my_var2": ""
                  }
                }
                """

        t = Template()
        vars = [
            UserVar("my_var1", "a value"),
            UserVar("my_var2"),
        ]
        t.add_variable(vars)

        to_json = t.to_json()
        assert to_json == json.dumps(json.loads(expected_json), sort_keys=True, indent=2,
                                     separators=(',', ': '))

    def test_jagged_array_render(self):
        expected_json = """
        {
          "builders": [
            {
              "boot_wait": "10s",
              "floppy_files": [
                ""
              ],
              "guest_additions_path": "VBoxGuestAdditions_{{.Version}}.iso",
              "guest_os_type": "Ubuntu_64",
              "http_directory": "",
              "iso_checksum": "sha512",
              "iso_checksum_type": "sha512",
              "iso_url": "",
              "ssh_port": 22,
              "type": "virtualbox-iso",
              "vboxmanage": [
                [
                  "modifyvm", "{{.Name}}", "--memory", "1024"
                ],
                [ 
                  "modifyvm", "{{.Name}}", "--vram", "36"
                ],
                [
                  "modifyvm", "{{.Name}}", "--cpus", "1"
                ]
              ],
              "virtualbox_version_file": ".vbox_version",
              "vm_name": "my_name"
            }
          ]
        }
        """

        t = Template()
        t.add_builder(
            builder.VirtualboxIso(
                boot_wait="10s",
                guest_os_type="Ubuntu_64",
                http_directory="",
                iso_url="",
                iso_checksum_type="sha512",
                iso_checksum="sha512",
                ssh_port=22,
                guest_additions_path="VBoxGuestAdditions_{{.Version}}.iso",
                virtualbox_version_file=".vbox_version",
                vm_name="my_name",
                floppy_files=[""],
                vboxmanage=[
                    "modifyvm {{.Name}} --memory 1024".split(),
                     "modifyvm {{.Name}} --vram 36".split(),
                     "modifyvm {{.Name}} --cpus 1".split()
                ]
                # vboxmanage=[['modifyvm {{.Name}} --memory 1024', "modifyvm {{.Name}} --cpus 1"]]
            )
        )

        to_json = t.to_json()
        assert to_json == json.dumps(json.loads(expected_json), sort_keys=True, indent=2,
                                     separators=(',', ': '))
