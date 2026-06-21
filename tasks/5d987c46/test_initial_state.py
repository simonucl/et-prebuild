# test_initial_state.py
#
# This pytest suite verifies that the *initial* operating-system state
# exactly matches the specification given to the student *before* they
# create any output artefacts.  It deliberately does **not** look for,
# nor allow, the expected output files/directories that the student will
# generate later on.

import json
import os
from pathlib import Path

import pytest


DATA_DIR = Path("/home/user/data")
OUTPUT_DIR = Path("/home/user/output")

ORDERS_JSON = DATA_DIR / "orders.json"
SCHEMA_JSON = DATA_DIR / "order_schema.json"


# ---------------------------------------------------------------------------
# Helpers ­–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# ---------------------------------------------------------------------------

def _load_json(path: Path):
    """
    Load and return JSON from *path*.  A useful abstraction that allows the
    assertions below to stay readable.
    """
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Ground-truth data (taken verbatim from the specification) ­––––––––––––––––
# ---------------------------------------------------------------------------

_EXPECTED_ORDERS = {
    "orders": [
        {
            "id": 1,
            "customer": {"name": "Alice", "email": "alice@example.com"},
            "total": 250.00,
            "status": "processed",
        },
        {
            "id": 2,
            "customer": {"name": "Bob", "email": "bob@example.com"},
            "total": 65.50,
            "status": "pending",
        },
        {
            "id": 3,
            "customer": {"name": "Carol", "email": "carol@example.com"},
            "total": 120.00,
            "status": "processed",
        },
        {
            "id": 4,
            "customer": {"name": "Dave", "email": "dave@example.com"},
            "total": 85.00,
            "status": "processed",
        },
    ]
}

_EXPECTED_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["orders"],
    "properties": {
        "orders": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "customer", "total", "status"],
                "properties": {
                    "id": {"type": "integer"},
                    "customer": {
                        "type": "object",
                        "required": ["name", "email"],
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string", "format": "email"},
                        },
                    },
                    "total": {"type": "number"},
                    "status": {"type": "string"},
                },
            },
        }
    },
}


# ---------------------------------------------------------------------------
# Tests ­–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# ---------------------------------------------------------------------------

def test_data_directory_exists_and_is_directory():
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."


@pytest.mark.parametrize("path", [ORDERS_JSON, SCHEMA_JSON])
def test_required_files_exist(path):
    assert path.exists(), f"Required file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."
    # Basic sanity check: file must not be empty.
    assert path.stat().st_size > 0, f"File {path} is empty."


def test_orders_json_content_matches_truth():
    content = _load_json(ORDERS_JSON)
    assert content == _EXPECTED_ORDERS, (
        f"Content of {ORDERS_JSON} does not match the expected ground-truth "
        f"data.\nExpected:\n{json.dumps(_EXPECTED_ORDERS, indent=2)}\n\n"
        f"Got:\n{json.dumps(content, indent=2)}"
    )


def test_schema_json_content_matches_truth():
    content = _load_json(SCHEMA_JSON)
    assert content == _EXPECTED_SCHEMA, (
        f"Content of {SCHEMA_JSON} does not match the expected ground-truth "
        f"schema.\nExpected:\n{json.dumps(_EXPECTED_SCHEMA, indent=2)}\n\n"
        f"Got:\n{json.dumps(content, indent=2)}"
    )


def test_output_directory_does_not_preexist():
    """
    The /home/user/output/ directory (and certainly any of the expected
    artefacts) must *not* exist prior to the student's work.  Its presence
    would indicate that the environment is already “polluted”.
    """
    assert not OUTPUT_DIR.exists(), (
        f"Output directory {OUTPUT_DIR} should not exist before the exercise "
        "starts.  Please reset the environment."
    )