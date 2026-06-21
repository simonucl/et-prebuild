# test_initial_state.py
# Pytest suite that validates the *initial* operating-system / filesystem state
# for the "local API smoke-test" exercise.
#
# DO NOT check for the output artefact (/home/user/api_test.log); the purpose of
# this file is to make sure the *inputs* are in place **before** the student
# runs their solution.

import os
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants describing the expected initial state
# --------------------------------------------------------------------------- #
API_DIR = Path("/home/user/simple_api")
USERS_JSON = API_DIR / "users.json"
STATUS_JSON = API_DIR / "status.json"

# Exact byte-lengths that curl will return (taken from the task description)
USERS_JSON_BYTES = 84
STATUS_JSON_BYTES = 38


# --------------------------------------------------------------------------- #
# Helper(s)
# --------------------------------------------------------------------------- #
def _assert_file(path: Path, expected_size: int) -> None:
    """
    Assert that a file exists, is readable, and has the exact byte-size
    specified by *expected_size*.
    """
    # 1. Existence and type
    assert path.exists(), f"Required file missing: {path!s}"
    assert path.is_file(), f"Expected {path!s} to be a file, but it is not."

    # 2. Readability
    try:
        data = path.read_bytes()
    except Exception as exc:  # pragma: no cover
        assert False, f"Could not read {path!s}: {exc}"

    # 3. Exact byte count
    actual_size = len(data)
    assert (
        actual_size == expected_size
    ), (
        f"{path!s} size mismatch: expected {expected_size} bytes, "
        f"found {actual_size} bytes."
    )


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_simple_api_directory_exists():
    """
    The directory /home/user/simple_api must exist and be a directory.
    """
    assert API_DIR.exists(), f"Directory missing: {API_DIR!s}"
    assert API_DIR.is_dir(), f"{API_DIR!s} exists but is not a directory."


def test_users_json_present_and_correct_size():
    """
    Verify /home/user/simple_api/users.json exists and is exactly 84 bytes.
    """
    _assert_file(USERS_JSON, USERS_JSON_BYTES)


def test_status_json_present_and_correct_size():
    """
    Verify /home/user/simple_api/status.json exists and is exactly 38 bytes.
    """
    _assert_file(STATUS_JSON, STATUS_JSON_BYTES)