# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be in
# place before the student performs any actions for the “backup-integrity
# spot-check” exercise.
#
# The tests purposefully avoid touching/inspecting any **output** artefacts
# (e.g. the size-verification log or its containing directory) in accordance
# with the grading-suite rules.
#
# Assertions performed:
#   • /home/user/backups/daily/ exists and is a directory.
#   • Exactly three files are present inside that directory.
#   • Each required file exists, is a regular file and has the exact
#     byte-size specified in the truth data.

import os
import stat
import pytest

BACKUP_DIR = "/home/user/backups/daily"

# Mapping of expected filename → exact byte size
EXPECTED_BACKUP_FILES = {
    "config_backup.conf": 17,
    "db_dump.sql": 27,
    "site_files.tar.gz": 18,
}


def _full_path(filename: str) -> str:
    """Helper to build the absolute path for a file in BACKUP_DIR."""
    return os.path.join(BACKUP_DIR, filename)


def test_backup_directory_exists_and_is_dir():
    assert os.path.exists(
        BACKUP_DIR
    ), f"Required directory {BACKUP_DIR!r} is missing."
    assert os.path.isdir(
        BACKUP_DIR
    ), f"{BACKUP_DIR!r} exists but is not a directory."


def test_backup_directory_contains_only_expected_files():
    # Collect the set of *regular* files in the directory
    present_files = {
        name
        for name in os.listdir(BACKUP_DIR)
        if stat.S_ISREG(os.stat(_full_path(name)).st_mode)
    }

    expected_files = set(EXPECTED_BACKUP_FILES)
    # Missing files
    missing = expected_files - present_files
    # Unexpected extra files
    extra = present_files - expected_files

    assert not missing, (
        "The following required backup file(s) are missing from "
        f"{BACKUP_DIR!r}: {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"Unexpected file(s) found in {BACKUP_DIR!r}: "
        f"{', '.join(sorted(extra))}. "
        "Only the three specified backup files should be present."
    )


@pytest.mark.parametrize("filename, expected_size", EXPECTED_BACKUP_FILES.items())
def test_each_backup_file_has_expected_size(filename, expected_size):
    path = _full_path(filename)
    assert os.path.exists(path), f"Required file {path!r} does not exist."
    assert os.path.isfile(path), f"{path!r} exists but is not a regular file."

    actual_size = os.path.getsize(path)
    assert (
        actual_size == expected_size
    ), f"{filename!r} has size {actual_size} bytes; expected {expected_size} bytes."