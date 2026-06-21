# test_initial_state.py
#
# This pytest suite validates that the initial operating-system / filesystem
# state is correct *before* the student performs any actions.
#
# It deliberately avoids checking for any output artifacts that the student
# is expected to create (e.g. /home/user/compliance/api_health.log), in
# accordance with the grading policy.

import os
import stat
import pwd
import pytest

# Constants for paths that must already exist
MOCK_API_DIR = "/home/user/mock_api"
HEALTH_FILE  = "/home/user/mock_api/health.json"

@pytest.fixture(scope="module")
def health_file_contents():
    """Read the health.json file once for reuse in multiple tests."""
    with open(HEALTH_FILE, "r", encoding="utf-8") as fh:
        return fh.read()

def test_mock_api_directory_exists_and_is_accessible():
    assert os.path.isdir(MOCK_API_DIR), (
        f"Required directory {MOCK_API_DIR!r} does not exist or is not a directory."
    )

    # Check that the directory is readable & executable (usable) by current user
    assert os.access(MOCK_API_DIR, os.R_OK | os.X_OK), (
        f"Current user lacks read/execute permission on {MOCK_API_DIR!r}."
    )

def test_health_json_file_exists_with_correct_permissions():
    assert os.path.isfile(HEALTH_FILE), (
        f"Required file {HEALTH_FILE!r} is missing."
    )

    # File must be readable
    assert os.access(HEALTH_FILE, os.R_OK), (
        f"Current user cannot read {HEALTH_FILE!r}."
    )

    # Optional: provide a gentle warning if world-writable (should not be)
    mode = stat.S_IMODE(os.lstat(HEALTH_FILE).st_mode)
    assert not (mode & stat.S_IWOTH), (
        f"{HEALTH_FILE!r} should not be world-writable (mode {oct(mode)})."
    )

def test_health_json_file_content_is_expected(health_file_contents):
    # Strip a single trailing newline if present, but no other whitespace.
    content = health_file_contents.rstrip("\n")
    expected = '{"status":"ok"}'
    assert content == expected, (
        f"{HEALTH_FILE} content mismatch:\n"
        f"Expected: {expected!r}\n"
        f"Found:    {content!r}"
    )