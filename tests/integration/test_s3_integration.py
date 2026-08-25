"""Integration tests: hit the REAL dev S3 bucket. Requires AWS credentials."""

import os

import pytest
from dotenv import load_dotenv

from order_pipeline.storage import download_file, list_objects, upload_file

load_dotenv()

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    not os.environ.get("AWS_ACCESS_KEY_ID"),
    reason="AWS credentials not available",
)
def test_real_s3_roundtrip(tmp_path):
    # upload
    local = tmp_path / "itest.csv"
    local.write_text("order_id,amount\n99,1.00\n", encoding="utf-8")
    key = upload_file(str(local), "raw/_integration_test.csv")
    assert key == "raw/_integration_test.csv"

    # list
    assert "raw/_integration_test.csv" in list_objects("raw/")

    # download back
    dest = tmp_path / "back.csv"
    download_file("raw/_integration_test.csv", str(dest))
    assert dest.read_text() == "order_id,amount\n99,1.00\n"
