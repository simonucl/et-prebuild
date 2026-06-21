# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state for the “credential rotation” exercise.  These checks must pass
# *before* the student performs any action.

import json
import os
from pathlib import Path

# Absolute paths used throughout the tests
ROOT_DIR = Path("/home/user/credential_rotation")
TOKEN_FILE = ROOT_DIR / "new_token.txt"
FAKE_ENDPOINT_FILE = ROOT_DIR / "fake_endpoint.json"
LOG_FILE = ROOT_DIR / "rotation_check.log"


def test_credential_rotation_directory_exists():
    """The /home/user/credential_rotation directory must exist and be a directory."""
    assert ROOT_DIR.exists(), (
        f"Required directory {ROOT_DIR} is missing.  "
        "The exercise cannot proceed without it."
    )
    assert ROOT_DIR.is_dir(), (
        f"{ROOT_DIR} exists but is not a directory.  "
        "Ensure it is created as a directory."
    )


def test_new_token_file_content():
    """
    new_token.txt must exist, be a regular file, and contain exactly the expected
    token followed by a single newline.
    """
    expected_content = "SECURE-TOKEN-998877\n"

    assert TOKEN_FILE.exists(), (
        f"Required file {TOKEN_FILE} is missing."
    )
    assert TOKEN_FILE.is_file(), (
        f"{TOKEN_FILE} exists but is not a regular file."
    )

    actual_content = TOKEN_FILE.read_text(encoding="utf-8")
    assert actual_content == expected_content, (
        f"{TOKEN_FILE} content mismatch.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Found:    {repr(actual_content)}"
    )


def test_fake_endpoint_json_content():
    """
    fake_endpoint.json must exist, be valid JSON, contain a dict with
    {'result': 'success'}, and end with a single newline character.
    """
    assert FAKE_ENDPOINT_FILE.exists(), (
        f"Required file {FAKE_ENDPOINT_FILE} is missing."
    )
    assert FAKE_ENDPOINT_FILE.is_file(), (
        f"{FAKE_ENDPOINT_FILE} exists but is not a regular file."
    )

    raw = FAKE_ENDPOINT_FILE.read_text(encoding="utf-8")
    # Check that the file ends with exactly one '\n'
    assert raw.endswith("\n"), (
        f"{FAKE_ENDPOINT_FILE} must end with exactly one newline (\\n)."
    )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"{FAKE_ENDPOINT_FILE} does not contain valid JSON: {exc}"
        ) from exc

    assert isinstance(data, dict), (
        f"{FAKE_ENDPOINT_FILE} JSON must be an object/dict."
    )

    expected_result = "success"
    actual_result = data.get("result")
    assert actual_result == expected_result, (
        f"{FAKE_ENDPOINT_FILE} must contain {{'result': '{expected_result}'}}.\n"
        f"Found: {data}"
    )


def test_rotation_check_log_does_not_exist_initially():
    """
    rotation_check.log must NOT exist before the student runs their solution.
    Its presence would indicate that the exercise has been attempted already.
    """
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists, but the student has not performed the "
        "required curl command yet.  Ensure the environment is clean."
    )