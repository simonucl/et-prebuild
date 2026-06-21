# test_initial_state.py
#
# This pytest suite verifies that the starting filesystem state
# is exactly as expected **before** the student carries out the
# three subtasks described in the exercise.
#
# IMPORTANT:  The tests intentionally avoid mentioning or checking
# for any output artefacts (slow_queries.json, validation.log, …).
#
# Only Python’s standard library and pytest are used.

import json
import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/db_metrics")
METRICS_FILE = BASE_DIR / "query_metrics.json"
SCHEMA_FILE = BASE_DIR / "query_metrics_schema.json"

# What the query_metrics.json file must contain.
EXPECTED_QUERY_METRICS = {
    "queries": [
        {
            "id": "Q123",
            "statement": "SELECT * FROM users;",
            "execution_time_ms": 153,
        },
        {
            "id": "Q124",
            "statement": "UPDATE orders SET status='SHIPPED' WHERE id=100;",
            "execution_time_ms": 2345,
        },
        {
            "id": "Q125",
            "statement": "DELETE FROM sessions WHERE last_active < NOW() - INTERVAL '30 days';",
            "execution_time_ms": 1820,
        },
        {
            "id": "Q126",
            "statement": "SELECT * FROM transactions WHERE amount > 1000;",
            "execution_time_ms": 2890,
        },
    ]
}

# Minimal expectations for the schema file.  We don’t need full JSON-Schema
# validation logic here; we just ensure the structure matches what was
# promised in the task description.
EXPECTED_SCHEMA_ROOT_KEYS = {
    "$schema",
    "title",
    "type",
    "required",
    "properties",
}

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _load_json(path: Path):
    """Load a JSON file, yielding python data or raising an informative error."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Expected file is missing: {path}")
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(f"{path} is not valid JSON: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_base_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Directory {BASE_DIR} is required but was not found. "
        "Create it and place the input files inside."
    )


def test_metrics_file_exists_and_matches_expected():
    assert METRICS_FILE.is_file(), (
        f"The metrics file {METRICS_FILE} is missing. "
        "It must be present before the student begins."
    )

    data = _load_json(METRICS_FILE)
    assert data == EXPECTED_QUERY_METRICS, (
        f"The contents of {METRICS_FILE} do not match the expected initial "
        "dataset. Make sure the file is unmodified from the original state."
    )


def test_schema_file_exists_and_has_minimal_shape():
    assert SCHEMA_FILE.is_file(), (
        f"The schema file {SCHEMA_FILE} is missing. "
        "It must be present before the student begins."
    )

    schema = _load_json(SCHEMA_FILE)

    missing_keys = EXPECTED_SCHEMA_ROOT_KEYS - schema.keys()
    assert not missing_keys, (
        f"The schema file {SCHEMA_FILE} is incomplete. "
        f"Missing top-level keys: {', '.join(sorted(missing_keys))}"
    )

    # Additional sanity checks that provide clearer feedback if things drift.
    assert schema["type"] == "object", (
        f"{SCHEMA_FILE}: top-level 'type' must be 'object'."
    )
    assert "queries" in schema["required"], (
        f"{SCHEMA_FILE}: 'queries' must be listed in the top-level 'required' array."
    )
    assert "queries" in schema["properties"], (
        f"{SCHEMA_FILE}: top-level 'properties' must define 'queries'."
    )