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
