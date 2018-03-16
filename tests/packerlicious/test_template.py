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


    expected_json_1 = """
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
              "modifyvm {{.Name}} --memory 1024"
            ],
            [
              "modifyvm {{.Name}} --cpus 1"
            ]
          ],
          "virtualbox_version_file": ".vbox_version",
          "vm_name": ""
        }
      ]
    }
    """
    expected_json_2 = """
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
              "modifyvm {{.Name}} --memory 1024"
            ],
            [
              "modifyvm",
              "{{.Name}}",
              "--cpus 1"
            ]
          ],
          "virtualbox_version_file": ".vbox_version",
          "vm_name": ""
        }
      ]
    }
    """
    exception_1 = "<class 'packerlicious.builder.VirtualboxIso'>: None.vboxmanage is <type 'list'>, expected [[<type 'str'>]]"
    exception_2 = "<class 'packerlicious.builder.VirtualboxIso'>: None.vboxmanage is <type 'int'>, expected <type 'str'>"
    @pytest.mark.parametrize('test_input,exception,expected', [
        pytest.param(
            [['modifyvm {{.Name}} --memory 1024'], ['modifyvm {{.Name}} --cpus 1']],
            False,
            expected_json_1,
            marks=pytest.mark.basic
        ),
        pytest.param(
            [['modifyvm {{.Name}} --memory 1024'], ['modifyvm', '{{.Name}}', '--cpus 1']],
            False,
            expected_json_2,
            marks=pytest.mark.basic
        ),
        pytest.param(
            [['modifyvm {{.Name}} --memory 1024'], 1],
            True,
            exception_1,
            marks=pytest.mark.basic
        ),
        pytest.param(
            [['modifyvm {{.Name}} --memory 1024'], [1]],
            True,
            exception_2,
            marks=pytest.mark.basic
        )
    ])
    def test_list_of_list_type_check(self, test_input, exception, expected):

        t = Template()
        HTTP_DIR = ""
        ISO_URL = ""
        ISO_CHECKSUM_TYPE = "sha512"
        ISO_CHECKSUM = "sha512"
        VM_NAME = ""
        VBOX_MANAGE=test_input
        if exception:
            with pytest.raises(TypeError) as excinfo:
                t.add_builder(
                    builder.VirtualboxIso(
                        boot_wait="10s",
                        guest_os_type="Ubuntu_64",
                        http_directory=HTTP_DIR,
                        iso_url=ISO_URL,
                        iso_checksum_type=ISO_CHECKSUM_TYPE,
                        iso_checksum=ISO_CHECKSUM,
                        ssh_port=22,
                        guest_additions_path="VBoxGuestAdditions_{{.Version}}.iso",
                        virtualbox_version_file=".vbox_version",
                        vm_name=VM_NAME,
                        floppy_files=[""],
                        vboxmanage=VBOX_MANAGE
                    )
                )
            assert expected == str(excinfo.value)
        else:
            t.add_builder(
                builder.VirtualboxIso(
                    boot_wait="10s",
                    guest_os_type="Ubuntu_64",
                    http_directory=HTTP_DIR,
                    iso_url=ISO_URL,
                    iso_checksum_type=ISO_CHECKSUM_TYPE,
                    iso_checksum=ISO_CHECKSUM,
                    ssh_port=22,
                    guest_additions_path="VBoxGuestAdditions_{{.Version}}.iso",
                    virtualbox_version_file=".vbox_version",
                    vm_name=VM_NAME,
                    floppy_files=[""],
                    vboxmanage=VBOX_MANAGE
                )
            )
            to_json = t.to_json()
            assert to_json == json.dumps(json.loads(expected), sort_keys=True, indent=2,
                                     separators=(',', ': '))
