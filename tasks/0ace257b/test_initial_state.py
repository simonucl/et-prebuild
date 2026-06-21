# test_initial_state.py
"""
Pytest suite to validate the initial state of the filesystem **before**
any student action is taken for the “localization engineer” task.

This test file checks that:
1. The project directory exists.
2. The English source JSON file exists with the exact expected content and
   no trailing newline.
3. The French translation and audit-log **do not yet exist**.
4. The `curl` executable is available (needed for the first task step).

Only the Python standard library and pytest are used.
"""

import os
import shutil
import pathlib
import pytest

# Constants for paths and expected content
PROJECT_DIR = pathlib.Path("/home/user/project")
EN_JSON = PROJECT_DIR / "translations_en.json"
FR_JSON = PROJECT_DIR / "translations_fr.json"
AUDIT_LOG = PROJECT_DIR / "translation_update.log"

EXPECTED_EN_CONTENT = '{"greeting":"Hello","farewell":"Goodbye"}'


def test_project_directory_exists():
    """Ensure /home/user/project directory is present."""
    assert PROJECT_DIR.is_dir(), (
        f"Required directory {PROJECT_DIR} is missing."
    )


def test_english_json_exists_with_exact_content():
    """Check that translations_en.json exists with exact single-line content."""
    assert EN_JSON.is_file(), (
        f"Required file {EN_JSON} is missing."
    )

    with EN_JSON.open("rb") as f:
        data = f.read()

    # Decode as UTF-8 without errors
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{EN_JSON} is not valid UTF-8: {exc}")  # pragma: no cover

    assert text == EXPECTED_EN_CONTENT, (
        f"Content of {EN_JSON} does not match expected.\n"
        f"Expected: {EXPECTED_EN_CONTENT!r}\n"
        f"Got:      {text!r}"
    )


def test_no_trailing_newline_in_english_json():
    """Ensure there is no trailing newline in translations_en.json."""
    with EN_JSON.open("rb") as f:
        data = f.read()

    assert not data.endswith(b"\n"), (
        f"{EN_JSON} should NOT end with a newline character."
    )


def test_french_json_absent_initially():
    """translations_fr.json should NOT exist before student action."""
    assert not FR_JSON.exists(), (
        f"{FR_JSON} should NOT exist in the initial state."
    )


def test_audit_log_absent_initially():
    """translation_update.log should NOT exist before student action."""
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} should NOT exist in the initial state."
    )


def test_curl_available_in_path():
    """Verify that the `curl` executable is available for the student."""
    curl_path = shutil.which("curl")
    assert curl_path is not None and os.access(curl_path, os.X_OK), (
        "The `curl` executable is required but was not found in PATH."
    )