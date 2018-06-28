import pytest

from packerlicious import Ref, Join, EnvVar, TemplateVar, UserVar


class TestPackerVariables(object):
    def test_environment_variable(self):
        var = EnvVar("MY_TEST_ENV")

        assert var.data == "MY_TEST_ENV"
        assert var.ref().data == "{{env `MY_TEST_ENV`}}"
        assert Ref(var).data == "{{env `MY_TEST_ENV`}}"

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

    def test_join_variable(self):
        var = Join("-", ["test", "coverage"])

        assert var.title == "test-coverage"
