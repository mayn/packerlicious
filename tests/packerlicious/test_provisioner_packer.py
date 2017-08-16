import pytest

import packerlicious.provisioner as provisioner


class TestPuppetMasterlessProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.PuppetMasterless()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'Resource manifest_file required in type puppet-masterless' == str(excinfo.value)


class TestPuppetServerProvisioner(object):

    def test_no_required_fields(self):
        b = provisioner.PuppetServer()

        b.to_dict()
