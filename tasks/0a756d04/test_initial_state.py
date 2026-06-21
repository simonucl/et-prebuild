# test_initial_state.py
#
# This pytest suite validates the initial state of the operating system
# and filesystem *before* the student attempts the task described in the
# prompt.  It checks only the pre-existing inputs and environment and
# deliberately avoids touching any files that the student is expected to
# create or modify later on.

import os
import stat
import pytest

BACKUP_DIR = "/home/user/backup"
SRC_FILE   = os.path.join(BACKUP_DIR, "files_to_backup.txt")

# The exact, byte-for-byte content we expect to find in files_to_backup.txt.
EXPECTED_SRC_CONTENT = (
    "/etc/hosts\n"
    "/home/user/data/report1.csv\n"
    "/etc/hosts\n"
    "/var/log/syslog\n"
    "/home/user/data/report2.csv\n"
    "/var/log/syslog\n"
)

def test_backup_directory_exists_and_is_writable():
    """
    /home/user/backup must exist, be a directory, and be writable by the
    current (unprivileged) user.  The directory's exact mode does not matter
    as long as the user has write permission.
    """
    assert os.path.isdir(BACKUP_DIR), (
        f"Required directory {BACKUP_DIR!r} is missing or not a directory."
    )

    # os.access is the most portable way to check *effective* permissions.
    assert os.access(BACKUP_DIR, os.W_OK), (
        f"Directory {BACKUP_DIR!r} exists but is not writable by the current user."
    )

def test_source_file_exists_with_correct_content():
    """
    The initial input file files_to_backup.txt must exist and contain the
    unsorted list with duplicates exactly as specified in the task description,
    including the single trailing newline and no extra blank lines.
    """
    assert os.path.isfile(SRC_FILE), (
        f"Required file {SRC_FILE!r} is missing."
    )

    with open(SRC_FILE, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    # Byte-for-byte comparison ensures no stray whitespace, missing newlines, etc.
    assert actual_content == EXPECTED_SRC_CONTENT, (
        f"{SRC_FILE!r} content does not match the expected initial state.\n"
        "---- Expected ----\n"
        f"{EXPECTED_SRC_CONTENT!r}\n"
        "---- Actual ----\n"
        f"{actual_content!r}"
    )

@pytest.mark.parametrize("path", [
    # NOTE: Per the grading rules we *must not* test for any of the output files
    # (files_to_backup.sorted.txt or operation.log).  The list below is limited
    # strictly to required pre-existing inputs.
    SRC_FILE,
])
def test_no_symlink_or_weird_type(path):
    """
    Sanity-check that the source file is a regular file, not a symlink or
    special device.  This guards against unexpected filesystem tricks.
    """
    st_mode = os.lstat(path).st_mode
    assert stat.S_ISREG(st_mode), (
        f"{path!r} is expected to be a regular file but is not."
    )