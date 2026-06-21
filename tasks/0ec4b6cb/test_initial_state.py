# test_initial_state.py
#
# Pytest suite that verifies the **initial** state of the OS / filesystem
# before the student runs any command.  It asserts the presence of the
# mock-API source file and the absence of any “provision_*” artefacts.
#
# Requirements checked:
#   1. /home/user/mock_api/ directory exists.
#   2. /home/user/mock_api/users.json exists and contains the exact,
#      57-byte JSON payload (no trailing newline).
#   3. /home/user/provision_output/       MUST NOT exist yet.
#   4. /home/user/provision_logs/         MUST NOT exist yet.
#   5. /home/user/provision_output/users_response.json MUST NOT exist yet.
#   6. /home/user/provision_logs/api_test.log          MUST NOT exist yet.
#
# Failures are reported with clear, actionable messages.
#
# NOTE: The tests rely only on the Python standard library and pytest.

import os
import stat
import pytest

# ---------------------------------------------------------------------------
# Constants describing the required initial state
# ---------------------------------------------------------------------------

HOME = "/home/user"
MOCK_API_DIR = os.path.join(HOME, "mock_api")
MOCK_API_FILE = os.path.join(MOCK_API_DIR, "users.json")

PROVISION_OUTPUT_DIR = os.path.join(HOME, "provision_output")
PROVISION_LOGS_DIR = os.path.join(HOME, "provision_logs")
PROVISION_RESPONSE_FILE = os.path.join(PROVISION_OUTPUT_DIR, "users_response.json")
PROVISION_LOG_FILE = os.path.join(PROVISION_LOGS_DIR, "api_test.log")

EXPECTED_JSON_CONTENT = b'{"users":[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]}'
EXPECTED_CONTENT_SIZE = 57  # bytes


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _assert_absent(path: str) -> None:
    """
    Assert that `path` does not exist in the filesystem.
    """
    assert not os.path.exists(path), (
        f"“{path}” should NOT exist before the student runs the curl command, "
        "but it is already present."
    )


def _assert_is_dir(path: str) -> None:
    """
    Assert that `path` exists and is a directory.
    """
    assert os.path.exists(path), f"Required directory “{path}” is missing."
    assert stat.S_ISDIR(os.stat(path).st_mode), f"“{path}” exists but is not a directory."


def _assert_file_with_exact_content(path: str, expected_bytes: bytes) -> None:
    """
    Assert that `path` exists, is a regular file, and its byte content matches
    `expected_bytes` exactly.
    """
    assert os.path.exists(path), f"Required file “{path}” is missing."
    assert stat.S_ISREG(os.stat(path).st_mode), f"“{path}” exists but is not a regular file."
    with open(path, "rb") as fh:
        data = fh.read()
    assert data == expected_bytes, (
        f"File “{path}” does not contain the expected data.\n"
        f"Expected ({len(expected_bytes)} bytes): {expected_bytes!r}\n"
        f"Found    ({len(data)} bytes): {data!r}"
    )
    assert len(data) == EXPECTED_CONTENT_SIZE, (
        f"File “{path}” has unexpected size: "
        f"{len(data)} bytes (expected {EXPECTED_CONTENT_SIZE})."
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_mock_api_directory_exists():
    """Verify that /home/user/mock_api/ directory is present."""
    _assert_is_dir(MOCK_API_DIR)


def test_mock_api_users_json_is_correct():
    """Verify the contents and size of the users.json file."""
    _assert_file_with_exact_content(MOCK_API_FILE, EXPECTED_JSON_CONTENT)


@pytest.mark.parametrize(
    "path",
    [
        PROVISION_OUTPUT_DIR,
        PROVISION_LOGS_DIR,
        PROVISION_RESPONSE_FILE,
        PROVISION_LOG_FILE,
    ],
)
def test_no_provision_artifacts_exist_yet(path):
    """Ensure that no provision_* directories or files exist before the command runs."""
    _assert_absent(path)