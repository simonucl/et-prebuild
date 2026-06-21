# test_initial_state.py
#
# This pytest suite validates the initial state of the project *before*
# the student performs any action.  It checks that the expected
# /home/user/legacy-analytics directory and its tracker.py script
# both exist with the correct permissions and exact contents.
#
# DO NOT add tests for files that should be created later (e.g.,
# verification.log).  These tests must all pass **before** the student
# starts working.


import os
import stat
import pytest

# Constant paths used throughout the tests
PROJECT_DIR = "/home/user/legacy-analytics"
TRACKER_PATH = os.path.join(PROJECT_DIR, "tracker.py")

###############################################################################
# Helper utilities
###############################################################################


def mode_as_octal(path: str) -> int:
    """
    Return the permission bits of a file or directory as an octal integer
    (e.g., 0o755).
    """
    return stat.S_IMODE(os.lstat(path).st_mode)


###############################################################################
# Tests for directory existence and permissions
###############################################################################


def test_project_directory_exists_and_is_dir():
    assert os.path.exists(PROJECT_DIR), (
        f"Expected directory {PROJECT_DIR} to exist, but it does not."
    )

    assert os.path.isdir(PROJECT_DIR), (
        f"Expected {PROJECT_DIR} to be a directory, but it is not."
    )


def test_project_directory_permissions():
    expected_mode = 0o755
    current_mode = mode_as_octal(PROJECT_DIR)
    assert current_mode == expected_mode, (
        f"{PROJECT_DIR} permissions are {oct(current_mode)}, "
        f"but expected {oct(expected_mode)} (rwxr-xr-x)."
    )


###############################################################################
# Tests for tracker.py existence, permissions, and contents
###############################################################################


def test_tracker_script_exists_and_is_file():
    assert os.path.exists(TRACKER_PATH), (
        f"Expected file {TRACKER_PATH} to exist, but it does not."
    )

    assert os.path.isfile(TRACKER_PATH), (
        f"Expected {TRACKER_PATH} to be a regular file, but it is not."
    )


def test_tracker_script_permissions():
    expected_mode = 0o755
    current_mode = mode_as_octal(TRACKER_PATH)
    assert current_mode == expected_mode, (
        f"{TRACKER_PATH} permissions are {oct(current_mode)}, "
        f"but expected {oct(expected_mode)} (rwxr-xr-x)."
    )


def test_tracker_script_contents():
    expected_contents = (
        "#!/usr/bin/env python3\n"
        'print("legacy-analytics OK")\n'
    )

    with open(TRACKER_PATH, "r", encoding="utf-8") as fp:
        actual_contents = fp.read()

    assert actual_contents == expected_contents, (
        f"The contents of {TRACKER_PATH} do not match the expected value.\n"
        "Expected (repr):\n"
        f"{repr(expected_contents)}\n"
        "Got (repr):\n"
        f"{repr(actual_contents)}"
    )