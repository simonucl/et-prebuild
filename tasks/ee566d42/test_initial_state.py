# test_initial_state.py
#
# This pytest suite validates that the **initial** filesystem state
# (before the student runs any commands) matches the specification that
# the automated grader relies on.
#
# It checks only the pre-existing “/home/user/data/**” area and makes
# NO assertions about any output artefacts the student is supposed to
# create later (e.g. /home/user/security_scan or its CSV file).

import os
import stat
import pytest

# --------------------------------------------------------------------
# Test data taken from the task’s “truth value”
# --------------------------------------------------------------------

DIRECTORIES = [
    "/home/user/data",
    "/home/user/data/logs",
    "/home/user/data/backup",
    "/home/user/data/public",
    "/home/user/data/private",
]

FILES = [
    # (path, expected_size_bytes, expected_octal_permissions)
    ("/home/user/data/logs/app.log",     62_914_560, 0o666),
    ("/home/user/data/backup/db.dump",  125_829_120, 0o600),
    ("/home/user/data/public/video.mp4", 73_400_320, 0o666),
    ("/home/user/data/public/readme.txt",      1024, 0o666),
    ("/home/user/data/private/secret.txt", 57_671_680, 0o600),
]

# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------

def get_permission_bits(path: str) -> int:
    """
    Return the permission bits of `path` as an int such that 0o666 == rw-rw-rw-.
    """
    st_mode = os.lstat(path).st_mode
    return stat.S_IMODE(st_mode)

# --------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------

@pytest.mark.parametrize("directory", DIRECTORIES)
def test_required_directories_exist(directory):
    assert os.path.isdir(directory), (
        f"Required directory missing: {directory!r}. "
        "The grading script expects it to be present before the task starts."
    )

@pytest.mark.parametrize("path, expected_size, expected_perms", FILES)
def test_required_files_exist_with_correct_attributes(path, expected_size, expected_perms):
    # 1) File must exist and be a regular file
    assert os.path.isfile(path), f"Required file missing or not a regular file: {path!r}"

    # 2) Size must match exactly
    actual_size = os.path.getsize(path)
    assert actual_size == expected_size, (
        f"File {path!r} has size {actual_size} bytes, "
        f"but {expected_size} bytes were expected."
    )

    # 3) Permission bits must match exactly the expected octal value
    actual_perms = get_permission_bits(path)
    assert actual_perms == expected_perms, (
        f"File {path!r} has permissions {oct(actual_perms)[2:]:>03}, "
        f"but expected {oct(expected_perms)[2:]:>03}."
    )