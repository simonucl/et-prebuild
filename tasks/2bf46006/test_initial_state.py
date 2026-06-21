# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before**
# the student performs any action.  It intentionally checks only the
# things that must already be present (or absent) according to the
# assignment description.

import os
import stat
import pytest


RELEASES_PATH = "/home/user/releases"
CURRENT_SYMLINK = "/home/user/release/current"

EXPECTED_RELEASE_DIRS = [
    "/home/user/releases/2024-01-26",
    "/home/user/releases/2024-01-20",
]

RELEASE_DIR = "/home/user/release"


@pytest.mark.parametrize("path", EXPECTED_RELEASE_DIRS)
def test_expected_release_directories_exist_and_are_empty(path):
    """
    Each required release directory must already exist, be a directory, and be
    empty.  If any of these conditions is false, the initial filesystem state
    is incorrect.
    """
    assert os.path.exists(path), f"Required directory {path!r} is missing."
    stat_info = os.lstat(path)
    assert stat.S_ISDIR(stat_info.st_mode), (
        f"Path {path!r} exists but is not a directory."
    )

    # Directory should be empty (no files, symlinks, or subdirectories).
    contents = os.listdir(path)
    assert (
        len(contents) == 0
    ), f"Directory {path!r} is expected to be empty but contains: {contents!r}"


def test_release_parent_directory_exists_and_is_empty():
    """
    /home/user/release/ must exist, be a directory, and be empty before the
    student creates the 'current' symlink.
    """
    assert os.path.exists(RELEASE_DIR), (
        f"Directory {RELEASE_DIR!r} is missing."
    )
    stat_info = os.lstat(RELEASE_DIR)
    assert stat.S_ISDIR(stat_info.st_mode), (
        f"Path {RELEASE_DIR!r} exists but is not a directory."
    )

    contents = os.listdir(RELEASE_DIR)
    assert (
        len(contents) == 0
    ), (
        f"Directory {RELEASE_DIR!r} should be empty before the task begins. "
        f"Found: {contents!r}"
    )


def test_current_symlink_does_not_exist_yet():
    """
    The symbolic link /home/user/release/current must NOT exist before the
    student runs their command.  If it already exists, the environment is
    in the wrong state.
    """
    assert not os.path.lexists(
        CURRENT_SYMLINK
    ), (
        f"Symlink {CURRENT_SYMLINK!r} should not exist before the student "
        "creates it."
    )