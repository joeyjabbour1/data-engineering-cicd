"""Unit tests for the storage module (mocked S3, no real AWS)."""

import boto3
import pytest
from moto import mock_aws

from order_pipeline.storage import download_file, list_objects, upload_file

BUCKET = "test-bucket"


@pytest.fixture
def aws_env(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-north-1")
    monkeypatch.setenv("S3_BUCKET", BUCKET)


@mock_aws
def test_upload_and_list(aws_env, tmp_path):
    boto3.client("s3", region_name="eu-north-1").create_bucket(
        Bucket=BUCKET,
        CreateBucketConfiguration={"LocationConstraint": "eu-north-1"},
    )
    local = tmp_path / "orders.csv"
    local.write_text("order_id,amount\n1,50.00\n", encoding="utf-8")

    key = upload_file(str(local), "raw/orders.csv")
    assert key == "raw/orders.csv"
    assert "raw/orders.csv" in list_objects("raw/")


@mock_aws
def test_download(aws_env, tmp_path):
    client = boto3.client("s3", region_name="eu-north-1")
    client.create_bucket(
        Bucket=BUCKET,
        CreateBucketConfiguration={"LocationConstraint": "eu-north-1"},
    )
    client.put_object(Bucket=BUCKET, Key="raw/x.csv", Body=b"data")

    dest = tmp_path / "out.csv"
    download_file("raw/x.csv", str(dest))
    assert dest.read_text() == "data"
