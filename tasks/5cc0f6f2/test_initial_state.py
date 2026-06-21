# test_initial_state.py
#
# Pytest suite that validates the operating-system state **before** the
# student runs any solution code for the “historical-configuration audit”.
#
# The tests assert that:
#   • The expected directory tree and *.conf files exist.
#   • Each “old” file (the ones that must be backed-up later) has an mtime
#     strictly greater than 30 days in the past, while the “recent” files do
#     not.
#   • The byte contents of the four “old” files match the specification.
#
# NOTE:  As required, we deliberately do *not* check for the presence or
#        absence of any output artifacts such as “.old” backup files or
#        compliance log directories/files.

import os
import stat
import time
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial filesystem state
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/audit_targets")

OLD_FILES = {
    "/home/user/audit_targets/webserver/httpd.conf": b"ServerName localhost\nListen 80\n",
    "/home/user/audit_targets/db/mysql.conf": b"[mysqld]\nport=3306\n",
    "/home/user/audit_targets/app/settings/app.conf": b"debug=false\napi_key=XYZ123\n",
    "/home/user/audit_targets/app/archive/oldapp.conf": b"version=1.2.3\n",
}

NEW_FILES = [
    "/home/user/audit_targets/webserver/newhttpd.conf",
    "/home/user/audit_targets/app/settings/recent.conf",
]

SECONDS_IN_DAY = 24 * 60 * 60
THIRTY_DAYS = 30 * SECONDS_IN_DAY


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _stat(path: str) -> os.stat_result:
    """Return os.stat, raising AssertionError with helpful message if fails."""
    try:
        return os.stat(path)
    except FileNotFoundError:
        pytest.fail(f"Expected path does not exist: {path}", pytrace=False)


def _mtime(path: str) -> float:
    """Convenience wrapper to obtain modification time."""
    return _stat(path).st_mtime


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_base_directory_exists():
    assert BASE_DIR.is_dir(), f"Missing base directory: {BASE_DIR}"


@pytest.mark.parametrize("file_path", list(OLD_FILES.keys()) + NEW_FILES)
def test_conf_files_exist(file_path):
    path = Path(file_path)
    assert path.is_file(), f"Required file is missing: {file_path}"


def test_old_file_contents():
    """
    The four historical *.conf files must contain *exactly* the bytes
    stipulated in the task description.  This guarantees the grader is
    working against the correct fixture data.
    """
    for path_str, expected_bytes in OLD_FILES.items():
        path = Path(path_str)
        with path.open("rb") as fp:
            actual = fp.read()
        assert (
            actual == expected_bytes
        ), f"Content mismatch for {path_str!s}.\nExpected:\n{expected_bytes!r}\nGot:\n{actual!r}"


def test_mtime_classification():
    """
    Validate that files expected to be 'old' really are strictly older than
    30 days, and that the 'recent' ones are NOT older than 30 days.
    """
    now = time.time()

    # Old files should satisfy  (now - mtime) > 30 days
    for path in OLD_FILES.keys():
        age = now - _mtime(path)
        assert (
            age > THIRTY_DAYS
        ), f"File {path} should be older than 30 days but is only {age / SECONDS_IN_DAY:.2f} days old."

    # New files should satisfy  (now - mtime) <= 30 days
    for path in NEW_FILES:
        age = now - _mtime(path)
        assert (
            age <= THIRTY_DAYS
        ), f"File {path} should be newer than or equal to 30 days but is {age / SECONDS_IN_DAY:.2f} days old."


def test_directory_structure_for_all_files():
    """
    Ensure that every ancestor directory of each expected file exists.
    This guards against cases where an intermediate directory is missing.
    """
    all_files = list(OLD_FILES.keys()) + NEW_FILES
    for file_path in all_files:
        path_obj = Path(file_path)
        parents = list(path_obj.parents)
        # The first parent is the directory containing the file; check all up to /home/user
        for directory in parents:
            if directory == Path("/"):
                break
            assert directory.is_dir(), f"Missing expected directory: {directory}"
            if directory == Path("/home/user"):
                break