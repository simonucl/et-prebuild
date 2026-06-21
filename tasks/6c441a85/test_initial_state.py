# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student runs any commands for the “core-dump
# compression” exercise.
#
# What we expect at this point:
#   1. Directory /home/user/app_dumps exists.
#   2. Exactly the three *.core files listed below exist as regular files
#      and have the exact byte sizes specified in the task description.
#   3. No *.core.gz files are present yet.
#   4. /home/user/app_dumps/compression.log must *not* exist yet.
#
# Any deviation means the starting state is wrong and the subsequent
# exercise cannot be graded reliably.

import os
import re
from pathlib import Path
import pytest

APP_DUMPS_DIR = Path("/home/user/app_dumps")

# Expected core-dump files and their sizes in bytes
EXPECTED_CORES = {
    "crash1.core": 12,   # "CORE_DUMP_1\n"
    "crash2.core": 12,   # "CORE_DUMP_2\n"
    "crash3.core": 20,   # "CORRUPTED_CORE_DUMP\n"
}

LOG_FILE = APP_DUMPS_DIR / "compression.log"


def test_app_dumps_dir_exists_and_is_dir():
    assert APP_DUMPS_DIR.exists(), (
        f"Required directory {APP_DUMPS_DIR} does not exist. "
        "The exercise expects all core dumps to live inside this directory."
    )
    assert APP_DUMPS_DIR.is_dir(), (
        f"{APP_DUMPS_DIR} exists but is not a directory. "
        "It must be a directory holding the core-dump files."
    )


@pytest.mark.parametrize("filename,expected_size", EXPECTED_CORES.items())
def test_core_files_exist_with_correct_size(filename, expected_size):
    file_path = APP_DUMPS_DIR / filename
    assert file_path.exists(), (
        f"Expected core-dump file {file_path} is missing."
    )
    assert file_path.is_file(), (
        f"{file_path} exists but is not a regular file."
    )

    actual_size = file_path.stat().st_size
    assert actual_size == expected_size, (
        f"Size mismatch for {file_path}: expected {expected_size} bytes, "
        f"found {actual_size} bytes."
    )


def test_no_extra_core_files_present():
    """
    Ensure that no additional *.core files are present.  The initial state
    must contain exactly the three expected dumps—nothing more, nothing less.
    """
    core_files_on_disk = sorted(p.name for p in APP_DUMPS_DIR.glob("*.core"))
    expected_sorted = sorted(EXPECTED_CORES.keys())
    assert core_files_on_disk == expected_sorted, (
        "Unexpected set of *.core files detected.\n"
        f"Expected: {expected_sorted}\n"
        f"Found   : {core_files_on_disk}"
    )


def test_no_gz_files_present_initially():
    gz_files = list(APP_DUMPS_DIR.glob("*.core.gz"))
    assert not gz_files, (
        "There should be NO '*.core.gz' files before the student performs the "
        "compression step, but the following files were found:\n"
        + "\n".join(str(p) for p in gz_files)
    )


def test_log_file_does_not_exist_initially():
    assert not LOG_FILE.exists(), (
        f"The log file {LOG_FILE} already exists, but it must be created by "
        "the student's solution after compression."
    )