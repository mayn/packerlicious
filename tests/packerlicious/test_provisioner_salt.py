import pytest

import packerlicious.provisioner as provisioner


class TestSaltMasterlessProvisioner(object):

    def test_required_fields_missing(self):
        b = provisioner.SaltMasterless()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_warning_minion_config(self):
        b = provisioner.SaltMasterless(
            local_state_tree="/dummy/path",
            remote_pillar_roots="/remote/salt/root/path",
            minion_config="/minion/config/path"
        )

        with pytest.warns(UserWarning) as record:
            b.to_dict()
        assert len(record) == 1
        assert "'minion_config' is present, 'remote_pillar_roots' and 'remote_state_tree' will be ignored." == str(record[0].message)
