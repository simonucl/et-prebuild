# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state **before**
# the learner runs any synchronisation command.  These tests guarantee that
# the starting conditions match the specification so that subsequent
# grading of the learner’s work is meaningful.
#
# Requirements verified
# ---------------------
# 1. /home/user/datasets/original/ exists and contains *exactly* the five
#    files listed in the task description, with the required directory
#    hierarchy.
# 2. /home/user/datasets/backup/ exists and is completely empty.
# 3. /home/user/datasets/sync_report.log does NOT yet exist.
#
# Only the Python stdlib and pytest are used.

import os
from pathlib import Path

import pytest

# Absolute base paths used throughout the tests
DATASETS_DIR = Path("/home/user/datasets")
ORIGINAL_DIR = DATASETS_DIR / "original"
BACKUP_DIR = DATASETS_DIR / "backup"
SYNC_LOG = DATASETS_DIR / "sync_report.log"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def list_all_files(base_dir: Path) -> set[str]:
    """
    Recursively walk ``base_dir`` and return a set of POSIX-style paths
    relative to ``base_dir`` for every *file* found.  Directories are not
    returned.
    """
    files: set[str] = set()
    for root, _dirs, filenames in os.walk(base_dir):
        root_path = Path(root)
        for fname in filenames:
            full_path = root_path / fname
            rel_path = full_path.relative_to(base_dir).as_posix()
            files.add(rel_path)
    return files


# ---------------------------------------------------------------------------
# Tests for the initial state
# ---------------------------------------------------------------------------


def test_original_directory_structure_and_files_exist():
    """
    The source directory must exist and contain exactly the five expected
    files (no more, no less) with the correct hierarchy.
    """
    assert ORIGINAL_DIR.is_dir(), (
        f"Required directory '{ORIGINAL_DIR}' is missing.  "
        "The initial dataset directory must be present."
    )

    expected_relative_files = {
        "experiment1.csv",
        "experiment2.csv",
        "readme.md",
        "images/plot_A.png",
        "images/plot_B.png",
    }

    found_files = list_all_files(ORIGINAL_DIR)

    # Check for missing files
    missing = expected_relative_files - found_files
    assert not missing, (
        "The following expected file(s) are missing from the initial "
        f"dataset: {sorted(missing)}"
    )

    # Check for unexpected / extra files
    extra = found_files - expected_relative_files
    assert not extra, (
        "Unexpected file(s) were found in the initial dataset directory: "
        f"{sorted(extra)}"
    )


def test_backup_directory_exists_and_is_empty():
    """
    The target backup directory must already exist but be *empty* before
    the learner starts their work.
    """
    assert BACKUP_DIR.is_dir(), (
        f"Required directory '{BACKUP_DIR}' is missing.  "
        "It must exist and be empty before synchronisation."
    )

    # Any item (file or dir) inside BACKUP_DIR constitutes a failure.
    contents = list(BACKUP_DIR.iterdir())
    assert not contents, (
        f"Backup directory '{BACKUP_DIR}' is expected to be empty, "
        f"but contains: {[p.name for p in contents]}"
    )


def test_sync_log_does_not_exist_yet():
    """
    The synchronisation report must *not* exist at the start.
    """
    assert not SYNC_LOG.exists(), (
        f"Log file '{SYNC_LOG}' should not exist before the synchronisation "
        "command is executed."
    )