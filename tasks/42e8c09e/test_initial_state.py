# test_initial_state.py
#
# This pytest suite validates that the sandbox is in its **initial**,
# pre-exercise state.  It must pass *before* the student starts working.
#
# What we assert:
#   1. The source directory /home/user/data_to_backup exists with the correct
#      structure *and exact byte contents*.
#   2. No backup-related artefacts (archive, log, .bak folder, etc.) exist yet.
#
# NOTE: Do **not** modify this file.  The grader relies on these checks.

import os
import glob
import pytest

HOME = "/home/user"
SRC_DIR = os.path.join(HOME, "data_to_backup")
BACKUPS_DIR = os.path.join(HOME, "backups")
ARCHIVE = os.path.join(BACKUPS_DIR, "full_backup.tar.gz")
LOG_FILE = os.path.join(HOME, "backup_restore.log")

# --------------------------------------------------------------------------- #
# Helpers & expected data                                                     #
# --------------------------------------------------------------------------- #

REPORT1_CONTENT = (
    b"Quarterly revenue report Q1 2024\n"
    b"Total: 1,234,567 USD\n"
)

REPORT2_CONTENT = (
    b"Quarterly revenue report Q2 2024\n"
    b"Total: 1,345,678 USD\n"
)

CONFIG_CONTENT = (
    b"[settings]\n"
    b"mode=production\n"
    b"version=2.3.4\n"
)

EXPECTED_RELATIVE_PATHS = {
    "report1.txt",
    "report2.txt",
    os.path.join("subdir", "config.cfg"),
}


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_source_directory_exists():
    assert os.path.isdir(SRC_DIR), (
        f"Required directory {SRC_DIR!r} is missing."
    )


def test_source_directory_structure():
    """
    Ensure that only the expected three files exist and they are where they
    should be.
    """
    found_paths = set()

    for root, dirs, files in os.walk(SRC_DIR):
        for name in files:
            abs_path = os.path.join(root, name)
            rel_path = os.path.relpath(abs_path, SRC_DIR)
            found_paths.add(rel_path)

    missing = EXPECTED_RELATIVE_PATHS - found_paths
    extra   = found_paths - EXPECTED_RELATIVE_PATHS

    assert not missing, (
        f"Missing expected file(s) in {SRC_DIR!r}: {sorted(missing)}"
    )
    assert not extra, (
        f"Unexpected extra file(s) present in {SRC_DIR!r}: {sorted(extra)}"
    )


@pytest.mark.parametrize("rel_path, expected_content", [
    ("report1.txt", REPORT1_CONTENT),
    ("report2.txt", REPORT2_CONTENT),
    (os.path.join("subdir", "config.cfg"), CONFIG_CONTENT),
])
def test_source_file_contents(rel_path, expected_content):
    abs_path = os.path.join(SRC_DIR, rel_path)
    assert os.path.isfile(abs_path), (
        f"Expected file {abs_path!r} is missing."
    )
    with open(abs_path, "rb") as fh:
        actual = fh.read()
    assert actual == expected_content, (
        f"Content mismatch in {abs_path!r}.\n"
        f"Expected bytes:\n{expected_content!r}\n"
        f"Actual bytes:\n{actual!r}"
    )


def test_no_backup_directory_yet():
    assert not os.path.exists(BACKUPS_DIR), (
        f"Backup directory {BACKUPS_DIR!r} should NOT exist yet."
    )


def test_no_archive_yet():
    assert not os.path.exists(ARCHIVE), (
        f"Backup archive {ARCHIVE!r} should NOT exist yet."
    )


def test_no_bak_directories_yet():
    bak_glob = os.path.join(HOME, "data_to_backup.bak_*")
    bak_dirs = glob.glob(bak_glob)
    assert not bak_dirs, (
        "No disaster-simulation directory should exist yet, but found: "
        f"{bak_dirs}"
    )


def test_no_log_file_yet():
    assert not os.path.exists(LOG_FILE), (
        f"Log file {LOG_FILE!r} should NOT exist yet."
    )