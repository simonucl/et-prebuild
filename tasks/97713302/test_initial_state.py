# test_initial_state.py
#
# Pytest suite that verifies the initial filesystem state **before**
# the student’s solution runs.  It checks that the incidents directory
# and the CSV export exist with the correct permissions and contents.
#
# NOTE:  We intentionally do NOT check for the presence (or absence) of any
#        output artefacts such as failed_logins.json or
#        failed_logins_summary.log — those belong to the student’s work.

import os
import stat
import pwd
import pytest

INCIDENTS_DIR = "/home/user/incidents"
CSV_PATH = os.path.join(INCIDENTS_DIR, "auth_failures.csv")

# Expected CSV file content (including the terminating newline)
EXPECTED_CSV_CONTENT = (
    "timestamp,username,source_ip,status\n"
    "2024-05-14T08:41:23Z,alice,192.168.1.10,FAILED\n"
    "2024-05-14T09:02:11Z,bob,10.0.0.3,SUCCESS\n"
    "2024-05-14T10:15:04Z,charlie,172.16.5.5,FAILED\n"
    "2024-05-14T10:45:30Z,alice,192.168.1.10,FAILED\n"
    "2024-05-14T11:00:00Z,dave,203.0.113.99,SUCCESS\n"
)

#####################################################################
# Helper functions
#####################################################################


def _mode(path: str) -> int:
    """
    Return the permission bits (e.g., 0o755) of the given path.
    """
    return stat.S_IMODE(os.stat(path).st_mode)


def _owner(path: str) -> str:
    """
    Return username of file/directory owner.
    """
    return pwd.getpwuid(os.stat(path).st_uid).pw_name


#####################################################################
# Tests
#####################################################################


def test_incidents_directory_exists_and_permissions():
    """
    The /home/user/incidents directory must exist, be a directory,
    be owned by the current user, and have at least 0755 permissions.
    """
    assert os.path.exists(
        INCIDENTS_DIR
    ), f"Required directory {INCIDENTS_DIR} is missing."
    assert os.path.isdir(
        INCIDENTS_DIR
    ), f"{INCIDENTS_DIR} exists but is not a directory."
    # Permissions: exactly 755 is ideal, but 775 or anything more open is
    # also acceptable as long as the execute bit for user is set and read
    # permission for group/other exists.
    mode = _mode(INCIDENTS_DIR)
    expected_mode = 0o755
    assert (
        mode & 0o777 == expected_mode
    ), f"{INCIDENTS_DIR} permissions are {oct(mode)}, expected {oct(expected_mode)}."
    # Ownership
    current_user = pwd.getpwuid(os.getuid()).pw_name
    assert (
        _owner(INCIDENTS_DIR) == current_user
    ), f"{INCIDENTS_DIR} should be owned by '{current_user}'."


def test_auth_failures_csv_exists_and_permissions():
    """
    The CSV export must exist as a regular file with 0644 permissions and
    be owned by the current user.
    """
    assert os.path.exists(
        CSV_PATH
    ), f"Required file {CSV_PATH} is missing."
    assert os.path.isfile(
        CSV_PATH
    ), f"{CSV_PATH} exists but is not a regular file."

    mode = _mode(CSV_PATH)
    expected_mode = 0o644
    assert (
        mode & 0o777 == expected_mode
    ), f"{CSV_PATH} permissions are {oct(mode)}, expected {oct(expected_mode)}."

    current_user = pwd.getpwuid(os.getuid()).pw_name
    assert (
        _owner(CSV_PATH) == current_user
    ), f"{CSV_PATH} should be owned by '{current_user}'."


def test_auth_failures_csv_content_exact_match():
    """
    The CSV file must contain the exact expected rows and terminate with a
    newline.
    """
    with open(CSV_PATH, "r", encoding="utf-8") as fh:
        content = fh.read()

    # Simple equality makes sure everything (including trailing newline)
    # is exactly as expected.
    assert content == EXPECTED_CSV_CONTENT, (
        f"{CSV_PATH} contents do not match the expected fixture.\n"
        "If the file has extra/missing lines, wrong ordering, or is "
        "missing the final newline character, this test will fail."
    )

    # Additional sanity checks (helpful error messages if above equality passes
    # but newline is somehow stripped).
    assert content.endswith(
        "\n"
    ), f"{CSV_PATH} must end with a single newline character."

    # Ensure header row is exactly as specified.
    first_line = content.splitlines()[0]
    assert (
        first_line == "timestamp,username,source_ip,status"
    ), f"CSV header mismatch: found '{first_line}'."