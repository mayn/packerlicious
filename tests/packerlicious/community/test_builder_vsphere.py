import pytest

import packerlicious.community.builder as builder

class TestVSphereIsoBuilder(object):

    required_defaults = {
        'vcenter_server':"",
        'username':"",
        'password':"",
        'datastore':"",
        'cluster':"",
        'vm_name':"",
        'disk_size':8192
    }

    def test_required_fields_missing(self):
        b = builder.VsphereIso()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_iso_checksum_mutually_exclusive(self):
        b = builder.VsphereIso(
                iso_url="/url/to/other/iso",
                iso_urls=["/url/to/iso"],
                iso_checksum_type="sha256",
                iso_checksum="my_checksum",
                iso_checksum_url="my_checksum_url",
                **self.required_defaults
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'VsphereIso: only one of the following can be specified: iso_url, iso_urls' == str(
            excinfo.value)


class TestVSphereCloneBuilder(object):

    def test_required_fields_missing(self):
        b = builder.VsphereClone()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)
