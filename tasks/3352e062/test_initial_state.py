# test_initial_state.py
#
# This pytest suite verifies that the *initial* filesystem/OS state
# exactly matches the specification *before* the student’s script runs.
#
# Rules verified:
#   • Required files/directories exist with the correct JSON content.
#   • Only the allowed directories (schema/, incoming/) exist under
#     /home/user/releases – logs/, quarantine/, etc. must NOT exist yet.
#   • Incoming directory contains exactly three JSON descriptors,
#     nothing more, nothing less.
#   • /home/user/releases is writable by the current (non-root) user.
#
# Nothing is written or modified by these tests; they are read-only.

import json
import os
import stat
from pathlib import Path

import pytest

ROOT = Path("/home/user/releases")
SCHEMA_DIR = ROOT / "schema"
INCOMING_DIR = ROOT / "incoming"

SCHEMA_FILE = SCHEMA_DIR / "service-schema.json"

AUTH_FILE = INCOMING_DIR / "service-auth.json"
PAYMENT_FILE = INCOMING_DIR / "service-payment.json"
UI_FILE = INCOMING_DIR / "service-ui.json"

EXPECTED_SCHEMA_JSON = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Microservice build descriptor",
    "type": "object",
    "required": ["service", "version", "commit", "buildDate"],
    "properties": {
        "service": {"type": "string"},
        "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
        "commit": {"type": "string", "minLength": 8, "maxLength": 40},
        "buildDate": {"type": "string", "format": "date-time"},
        "notes": {"type": "string"},
    },
    "additionalProperties": False,
}

EXPECTED_AUTH_JSON = {
    "service": "auth",
    "version": "2.3.4",
    "commit": "1a2b3c4d",
    "buildDate": "2023-08-22T10:15:00Z",
    "notes": "Added support for OAuth2.",
}

EXPECTED_PAYMENT_JSON = {
    "service": "payment",
    "version": "1.19.0",
    "commit": "9d8c7b6a",
    "buildDate": "2023-08-24T14:22:00Z",
}

EXPECTED_UI_JSON = {
    "service": "ui",
    "version": "5.7.1",
    "buildDate": "2023-08-25T08:05:00Z",
    "notes": "UI improvements.",
}


def _load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Required file {path} is missing")
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(f"File {path} does not contain valid JSON: {exc}")


def test_required_directories_exist():
    """schema/ and incoming/ must exist and be directories."""
    assert SCHEMA_DIR.is_dir(), f"Directory {SCHEMA_DIR} is missing"
    assert INCOMING_DIR.is_dir(), f"Directory {INCOMING_DIR} is missing"


def test_no_unexpected_directories_exist():
    """
    No other directories should be present yet under /home/user/releases.
    """
    allowed_dirs = {"schema", "incoming"}
    present_dirs = {p.name for p in ROOT.iterdir() if p.is_dir()}
    unexpected = present_dirs - allowed_dirs
    assert (
        not unexpected
    ), f"Unexpected directories present in {ROOT}: {', '.join(sorted(unexpected))}"


@pytest.mark.parametrize(
    "file_path,expected",
    [
        (SCHEMA_FILE, EXPECTED_SCHEMA_JSON),
    ],
)
def test_schema_file_content(file_path: Path, expected: dict):
    """
    Verify that the schema file exists and its JSON content matches exactly.
    """
    data = _load_json(file_path)
    assert (
        data == expected
    ), f"JSON content mismatch in {file_path}. Expected:\n{expected}\nGot:\n{data}"


@pytest.mark.parametrize(
    "file_path,expected",
    [
        (AUTH_FILE, EXPECTED_AUTH_JSON),
        (PAYMENT_FILE, EXPECTED_PAYMENT_JSON),
        (UI_FILE, EXPECTED_UI_JSON),
    ],
)
def test_incoming_files_content(file_path: Path, expected: dict):
    """
    Incoming directory must contain exactly three JSON descriptors
    with the expected content.
    """
    data = _load_json(file_path)
    assert (
        data == expected
    ), f"JSON content mismatch in {file_path}. Expected:\n{expected}\nGot:\n{data}"


def test_incoming_contains_only_expected_files():
    """No extra or missing files allowed in incoming/."""
    expected_files = {"service-auth.json", "service-payment.json", "service-ui.json"}
    actual_files = {p.name for p in INCOMING_DIR.iterdir() if p.is_file()}
    missing = expected_files - actual_files
    extra = actual_files - expected_files
    assert not missing, f"Missing files in {INCOMING_DIR}: {', '.join(sorted(missing))}"
    assert not extra, f"Unexpected files in {INCOMING_DIR}: {', '.join(sorted(extra))}"


@pytest.mark.parametrize(
    "path",
    [
        ROOT / "logs",
        ROOT / "quarantine",
        ROOT / "release-summary.json",
    ],
)
def test_output_artifacts_do_not_exist_yet(path: Path):
    """Artifacts that are supposed to be created later must NOT exist now."""
    assert not path.exists(), f"{path} should NOT exist before the script runs"


def test_root_is_writable_by_current_user():
    """Current user must have write permission on /home/user/releases."""
    assert os.access(
        ROOT, os.W_OK
    ), f"Directory {ROOT} is not writable by the current user"


def test_permissions_of_existing_items():
    """
    Verify that the initial items have reasonable permissions
    (at least readable by the current user).
    """
    for p in [SCHEMA_DIR, INCOMING_DIR, SCHEMA_FILE, AUTH_FILE, PAYMENT_FILE, UI_FILE]:
        assert p.exists(), f"{p} is missing (checked in permission test)"
        mode = p.stat().st_mode
        assert mode & stat.S_IRUSR, f"{p} is not readable by the owner"