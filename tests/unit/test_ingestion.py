"""Unit tests for the ingestion module."""

import json

import pytest

from order_pipeline.exceptions import IngestionError
from order_pipeline.ingestion import ingest_file


def test_ingest_csv_returns_list_of_dicts(tmp_path):
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(
        "order_id,customer_id,amount\n1,C100,50.00\n2,C101,-9.99\n",
        encoding="utf-8",
    )

    result = ingest_file(str(csv_file))

    assert result == [
        {"order_id": "1", "customer_id": "C100", "amount": "50.00"},
        {"order_id": "2", "customer_id": "C101", "amount": "-9.99"},
    ]


def test_ingest_json_returns_list_of_dicts(tmp_path):
    json_file = tmp_path / "orders.json"
    records = [{"order_id": "1", "customer_id": "C100", "amount": "50.00"}]
    json_file.write_text(json.dumps(records), encoding="utf-8")

    result = ingest_file(str(json_file))

    assert result == records


def test_ingest_missing_file_raises(tmp_path):
    with pytest.raises(IngestionError, match="File not found"):
        ingest_file(str(tmp_path / "nope.csv"))


def test_ingest_unsupported_extension_raises(tmp_path):
    bad_file = tmp_path / "data.xml"
    bad_file.write_text("<orders/>", encoding="utf-8")

    with pytest.raises(IngestionError, match="Unsupported file format"):
        ingest_file(str(bad_file))


def test_ingest_json_object_not_list_raises(tmp_path):
    json_file = tmp_path / "single.json"
    json_file.write_text('{"order_id": "1"}', encoding="utf-8")

    with pytest.raises(IngestionError, match="must be a list"):
        ingest_file(str(json_file))


def test_ingest_malformed_json_raises(tmp_path):
    json_file = tmp_path / "broken.json"
    json_file.write_text('[{"order_id": "1",]', encoding="utf-8")

    with pytest.raises(IngestionError):
        ingest_file(str(json_file))
