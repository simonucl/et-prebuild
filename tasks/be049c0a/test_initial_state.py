# test_initial_state.py
#
# Pytest suite that verifies the initial on-disk state expected
# BEFORE the student performs any credential-rotation steps.
#
# It checks only the pre-existing artefacts; it deliberately does
# NOT look for the output files that will be produced by the
# student’s solution.

import json
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CREDENTIALS_DIR      = Path("/home/user/credentials")
CREDS_JSON_PATH      = CREDENTIALS_DIR / "creds.json"
CREDS_SCHEMA_PATH    = CREDENTIALS_DIR / "creds_schema.json"

EXPECTED_CREDS_DOC = {
    "user":          "service_account",
    "access_key":    "AKIAOLD123456789",
    "secret_key":    "oldSecretKeyValue",
    "rotation_date": "2022-01-15T10:00:00Z",
}

REQUIRED_FIELDS = {"user", "access_key", "secret_key", "rotation_date"}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _load_json(path: Path):
    """Load and return JSON data from *path*, raising a useful assertion
    if the file cannot be read or parsed."""
    assert path.exists(), f"Expected file does not exist: {path}"
    assert path.is_file(), f"Expected a regular file at {path}, found something else."

    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path} is not valid JSON: {exc}")

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_credentials_directory_exists():
    """The /home/user/credentials directory must exist."""
    assert CREDENTIALS_DIR.exists(), f"Directory missing: {CREDENTIALS_DIR}"
    assert CREDENTIALS_DIR.is_dir(), f"Expected {CREDENTIALS_DIR} to be a directory."


def test_creds_json_present_and_exact_contents():
    """
    1. /home/user/credentials/creds.json must exist.
    2. It must contain exactly the expected 4 fields with the correct values.
    """
    data = _load_json(CREDS_JSON_PATH)

    # All expected keys must be present
    missing_keys = REQUIRED_FIELDS - data.keys()
    assert not missing_keys, (
        f"{CREDS_JSON_PATH} is missing required field(s): {', '.join(sorted(missing_keys))}"
    )

    # There should be no extra keys
    extra_keys = set(data.keys()) - REQUIRED_FIELDS
    assert not extra_keys, (
        f"{CREDS_JSON_PATH} has unexpected extra field(s): {', '.join(sorted(extra_keys))}"
    )

    # Field-by-field exact match
    for key, expected_value in EXPECTED_CREDS_DOC.items():
        assert data[key] == expected_value, (
            f"{CREDS_JSON_PATH}: field '{key}' value mismatch. "
            f"Expected '{expected_value}', found '{data[key]}'"
        )


def test_creds_schema_present_and_minimally_correct():
    """
    1. /home/user/credentials/creds_schema.json must exist and be valid JSON.
    2. It must declare a top-level 'required' array containing the four
       required properties.
    3. For each required property, the schema's 'properties' section must
       specify 'type': 'string'.
    """
    schema = _load_json(CREDS_SCHEMA_PATH)

    # --- Validate 'required' field -----------------------------------------
    assert "required" in schema, (
        f"{CREDS_SCHEMA_PATH} does not contain a top-level 'required' list."
    )
    required = set(schema["required"])
    missing_required = REQUIRED_FIELDS - required
    assert not missing_required, (
        f"{CREDS_SCHEMA_PATH} 'required' list is missing: {', '.join(sorted(missing_required))}"
    )

    # --- Validate 'properties' section -------------------------------------
    assert "properties" in schema, (
        f"{CREDS_SCHEMA_PATH} does not contain a top-level 'properties' map."
    )
    properties = schema["properties"]

    for field in REQUIRED_FIELDS:
        assert field in properties, (
            f"{CREDS_SCHEMA_PATH} 'properties' map does not declare '{field}'."
        )
        prop_schema = properties[field]
        assert prop_schema.get("type") == "string", (
            f"{CREDS_SCHEMA_PATH}: property '{field}' is expected to be "
            f"type 'string' but schema says '{prop_schema.get('type')}'."
        )