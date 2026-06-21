# test_initial_state.py
#
# This pytest suite validates the initial on-disk workspace *before* the student
# starts working.  It checks only the stub materials that must already be
# present and explicitly avoids looking for any of the artefacts that the
# student is expected to create later.
#
# Tested paths (all must exist **before** the exercise begins):
#   /home/user/etl/
#       ├── raw/events.json      (array with 5 event objects)
#       └── schema/event_schema.json  (Draft-07 JSON Schema for the events)
#
# Nothing else is inspected so as not to interfere with the student’s work.
#
# The assertions give clear, actionable error messages if something is missing
# or malformed.

import json
from pathlib import Path

import pytest

ETL_ROOT = Path("/home/user/etl")
RAW_EVENTS_PATH = ETL_ROOT / "raw" / "events.json"
SCHEMA_PATH = ETL_ROOT / "schema" / "event_schema.json"


@pytest.fixture(scope="module")
def events_data():
    """Load and return the JSON array from raw/events.json."""
    try:
        raw_txt = RAW_EVENTS_PATH.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        pytest.fail(f"Required file missing: {RAW_EVENTS_PATH}", pytrace=False)
    try:
        data = json.loads(raw_txt)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{RAW_EVENTS_PATH} is not valid JSON: {exc}", pytrace=False)
    if not isinstance(data, list):
        pytest.fail(f"{RAW_EVENTS_PATH} must contain a JSON array, got {type(data).__name__}",
                    pytrace=False)
    return data


@pytest.fixture(scope="module")
def schema_data():
    """Load and return the JSON schema object."""
    try:
        raw_txt = SCHEMA_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file missing: {SCHEMA_PATH}", pytrace=False)
    try:
        data = json.loads(raw_txt)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{SCHEMA_PATH} is not valid JSON: {exc}", pytrace=False)
    if not isinstance(data, dict):
        pytest.fail(f"{SCHEMA_PATH} must contain a JSON object, got {type(data).__name__}",
                    pytrace=False)
    return data


def test_directory_structure():
    """Ensure the base directory and the raw/schema sub-directories exist."""
    assert ETL_ROOT.is_dir(), f"Expected directory missing: {ETL_ROOT}"
    assert (ETL_ROOT / "raw").is_dir(), f"Expected directory missing: {ETL_ROOT / 'raw'}"
    assert (ETL_ROOT / "schema").is_dir(), f"Expected directory missing: {ETL_ROOT / 'schema'}"


def test_raw_events_file_exists_and_is_readable():
    """Check that raw/events.json exists and is a regular file."""
    assert RAW_EVENTS_PATH.is_file(), f"Required file missing: {RAW_EVENTS_PATH}"
    # A separate read happens in the events_data fixture, so we simply assert here.


def test_raw_events_json_structure(events_data):
    """Validate high-level structure of events.json (array length & required keys)."""
    assert len(events_data) == 5, (
        f"{RAW_EVENTS_PATH} should contain exactly 5 event objects; found {len(events_data)}."
    )

    required_keys = {"id", "timestamp", "type", "payload"}
    for idx, event in enumerate(events_data, start=1):
        assert isinstance(event, dict), (
            f"Element #{idx} in {RAW_EVENTS_PATH} is not a JSON object."
        )
        missing = required_keys - event.keys()
        assert not missing, (
            f"Element #{idx} in {RAW_EVENTS_PATH} is missing required keys: {', '.join(sorted(missing))}"
        )


def test_raw_events_expected_content(events_data):
    """Verify that the raw events exactly match the specification given in the task."""
    expected_events = [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "timestamp": "2023-06-01T12:00:00Z",
            "type": "click",
            "payload": {"element_id": "btn_signup"},
        },
        {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "timestamp": "2023-06-01T12:05:00Z",
            "type": "view",
            "payload": {"page": "/home"},
        },
        {
            "id": "not-a-uuid",
            "timestamp": "2023-06-01T12:10:00Z",
            "type": "purchase",
            "payload": {"amount": 19.99},
        },
        {
            "id": "123e4567-e89b-12d3-a456-426614174002",
            "timestamp": "invalid-date",
            "type": "click",
            "payload": {"element_id": "btn_login"},
        },
        {
            "id": "123e4567-e89b-12d3-a456-426614174003",
            "timestamp": "2023-06-01T12:15:00Z",
            "type": "purchase",
            "payload": {"amount": 49.99},
        },
    ]
    assert events_data == expected_events, (
        f"The contents of {RAW_EVENTS_PATH} do not match the expected starter data."
    )


def test_schema_file_exists_and_is_readable():
    """Check that schema/event_schema.json exists and is a regular file."""
    assert SCHEMA_PATH.is_file(), f"Required file missing: {SCHEMA_PATH}"


def test_schema_content(schema_data):
    """Lightweight sanity checks on the JSON Schema file."""
    assert schema_data.get("$schema") == "http://json-schema.org/draft-07/schema#", (
        f"{SCHEMA_PATH} does not declare draft-07 meta-schema."
    )
    assert schema_data.get("type") == "object", (
        f"{SCHEMA_PATH} top-level 'type' should be 'object'."
    )
    required = schema_data.get("required", [])
    for key in ("id", "timestamp", "type", "payload"):
        assert key in required, (
            f"{SCHEMA_PATH} should require field '{key}' but it does not."
        )