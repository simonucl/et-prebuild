# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state **before** the student performs any action for the “restore-through-
# symlink” exercise.
#
# The tests deliberately fail with clear, actionable messages if the setup
# is not exactly as described in the task.

import os
import stat
from pathlib import Path

HOME = Path("/home/user")
BACKUP_DIR = HOME / "backup" / "2023-10-10"
BACKUP_FILE = BACKUP_DIR / "settings.ini"

RESTORE_DIR = HOME / "restore"
RESTORE_LINK = RESTORE_DIR / "settings.ini"
RESTORE_LOG = RESTORE_DIR / "restore_link_test.log"

EXPECTED_BACKUP_CONTENT = "[General]\nversion=1\n"
EXPECTED_BACKUP_DIR_MODE = 0o755
EXPECTED_BACKUP_FILE_MODE = 0o644


def test_backup_directory_exists_with_correct_permissions():
    assert BACKUP_DIR.exists(), (
        f"Required directory {BACKUP_DIR} is missing."
    )
    assert BACKUP_DIR.is_dir(), (
        f"{BACKUP_DIR} exists but is not a directory."
    )

    actual_mode = stat.S_IMODE(BACKUP_DIR.stat().st_mode)
    assert actual_mode == EXPECTED_BACKUP_DIR_MODE, (
        f"{BACKUP_DIR} permissions are {oct(actual_mode)}, "
        f"expected {oct(EXPECTED_BACKUP_DIR_MODE)}."
    )


def test_backup_file_exists_with_correct_permissions_and_content():
    assert BACKUP_FILE.exists(), (
        f"Required file {BACKUP_FILE} is missing."
    )
    assert BACKUP_FILE.is_file(), (
        f"{BACKUP_FILE} exists but is not a regular file."
    )

    actual_mode = stat.S_IMODE(BACKUP_FILE.stat().st_mode)
    assert actual_mode == EXPECTED_BACKUP_FILE_MODE, (
        f"{BACKUP_FILE} permissions are {oct(actual_mode)}, "
        f"expected {oct(EXPECTED_BACKUP_FILE_MODE)}."
    )

    content = BACKUP_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_BACKUP_CONTENT, (
        f"{BACKUP_FILE} content mismatch.\n"
        f"Expected exactly:\n{EXPECTED_BACKUP_CONTENT!r}\n"
        f"Found:\n{content!r}"
    )


def test_restore_directory_and_artifacts_do_not_exist_yet():
    assert not RESTORE_DIR.exists(), (
        f"Directory {RESTORE_DIR} should NOT exist before the task starts."
    )
    # If the directory does not exist, neither the symlink nor the log file
    # can exist.  Still, provide explicit checks for clarity.
    assert not RESTORE_LINK.exists(), (
        f"Symlink {RESTORE_LINK} should NOT exist before the task starts."
    )
    assert not RESTORE_LOG.exists(), (
        f"Log file {RESTORE_LOG} should NOT exist before the task starts."
    )