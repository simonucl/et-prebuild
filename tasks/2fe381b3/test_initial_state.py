# test_initial_state.py
#
# This pytest suite verifies the *initial* operating-system / filesystem
# state before the student performs the credential-rotation task.
#
# Expectations (truth values):
#   1. The directory /home/user/cred_rotation **exists**.
#   2. /home/user/cred_rotation/old_creds.json exists and contains the exact
#      JSON document shown in the public task description.
#   3. /home/user/cred_rotation/creds_schema.json exists and contains the exact
#      JSON Schema shown in the public task description.
#   4. /home/user/cred_rotation/new_creds.json must *not* exist yet.
#   5. /home/user/cred_rotation/rotation.log must either not exist or be empty.
#
# If any of these conditions fail, the tests will raise a descriptive
# assertion error so that the student knows what prerequisite is missing.


import json
import re
from pathlib import Path

import pytest


BASE_DIR = Path("/home/user/cred_rotation")
OLD_CREDS_PATH = BASE_DIR / "old_creds.json"
SCHEMA_PATH = BASE_DIR / "creds_schema.json"
NEW_CREDS_PATH = BASE_DIR / "new_creds.json"
ROTATION_LOG_PATH = BASE_DIR / "rotation.log"


@pytest.fixture(scope="module")
def old_creds():
    """Load and return the contents of old_creds.json as a Python dict."""
    try:
        with OLD_CREDS_PATH.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        pytest.fail(f"Expected file {OLD_CREDS_PATH} to exist but it is missing.")
    except json.JSONDecodeError as exc:
        pytest.fail(f"{OLD_CREDS_PATH} is not valid JSON: {exc}")


@pytest.fixture(scope="module")
def creds_schema():
    """Load and return the contents of creds_schema.json as a Python dict."""
    try:
        with SCHEMA_PATH.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        pytest.fail(f"Expected file {SCHEMA_PATH} to exist but it is missing.")
    except json.JSONDecodeError as exc:
        pytest.fail(f"{SCHEMA_PATH} is not valid JSON: {exc}")


def test_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Required directory {BASE_DIR} does not exist. "
        "Create it before running the rotation procedure."
    )


def test_old_creds_content_exact(old_creds):
    expected = {
        "service": "payments-api",
        "environment": "production",
        "credentials": {
            "access_key": "AKIAOLD1234567",
            "secret_key": "oldsecret",
            "created_at": "2023-01-15T08:30:00Z",
            "version": 1,
        },
    }
    assert old_creds == expected, (
        f"{OLD_CREDS_PATH} content differs from the expected initial document."
    )


def test_old_creds_matches_basic_schema_requirements(old_creds):
    # Minimal in-code schema check to ensure the document structure/plausibility.
    assert "credentials" in old_creds, "Missing 'credentials' object in old_creds.json"
    creds = old_creds["credentials"]

    # Check version
    assert creds.get("version") == 1, (
        "The .credentials.version field must be the integer 1 in the initial file."
    )

    # Regex check for access_key
    access_key = creds.get("access_key")
    assert isinstance(access_key, str), "access_key must be a string"
    assert re.fullmatch(r"^AKIA[0-9A-Z]{8,}$", access_key), (
        "access_key does not match the expected AWS-style pattern."
    )

    # created_at should end with 'Z' (UTC ISO-8601)
    created_at = creds.get("created_at")
    assert isinstance(created_at, str), "created_at must be a string"
    assert created_at.endswith("Z"), "created_at must be in UTC ISO-8601 format ending with 'Z'."


def test_schema_content_exact(creds_schema):
    expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["service", "environment", "credentials"],
        "properties": {
            "service": {"type": "string"},
            "environment": {"type": "string"},
            "credentials": {
                "type": "object",
                "required": ["access_key", "secret_key", "created_at", "version"],
                "properties": {
                    "access_key": {
                        "type": "string",
                        "pattern": "^AKIA[0-9A-Z]{8,}$",
                    },
                    "secret_key": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "version": {"type": "integer", "minimum": 1},
                },
            },
        },
    }
    assert creds_schema == expected_schema, (
        f"The JSON Schema in {SCHEMA_PATH} does not match the expected initial schema."
    )


def test_new_creds_not_present_yet():
    assert not NEW_CREDS_PATH.exists(), (
        f"{NEW_CREDS_PATH} already exists, but it should be created *after* "
        "the rotation script runs."
    )


def test_rotation_log_not_present_or_empty():
    if ROTATION_LOG_PATH.exists():
        size = ROTATION_LOG_PATH.stat().st_size
        assert size == 0, (
            f"{ROTATION_LOG_PATH} already exists and is not empty ({size} bytes). "
            "The rotation procedure should append audit lines only after validation."
        )