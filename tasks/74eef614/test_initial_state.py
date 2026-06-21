# test_initial_state.py
#
# This test-suite verifies that the machine starts from the **expected,
# pristine state** before the student’s backup routine is run.
#
# 1. The legacy data found in /home/user/important_data/ must already exist
#    exactly as described (four files, exact sizes, correct directory layout).
# 2. No deliverables must exist yet in /home/user/backups/.
#
# If any of these assertions fail, the operating-system image given to the
# student is wrong and the exercise can’t be completed reliably.

import os
from pathlib import Path

import pytest

IMPORTANT_DIR = Path("/home/user/important_data")
BACKUP_DIR = Path("/home/user/backups")

# Expected files (key = relative path inside important_data, value = size in bytes)
FILES_INFO = {
    "README.md": 104,
    "reports/quarter1.txt": 43,
    "reports/quarter2.txt": 43,
    "scripts/cleanup.sh": 52,
}

# Deliverable paths that must **not** exist before the student starts
DELIVERABLES = [
    BACKUP_DIR / "ImportantData_20240401.tar.gz",
    BACKUP_DIR / "ImportantData_20240401.manifest",
    BACKUP_DIR / "backup_success.log",
]


def test_important_data_directory_exists():
    """/home/user/important_data must exist and be a directory."""
    assert IMPORTANT_DIR.exists(), f"Expected directory {IMPORTANT_DIR} is missing."
    assert IMPORTANT_DIR.is_dir(), f"{IMPORTANT_DIR} exists but is not a directory."


def test_expected_files_present_with_correct_sizes():
    """
    The legacy application must ship with exactly four data files
    (and nothing else) in the expected subtree, each with the precise size.
    """
    # 1. Verify that *only* the expected files exist
    discovered = [
        str(Path(root).joinpath(name).relative_to(IMPORTANT_DIR))
        for root, _, files in os.walk(IMPORTANT_DIR)
        for name in files
    ]
    expected = sorted(FILES_INFO.keys())
    assert sorted(discovered) == expected, (
        "The file set in /home/user/important_data differs from the specification.\n"
        f"Expected: {expected}\nFound:    {sorted(discovered)}"
    )

    # 2. Verify sizes of each expected file
    for rel_path, expected_size in FILES_INFO.items():
        abs_path = IMPORTANT_DIR / rel_path
        assert abs_path.exists(), f"Required file {abs_path} is missing."
        size = abs_path.stat().st_size
        assert size == expected_size, (
            f"File {abs_path} has size {size} bytes but should be {expected_size} bytes."
        )


def test_no_backup_artifacts_exist_yet():
    """
    The student hasn't run their backup routine yet, so the backup directory
    (and especially the three deliverables) must not be present.
    """
    # /home/user/backups/ may or may not exist; if it does, it must not yet
    # contain any of the deliverables the grading logic will later look for.
    for path in DELIVERABLES:
        assert not path.exists(), (
            f"Deliverable {path} already exists before the task has begun; "
            "the initial state must not contain any backup artifacts."
        )