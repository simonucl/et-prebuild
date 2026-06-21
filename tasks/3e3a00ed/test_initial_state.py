# test_initial_state.py
#
# This pytest suite validates the initial state of the filesystem and
# environment _before_ the student runs any commands for the exercise
# “Retrieve local backup status via curl and archive it”.
#
# It checks only pre-existing assets; it does NOT look for—nor require the
# absence of—any of the files the student is expected to create later.

import json
import shutil
from pathlib import Path

import pytest


# Constants used by all tests
MOCK_JSON_PATH = Path("/home/user/mock_backup_api.json")


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _read_text(p: Path) -> str:
    """
    Read text from *p* using UTF-8 with universal newlines.  Any error is raised
    to the caller (pytest will surface it).
    """
    return p.read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_curl_is_installed():
    """curl must be available in PATH so the learner can use it."""
    curl_path = shutil.which("curl")
    assert curl_path is not None, (
        "The command-line tool 'curl' is not installed or not discoverable in "
        "the PATH.  Install it or fix PATH before the exercise is attempted."
    )


def test_mock_json_file_exists_and_is_file():
    """
    The staged source data must already be present at the exact expected path.
    """
    assert MOCK_JSON_PATH.exists(), (
        f"Required source file not found at {MOCK_JSON_PATH!s}.  "
        "The exercise cannot proceed without this payload."
    )
    assert MOCK_JSON_PATH.is_file(), (
        f"Expected {MOCK_JSON_PATH!s} to be a file, but it is not."
    )


def test_mock_json_file_is_readable_and_valid_json():
    """
    Verify the staged file is readable and contains valid JSON with the
    expected top-level keys.
    """
    # Read file
    try:
        raw = _read_text(MOCK_JSON_PATH)
    except Exception as exc:  # pragma: no cover
        pytest.fail(
            f"Unable to read {MOCK_JSON_PATH!s}: {exc}",
            pytrace=False,
        )

    # Parse JSON
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(
            f"{MOCK_JSON_PATH!s} is not valid JSON: {exc}",
            pytrace=False,
        )

    # Minimal schema validation: ensure required keys exist
    required_keys = {"backup_id", "status", "duration_seconds", "size_bytes"}
    missing = required_keys.difference(data)
    assert not missing, (
        f"{MOCK_JSON_PATH!s} is missing expected JSON key(s): {', '.join(missing)}"
    )