"""Ingestion module: reads raw CSV/JSON files into a list of records."""

import csv
import json
from pathlib import Path

from order_pipeline.exceptions import IngestionError


def ingest_file(file_path: str) -> list[dict]:
    """
    Read a CSV or JSON file into a list of dict records.

    Ingestion reads data "as-is" - it does NOT validate content
    (negative amounts, missing fields, etc. pass through untouched).
    It only fails if the file cannot be structurally read.

    Args:
        file_path: Path to a .csv or .json file.

    Returns:
        A list of dictionaries, one per record.

    Raises:
        IngestionError: if the file is missing, unreadable, malformed,
                        or has an unsupported extension.
    """
    path = Path(file_path)

    if not path.exists():
        raise IngestionError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    try:
        if suffix == ".csv":
            with path.open(mode="r", encoding="utf-8", newline="") as f:
                return list(csv.DictReader(f))

        elif suffix == ".json":
            with path.open(mode="r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise IngestionError(
                    f"JSON must be a list of records, got {type(data).__name__}"
                )
            return data

        else:
            raise IngestionError(f"Unsupported file format: {suffix}")

    except (OSError, csv.Error, json.JSONDecodeError) as exc:
        raise IngestionError(f"Failed to read {file_path}: {exc}") from exc