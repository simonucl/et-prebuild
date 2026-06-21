# test_initial_state.py
"""
Pytest suite that validates the container’s initial filesystem state
*before* the student types the required one-liner.

NOTE:  If any test in this suite fails, the container is not in the expected
       “clean slate” that the task description promises.

Only the Python standard library and pytest are used.
"""

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
BASE_DIR = HOME / "mobile-pipelines"
SCRIPTS_DIR = BASE_DIR / "scripts"
LOGS_DIR = BASE_DIR / "logs"
LOG_FILE = LOGS_DIR / "perm_fix.log"

SCRIPT_FILES = {
    SCRIPTS_DIR / "deploy_android.sh",
    SCRIPTS_DIR / "build_ios.sh",
    SCRIPTS_DIR / "cleanup.sh",
}
NON_SCRIPT_FILES = {
    SCRIPTS_DIR / "readme.md",
}


def _assert_is_file(path: Path):
    assert path.exists(), f"Expected file or directory at {path} but it is missing."
    assert path.is_file(), f"Expected {path} to be a regular file."


def _assert_mode(path: Path, expected: int):
    actual = stat.S_IMODE(path.stat().st_mode)
    assert (
        actual == expected
    ), f"Expected permissions {oct(expected)} for {path}, found {oct(actual)}."


# --------------------------------------------------------------------------- #
#  Directory structure                                                        #
# --------------------------------------------------------------------------- #
def test_required_directories_exist():
    for directory in (BASE_DIR, SCRIPTS_DIR, LOGS_DIR):
        assert directory.exists(), f"Missing directory {directory}"
        assert directory.is_dir(), f"{directory} exists but is not a directory"


# --------------------------------------------------------------------------- #
#  Presence of expected files                                                 #
# --------------------------------------------------------------------------- #
def test_expected_files_exist():
    for file_path in SCRIPT_FILES | NON_SCRIPT_FILES | {LOG_FILE}:
        _assert_is_file(file_path)


# --------------------------------------------------------------------------- #
#  File permissions prior to student action                                   #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("script_path", sorted(SCRIPT_FILES))
def test_script_files_are_not_executable(script_path: Path):
    """
    All *.sh scripts start as 0644 (rw-r--r--) — definitely NOT executable.
    """
    _assert_is_file(script_path)
    mode = stat.S_IMODE(script_path.stat().st_mode)

    # Validate exact mode: rw-r--r--
    _assert_mode(script_path, 0o644)

    # Extra safety: ensure *no* execute bits are set
    assert (
        mode & stat.S_IXUSR == 0
    ), f"{script_path} unexpectedly has the owner-executable bit set."
    assert (
        mode & stat.S_IXGRP == 0
    ), f"{script_path} unexpectedly has the group-executable bit set."
    assert (
        mode & stat.S_IXOTH == 0
    ), f"{script_path} unexpectedly has the other-executable bit set."


@pytest.mark.parametrize("other_path", sorted(NON_SCRIPT_FILES))
def test_non_script_files_permissions(other_path: Path):
    """
    Non-script text files (e.g., readme.md) remain 0644 and should not become executable.
    """
    _assert_is_file(other_path)
    _assert_mode(other_path, 0o644)


def test_log_file_starts_empty_and_is_correctly_permissioned():
    """
    The audit log exists, is empty, and owned/writable by the current user.
    """
    _assert_is_file(LOG_FILE)
    _assert_mode(LOG_FILE, 0o644)

    size = LOG_FILE.stat().st_size
    assert size == 0, (
        f"{LOG_FILE} is expected to be empty before the student runs "
        f"their command, but its size is {size} bytes."
    )