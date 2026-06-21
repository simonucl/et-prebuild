# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state *before* the student
starts solving the exercise.

It checks that:
1. /home/user/backup exists and is a directory.
2. /home/user/backup/full_backup.log exists, is a regular file and its
   byte-exact content matches the specification (three lines, each ending with LF).
3. The file permissions of full_backup.log are 0o644.

NOTE:  We deliberately do NOT test for the presence or absence of any output
files such as /home/user/backup/reordered_backup.log or
/home/user/backup/reorder_status.txt, in accordance with the rules.
"""

import os
import stat
import pytest

BACKUP_DIR = "/home/user/backup"
FULL_BACKUP_FILE = os.path.join(BACKUP_DIR, "full_backup.log")

EXPECTED_FULL_BACKUP_CONTENT = (
    b"2024-06-01|00:15|37GB|OK\n"
    b"2024-06-02|00:17|40GB|OK\n"
    b"2024-06-03|00:20|38GB|FAIL\n"
)


def test_backup_directory_exists_and_is_dir():
    """Ensure the /home/user/backup directory exists."""
    assert os.path.exists(
        BACKUP_DIR
    ), f"Required directory missing: {BACKUP_DIR}"
    assert os.path.isdir(
        BACKUP_DIR
    ), f"Expected {BACKUP_DIR} to be a directory."


def test_full_backup_log_exists_and_is_file():
    """Ensure /home/user/backup/full_backup.log exists and is a regular file."""
    assert os.path.exists(
        FULL_BACKUP_FILE
    ), f"Required file missing: {FULL_BACKUP_FILE}"
    assert os.path.isfile(
        FULL_BACKUP_FILE
    ), f"{FULL_BACKUP_FILE} exists but is not a regular file."


def test_full_backup_log_content_matches_spec():
    """
    Verify the content of /home/user/backup/full_backup.log is *exactly*
    the three specified lines terminated by LF and nothing else.
    """
    with open(FULL_BACKUP_FILE, "rb") as fp:
        data = fp.read()

    assert (
        data == EXPECTED_FULL_BACKUP_CONTENT
    ), (
        f"Content of {FULL_BACKUP_FILE} does not match the specification.\n"
        f"Expected bytes:\n{EXPECTED_FULL_BACKUP_CONTENT!r}\n"
        f"Actual bytes:\n{data!r}"
    )


def test_full_backup_log_permissions():
    """Check that full_backup.log has mode 0644."""
    st_mode = os.stat(FULL_BACKUP_FILE).st_mode
    perms = stat.S_IMODE(st_mode)
    expected_perms = 0o644
    assert (
        perms == expected_perms
    ), f"{FULL_BACKUP_FILE} permissions are {oct(perms)}, expected {oct(expected_perms)}."