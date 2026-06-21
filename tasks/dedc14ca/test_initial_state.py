# test_initial_state.py
#
# This pytest suite verifies that the environment starts in the expected
# initial state *before* the student runs any code.  It checks that the
# required raw data files and the JSON-Schema file exist at their exact
# absolute locations and that their contents are exactly as described in
# the task statement.
#
# IMPORTANT:  In accordance with the grading specification we explicitly
# do NOT look for, nor rely on the (yet-to-be-created) “processed” output
# directory or any of its files.

import json
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants for absolute paths
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/ml_data")
RAW_DIR = BASE_DIR / "raw"
SCHEMA_DIR = BASE_DIR / "schema"

V1_PATH = RAW_DIR / "training_v1.json"
V2_PATH = RAW_DIR / "training_v2.json"
SCHEMA_PATH = SCHEMA_DIR / "record_schema.json"

# ---------------------------------------------------------------------------
# Expected contents (verbatim from the task description)
# ---------------------------------------------------------------------------

EXPECTED_V1 = [
    {"text": "Hello world", "label": "greeting"},
    {"text": "Goodbye", "label": "farewell"},
    {"text": "How are you"},
    {"text": "What's up?", "label": "greeting"},
    {"text": "See you", "label": "farewell"},
]

EXPECTED_V2 = [
    {"text": "Buy now", "label": "advertisement"},
    {"label": "statement"},
    {"text": "Great job!", "label": "praise"},
    {"text": "Error sample"},
    {"text": "Thanks", "label": "gratitude"},
]

EXPECTED_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Training record",
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "label": {"type": "string"},
    },
    "required": ["text", "label"],
    "additionalProperties": False,
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _load_json_file(path: Path):
    """Load a JSON file and return the parsed Python object.

    Fail with a clear message if the file is missing or invalid JSON.
    """
    assert path.exists(), f"Expected file '{path}' is missing."
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        pytest.fail(f"File '{path}' contains invalid JSON: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_raw_files_exist():
    """Raw JSON data files must exist at their exact absolute paths."""
    assert V1_PATH.exists(), f"Required raw data file not found: {V1_PATH}"
    assert V2_PATH.exists(), f"Required raw data file not found: {V2_PATH}"


def test_schema_file_exists():
    """The JSON Schema file must exist at its exact absolute path."""
    assert SCHEMA_PATH.exists(), f"Required schema file not found: {SCHEMA_PATH}"


def test_training_v1_contents():
    """Validate that training_v1.json matches the expected records."""
    data = _load_json_file(V1_PATH)
    assert data == EXPECTED_V1, (
        f"Contents of {V1_PATH} do not match the expected data.\n"
        f"Expected: {EXPECTED_V1}\nActual  : {data}"
    )


def test_training_v2_contents():
    """Validate that training_v2.json matches the expected records."""
    data = _load_json_file(V2_PATH)
    assert data == EXPECTED_V2, (
        f"Contents of {V2_PATH} do not match the expected data.\n"
        f"Expected: {EXPECTED_V2}\nActual  : {data}"
    )


def test_schema_contents():
    """Validate that record_schema.json is exactly as specified."""
    schema = _load_json_file(SCHEMA_PATH)
    assert schema == EXPECTED_SCHEMA, (
        f"Contents of {SCHEMA_PATH} do not match the expected schema.\n"
        f"Expected: {EXPECTED_SCHEMA}\nActual  : {schema}"
    )