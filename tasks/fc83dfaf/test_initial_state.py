# test_initial_state.py
#
# This pytest suite verifies that the machine starts in the **clean**
# state expected *before* the student carries out the task described in
# the exercise.  If any of these assertions fail, the exercise runner
# is already “contaminated” with files or directories that the student
# is supposed to create, and the environment must be reset.
#
# Only the Python stdlib and pytest are used.

import os
from pathlib import Path


HOME = Path("/home/user")
BACKUP_DIR = HOME / "backup_checks"
PING_LOG = BACKUP_DIR / "loopback_ping.log"


def test_home_directory_exists_and_is_directory():
    """Sanity-check: /home/user must exist and be a directory."""
    assert HOME.exists(), "Expected home directory /home/user to exist."
    assert HOME.is_dir(), "/home/user exists but is not a directory."


def test_backup_checks_directory_absent():
    """
    The backup_checks directory must NOT exist yet.

    The student’s first step in the assignment is to create this
    directory.  If it is already present, the environment is in an
    unexpected state.
    """
    assert not BACKUP_DIR.exists(), (
        "Directory /home/user/backup_checks already exists. "
        "The exercise expects the student to create it."
    )


def test_loopback_ping_log_absent():
    """
    The loopback_ping.log file must NOT exist yet.

    The student is responsible for generating this file with the
    correct ping output and summary line.  Its pre-existence would give
    the student an unearned pass.
    """
    assert not PING_LOG.exists(), (
        "File /home/user/backup_checks/loopback_ping.log already exists. "
        "The exercise expects the student to create it."
    )