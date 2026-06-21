# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before**
# the student performs any actions.  It deliberately checks only the
# pre-existing resources and does *not* look for any of the output
# artifacts the student is expected to create later on.
#
# Requirements that are verified:
#   1. /home/user/api_test/logs exists and is a directory.
#   2. /home/user/api_test/logs/requests.log
#        • exists, is a regular file, is exactly 38 bytes long
#        • contains the expected byte sequence
#   3. /home/user/api_test/logs/responses.log
#        • exists, is a regular file, is exactly 26 bytes long
#        • contains the expected byte sequence
#
# Any failure message should make it immediately clear what part of the
# initial setup is missing or incorrect.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the expected initial state
# --------------------------------------------------------------------------- #
LOG_DIR = Path("/home/user/api_test/logs")
REQUESTS_LOG = LOG_DIR / "requests.log"
RESPONSES_LOG = LOG_DIR / "responses.log"

EXPECTED_REQUESTS_BYTES = b"GET /users\nPOST /users\nGET /users/123\n"
EXPECTED_RESPONSES_BYTES = b"200 OK\n201 Created\n200 OK\n"

# --------------------------------------------------------------------------- #
# Helper assertions
# --------------------------------------------------------------------------- #
def _assert_file(path: Path, expected_size: int, expected_bytes: bytes) -> None:
    """
    Assert that `path` exists, is a regular file, has the expected size,
    and contains exactly `expected_bytes`.
    """
    assert path.exists(), f"Expected file {path} to exist, but it does not."
    assert path.is_file(), f"Expected {path} to be a regular file."

    actual_size = path.stat().st_size
    assert (
        actual_size == expected_size
    ), f"{path} should be {expected_size} bytes, but is {actual_size} bytes."

    with path.open("rb") as fh:
        data = fh.read()

    assert (
        data == expected_bytes
    ), (
        f"Content of {path} differs from the expected initial content.\n"
        f"Expected bytes ({expected_size} B): {expected_bytes!r}\n"
        f"Actual bytes   ({actual_size} B): {data!r}"
    )

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_logs_directory_exists_and_is_dir():
    """Verify that the logs directory exists and is indeed a directory."""
    assert LOG_DIR.exists(), f"Directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


@pytest.mark.parametrize(
    "file_path, expected_size, expected_bytes",
    [
        (REQUESTS_LOG, 38, EXPECTED_REQUESTS_BYTES),
        (RESPONSES_LOG, 26, EXPECTED_RESPONSES_BYTES),
    ],
)
def test_log_files_presence_and_content(file_path, expected_size, expected_bytes):
    """Check each log file for presence, size, and exact byte-for-byte content."""
    _assert_file(file_path, expected_size, expected_bytes)