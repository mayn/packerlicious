import pytest

import packerlicious.builder as builder


class TestVagrantBuilder(object):

    def test_required_fields_missing(self):
        b = builder.Vagrant()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'Vagrant: one of the following must be specified: source_path, global_id' in str(excinfo.value)

    def test_source_path_global_id_mutually_exclusive(self):
        b = builder.Vagrant(
            source_path="..",
            global_id="..",
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'Vagrant: only one of the following can be specified: source_path, global_id' in str(excinfo.value)
