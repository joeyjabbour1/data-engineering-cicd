"""S3 storage module: upload/download/list objects for the order pipeline."""

import os

import boto3
from botocore.exceptions import ClientError

from order_pipeline.exceptions import OrderPipelineError


class StorageError(OrderPipelineError):
    """Raised when an S3 operation fails."""


def get_s3_client():
    """Create an S3 client from environment credentials."""
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ.get("AWS_DEFAULT_REGION", "eu-north-1"),
    )


def upload_file(local_path: str, key: str, bucket: str | None = None) -> str:
    """Upload a local file to S3. Returns the destination key."""
    bucket = bucket or os.environ["S3_BUCKET"]
    client = get_s3_client()
    try:
        client.upload_file(local_path, bucket, key)
        return key
    except ClientError as exc:
        raise StorageError(
            f"Failed to upload {local_path} to {bucket}/{key}: {exc}"
        ) from exc


def download_file(key: str, local_path: str, bucket: str | None = None) -> str:
    """Download an S3 object to a local path. Returns the local path."""
    bucket = bucket or os.environ["S3_BUCKET"]
    client = get_s3_client()
    try:
        client.download_file(bucket, key, local_path)
        return local_path
    except ClientError as exc:
        raise StorageError(f"Failed to download {bucket}/{key}: {exc}") from exc


def list_objects(prefix: str = "", bucket: str | None = None) -> list[str]:
    """List object keys under a prefix. Returns a list of keys."""
    bucket = bucket or os.environ["S3_BUCKET"]
    client = get_s3_client()
    try:
        response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return [obj["Key"] for obj in response.get("Contents", [])]
    except ClientError as exc:
        raise StorageError(f"Failed to list {bucket}/{prefix}: {exc}") from exc
