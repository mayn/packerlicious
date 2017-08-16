import pytest

import packerlicious.provisioner as provisioner


class TestChefClientProvisioner(object):

    def test_no_required_fields(self):
        b = provisioner.ChefClient()

        b.to_dict()


class TestChefSoloProvisioner(object):

    def test_no_required_fields(self):
        b = provisioner.ChefSolo()

        b.to_dict()
