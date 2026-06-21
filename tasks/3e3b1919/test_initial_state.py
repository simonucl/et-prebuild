# test_initial_state.py
#
# This pytest file verifies that the operating-system / filesystem state
# is exactly as expected *before* the student performs any actions for the
# “rsync + verification-log” exercise.
#
# What we assert about the initial state
# --------------------------------------
# 1. Source directory /home/user/datasets/raw/ exists and contains *only*
#    the two CSV files customers.csv (45 bytes) and sales.csv (70 bytes).
# 2. The destination directory /home/user/remote_server/datasets_backup/
#    exists and is completely empty.
# 3. The verification log /home/user/sync.log must not exist yet.
#
# If any assertion fails, the corresponding error message should make it
# clear to the learner what is missing or incorrect.

import os
from pathlib import Path

SOURCE_DIR = Path("/home/user/datasets/raw")
TARGET_DIR = Path("/home/user/remote_server/datasets_backup")
SYNC_LOG   = Path("/home/user/sync.log")

EXPECTED_FILES = {
    "customers.csv": 45,
    "sales.csv": 70,
}


def test_source_directory_exists():
    assert SOURCE_DIR.is_dir(), (
        f"Source directory {SOURCE_DIR} is missing. "
        "It must exist and contain the raw CSV files."
    )


def test_source_contains_exact_two_files_with_correct_sizes():
    # Gather only regular files (skip sub-dirs, sockets, etc.)
    actual_files = {p.name: p for p in SOURCE_DIR.iterdir() if p.is_file()}

    missing = [name for name in EXPECTED_FILES if name not in actual_files]
    extra   = [name for name in actual_files if name not in EXPECTED_FILES]

    assert not missing, (
        f"The source directory is missing expected file(s): {', '.join(missing)}"
    )
    assert not extra, (
        f"The source directory contains unexpected extra file(s): {', '.join(extra)}"
    )

    for name, expected_size in EXPECTED_FILES.items():
        size = actual_files[name].stat().st_size
        assert size == expected_size, (
            f"{name} should be {expected_size} bytes but is {size} bytes"
        )


def test_target_directory_exists_and_is_empty():
    assert TARGET_DIR.is_dir(), (
        f"Target directory {TARGET_DIR} does not exist. "
        "It must be present (empty) before synchronisation."
    )

    # Any files inside TARGET_DIR at this point are a failure.
    contents = list(TARGET_DIR.iterdir())
    assert not contents, (
        f"Target directory {TARGET_DIR} is expected to be empty but contains: "
        f"{', '.join(p.name for p in contents)}"
    )


def test_sync_log_does_not_exist_yet():
    assert not SYNC_LOG.exists(), (
        f"{SYNC_LOG} already exists but should be created only *after* "
        "the synchronisation step."
    )