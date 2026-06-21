# test_initial_state.py
#
# Pytest suite that validates the **initial** on-disk state *before* the
# student script runs.  It checks directories, files, sizes and manifest
# correctness so that any mutation performed by the student can be
# attributed solely to their code and not to a bad starting snapshot.
#
# NOTE:  Do **not** edit this file when solving the main exercise.

import os
import pytest

HOME = "/home/user"
BACKUPS_DIR = os.path.join(HOME, "backups")
DAILY_DIR = os.path.join(BACKUPS_DIR, "daily")
QUARANTINE_DIR = os.path.join(BACKUPS_DIR, "quarantine")
VALIDATION_DIR = os.path.join(HOME, "backup_validation")
MANIFEST_PATH = os.path.join(BACKUPS_DIR, "manifest.size")

# Ground-truth expectations for the initial snapshot
EXPECTED_MANIFEST_LINES = [
    "56 users.bak",
    "59 inventory.bak",
    "80 orders.bak",
]

EXPECTED_SIZES = {
    "users.bak": 56,
    "inventory.bak": 59,
    "orders.bak": 85,     # real size on disk (intentionally differs from manifest)
}

@pytest.mark.order(1)
def test_required_directories_exist():
    assert os.path.isdir(BACKUPS_DIR), f"Missing directory: {BACKUPS_DIR}"
    assert os.path.isdir(DAILY_DIR), f"Missing directory: {DAILY_DIR}"

@pytest.mark.order(2)
def test_quarantine_not_present_yet():
    assert not os.path.exists(QUARANTINE_DIR), (
        f"Quarantine directory {QUARANTINE_DIR} should NOT exist before the task starts."
    )

@pytest.mark.order(3)
def test_validation_dir_not_present_yet():
    assert not os.path.exists(VALIDATION_DIR), (
        f"Validation directory {VALIDATION_DIR} should NOT exist before the task starts."
    )

@pytest.mark.order(4)
def test_manifest_file_exists_and_contents_are_correct():
    assert os.path.isfile(MANIFEST_PATH), f"Missing manifest file: {MANIFEST_PATH}"

    with open(MANIFEST_PATH, "rt", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    # Exact line-by-line equality
    assert lines == EXPECTED_MANIFEST_LINES, (
        f"Manifest contents mismatch.\nExpected lines:\n{EXPECTED_MANIFEST_LINES}\n"
        f"Actual lines:\n{lines}"
    )

@pytest.mark.order(5)
@pytest.mark.parametrize("filename, real_size", EXPECTED_SIZES.items())
def test_backup_file_present_with_expected_real_size(filename, real_size):
    path = os.path.join(DAILY_DIR, filename)
    assert os.path.isfile(path), f"Missing backup file: {path}"

    actual_size = os.path.getsize(path)
    assert actual_size == real_size, (
        f"Size mismatch for {path}. Expected {real_size} bytes on disk, found {actual_size}."
    )