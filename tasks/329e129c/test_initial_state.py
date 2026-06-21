# test_initial_state.py
"""
Pytest suite that validates the *initial* on-disk state **before** the student
runs any commands for the “delete *.tmp build artefacts” task.

The checks intentionally cover only the pre-task state; they do **not** look for
any files or directories that will be created by the user solution.
"""

import os
from pathlib import Path

ROOT_DIR = Path("/home/user/ci_cd")
BUILD_DIR = ROOT_DIR / "build-artifacts"
CACHE_DIR = BUILD_DIR / "cache"

# Absolute paths of the files that must exist prior to the task
EXPECTED_TMP_FILES = {
    str(BUILD_DIR / "temp1.tmp"),
    str(BUILD_DIR / "temp2.tmp"),
    str(CACHE_DIR / "build123.tmp"),
    str(CACHE_DIR / "old.build.tmp"),
}

# Non-tmp artefact that must stay untouched throughout the task
IMPORTANT_BIN = BUILD_DIR / "important.bin"


def test_required_directories_exist_and_are_dirs():
    for directory in (ROOT_DIR, BUILD_DIR, CACHE_DIR):
        assert directory.exists(), f"Required directory {directory} is missing."
        assert directory.is_dir(), f"{directory} exists but is not a directory."


def test_required_tmp_files_exist_and_are_files():
    for filepath in EXPECTED_TMP_FILES:
        path = Path(filepath)
        assert path.exists(), f"Required file {filepath} is missing."
        assert path.is_file(), f"{filepath} exists but is not a regular file."


def test_no_extra_tmp_files_present():
    """Ensure there are *exactly* the expected *.tmp files before deletion."""
    discovered_tmp_files = {
        str(p) for p in BUILD_DIR.rglob("*.tmp") if p.is_file()
    }
    assert (
        discovered_tmp_files == EXPECTED_TMP_FILES
    ), (
        "The set of .tmp files present does not match the expected initial state.\n"
        f"Expected: {sorted(EXPECTED_TMP_FILES)}\n"
        f"Found:    {sorted(discovered_tmp_files)}"
    )


def test_important_bin_exists_and_is_file():
    assert IMPORTANT_BIN.exists(), f"Critical artefact {IMPORTANT_BIN} is missing."
    assert IMPORTANT_BIN.is_file(), f"{IMPORTANT_BIN} exists but is not a file."


def test_cleanup_directory_does_not_exist_yet():
    cleanup_dir = Path("/home/user/cleanup")
    assert not cleanup_dir.exists(), (
        f"{cleanup_dir} should not exist before the task begins."
    )