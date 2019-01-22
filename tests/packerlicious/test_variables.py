import pytest

from packerlicious import Ref, EnvVar, TemplateVar, UserVar, PackerVariable


class TestPackerVariables(object):
    def test_environment_variable(self):
        var = EnvVar("MY_TEST_ENV")

        assert var.title == "my_test_env"
        assert var.data == "{{env `MY_TEST_ENV`}}"
        assert var.ref().data == "{{user `my_test_env`}}"
        assert Ref(var).data == "{{user `my_test_env`}}"

    def test_environment_variable_name_specified(self):
        var = EnvVar("my_other_name", "MY_TEST_ENV")

        assert var.title == "my_other_name"
        assert var.data == "{{env `MY_TEST_ENV`}}"
        assert var.ref().data == "{{user `my_other_name`}}"
        assert Ref(var).data == "{{user `my_other_name`}}"

    def test_template_variable(self):
        var = TemplateVar("MY_TEST_TEMPLATE")

        assert var.data == "MY_TEST_TEMPLATE"
        assert var.ref().data == "{{.MY_TEST_TEMPLATE}}"
        assert Ref(var).data == "{{.MY_TEST_TEMPLATE}}"

    def test_user_variable(self):
        var = UserVar("MY_TEST_USER", "testValue")

        assert var.title == "MY_TEST_USER"
        assert var.data == "testValue"
        assert var.ref().data == "{{user `MY_TEST_USER`}}"
        assert Ref(var).data == "{{user `MY_TEST_USER`}}"

    def test_packer_variable(self):
        var = PackerVariable("{{timestamp}}")

        assert var.data == "{{timestamp}}"
        assert var.ref().data.data == "{{timestamp}}"
        assert Ref(var).data.data == "{{timestamp}}"
