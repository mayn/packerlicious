import pytest

import packerlicious.builder as builder


class TestAmazonInstanceBuilder(object):

    def test_required_fields_missing(self):
        b = builder.AmazonInstance()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_exactly_one_source_ami(self):
        b = builder.AmazonInstance(
            account_id="...",
            access_key="dummy-access-key",
            secret_key="dummy-secret-key",
            instance_type="t2.micro",
            ami_name="ami-result",
            region="us-east-1",
            s3_bucket="...",
            x509_cert_path="...",
            x509_key_path="...",
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonInstance: one of the following must be specified: source_ami, source_ami_filter' == str(excinfo.value)

    def test_mutually_exclusive_security_group_ami(self):
        b = builder.AmazonInstance(
            account_id="...",
            access_key="dummy-access-key",
            secret_key="dummy-secret-key",
            instance_type="t2.micro",
            ami_name="ami-result",
            region="us-east-1",
            source_ami="dummy-source-ami",
            s3_bucket="...",
            x509_cert_path="...",
            x509_key_path="...",
            security_group_id="sg-123",
            security_group_ids=["sg-123", "sg-456"],
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonInstance: only one of the following can be specified: security_group_id, security_group_ids' == str(excinfo.value)


class TestAmazonEbsBuilder(object):

    def test_required_fields_missing(self):
        b = builder.AmazonEbs()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_exactly_one_source_ami(self):
        b = builder.AmazonEbs(
            access_key="dummy-access-key",
            secret_key="dummy-secret-key",
            instance_type="t2.micro",
            ami_name="ami-result",
            region="us-east-1",
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonEbs: one of the following must be specified: source_ami, source_ami_filter' == str(excinfo.value)

    def test_mutually_exclusive_security_group_ami(self):
        b = builder.AmazonEbs(
            access_key="dummy-access-key",
            secret_key="dummy-secret-key",
            instance_type="t2.micro",
            ami_name="ami-result",
            region="us-east-1",
            source_ami="dummy-source-ami",
            security_group_id="sg-123",
            security_group_ids=["sg-123", "sg-456"],
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonEbs: only one of the following can be specified: security_group_id, security_group_ids' == str(excinfo.value)

class TestAmazonChroot(object):

    def test_required_fields_missing(self):
        b = builder.AmazonChroot()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_exactly_one_source_ami(self):
        b = builder.AmazonChroot(
            ami_name  ="some-ami",
            access_key="dummy-access-key",
            secret_key="dummy-secret-key",
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonChroot: one of the following must be specified: source_ami, source_ami_filter' == str(excinfo.value)

    def test_exactly_one_source_ami_when_from_scratch_is_false(self):
        b = builder.AmazonChroot(
            ami_name  ="some-ami",
            access_key="dummy-access-key",
            secret_key="dummy-secret-key",
            from_scratch="false"
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonChroot: one of the following must be specified: source_ami, source_ami_filter' == str(excinfo.value)

    def test_required_fields_when_from_scratch_is_true(self):
        b = builder.AmazonChroot(
            ami_name  ="some-ami",
            access_key="dummy-access-key",
            secret_key="dummy-secret-key",
            from_scratch="true"
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonChroot: when from_config is True, source_ami is ' \
               'ignored and ami_virtualization_type, pre_mount_commands, ' \
               'root_volume_size options are required' == str(excinfo.value)


class TestAmazonEbsSurrogate(object):

    def test_required_fields_missing(self):
        b = builder.AmazonEbsSurrogate()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_exactly_one_source_ami(self):
        ami_root_dev = builder.BlockDeviceMapping()
        b = builder.AmazonEbsSurrogate(
            access_key="dummy-access-key",
            secret_key="dummy-secret-key",
            instance_type="t2.micro",
            source_device_name="some_device",
            region="us-east-1",
            ami_root_device=[ami_root_dev],
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonEbsSurrogate: one of the following must be specified: source_ami, source_ami_filter' == str(excinfo.value)

    def test_mutually_exclusive_security_group_ami(self):
        ami_root_dev = builder.BlockDeviceMapping()
        b = builder.AmazonEbsSurrogate(
            access_key="dummy-access-key",
            secret_key="dummy-secret-key",
            instance_type="t2.micro",
            source_device_name="some_device",
            region="us-east-1",
            ami_root_device=[ami_root_dev],
            source_ami="dummy-source-ami",
            security_group_id="sg-123",
            security_group_ids=["sg-123", "sg-456"],
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonEbsSurrogate: only one of the following can be specified: security_group_id, security_group_ids' == str(excinfo.value)

class TestAmazonEbsVolume(object):

    def test_required_fields_missing(self):
        b = builder.AmazonEbsVolume()

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'required' in str(excinfo.value)

    def test_exactly_one_source_ami(self):
        b = builder.AmazonEbsVolume(
            access_key="dummy-access-key",
            secret_key="dummy-secret-key",
            instance_type="t2.micro",
            region="us-east-1",
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonEbsVolume: one of the following must be specified: source_ami, source_ami_filter' == str(excinfo.value)

    def test_mutually_exclusive_security_group_ami(self):
        b = builder.AmazonEbsVolume(
            access_key="dummy-access-key",
            secret_key="dummy-secret-key",
            instance_type="t2.micro",
            region="us-east-1",
            source_ami="dummy-source-ami",
            security_group_id="sg-123",
            security_group_ids=["sg-123", "sg-456"],
        )

        with pytest.raises(ValueError) as excinfo:
            b.to_dict()
        assert 'AmazonEbsVolume: only one of the following can be specified: security_group_id, security_group_ids' == str(excinfo.value)
