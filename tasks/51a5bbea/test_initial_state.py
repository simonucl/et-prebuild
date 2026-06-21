# test_initial_state.py
#
# This test-suite validates the *pre-exercise* state of the operating system.
# It checks that the expected backup directory and the three placeholder SQL
# dump files are present.  Nothing about the *output* path
# (/home/user/backup_verification/…) is asserted here, because those items are
# supposed to be created by the student’s solution.

import os
from pathlib import Path

BACKUP_DIR = Path("/home/user/data/backups")
EXPECTED_FILES = {
    BACKUP_DIR / "backup-20240115T231500Z.sql",
    BACKUP_DIR / "backup-20240116T231500Z.sql",
    BACKUP_DIR / "backup-20240117T231500Z.sql",
}


def test_backup_directory_exists():
    """
    The backups directory must already exist and be a directory.
    """
    assert BACKUP_DIR.exists(), (
        f"Required directory '{BACKUP_DIR}' is missing. "
        "Create it before running the exercise."
    )
    assert BACKUP_DIR.is_dir(), (
        f"'{BACKUP_DIR}' exists but is not a directory; "
        "fix the filesystem layout."
    )


def test_expected_backup_files_present_and_no_extras():
    """
    Exactly the three pre-seeded zero-byte SQL files must be present.
    """
    existing_files = {p for p in BACKUP_DIR.glob("backup-*.sql") if p.is_file()}

    # Check for missing files
    missing = EXPECTED_FILES - existing_files
    assert not missing, (
        "The following required backup file(s) are missing:\n  - "
        + "\n  - ".join(str(p) for p in sorted(missing))
    )

    # Check for unexpected extras
    extras = existing_files - EXPECTED_FILES
    assert not extras, (
        "Unexpected backup file(s) found in the directory (should not be present yet):\n  - "
        + "\n  - ".join(str(p) for p in sorted(extras))
    )

    # Optionally verify they are zero-byte placeholders
    non_zero = [p for p in EXPECTED_FILES if p.stat().st_size != 0]
    assert not non_zero, (
        "The following pre-seeded backup file(s) are expected to be empty "
        "but are not:\n  - " + "\n  - ".join(str(p) for p in sorted(non_zero))
    )