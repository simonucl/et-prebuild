# test_initial_state.py
#
# Pytest suite to verify that the operating-system / filesystem
# is in the expected **initial** state *before* the student carries
# out the assignment.
#
# Expectations for the clean slate:
#   •  /home/user/projects/file_index.db   MUST NOT exist
#   •  /home/user/projects/file_index.log  MUST NOT exist
#   •  /home/user/projects/                may or may not exist, but
#        – if it does, it must be a directory and writable by the user
#        – if it does not, its parent (/home/user) must be writable
#
# These checks ensure the student starts from a known good state and
# that nothing from a previous run can interfere with evaluation.

import os
from pathlib import Path
import stat
import pytest

PROJECTS_DIR = Path("/home/user/projects")
DB_FILE       = PROJECTS_DIR / "file_index.db"
LOG_FILE      = PROJECTS_DIR / "file_index.log"


def _is_writable(path: Path) -> bool:
    """
    Return True if `path` is writable by the current real user.
    Uses os.access with the W_OK mode.
    """
    return os.access(str(path), os.W_OK)


def test_file_index_db_absent():
    """
    The SQLite database must NOT exist before the exercise begins.
    """
    assert not DB_FILE.exists(), (
        f"Precondition failed: unexpected file {DB_FILE} already exists. "
        "Remove it before performing the task."
    )


def test_file_index_log_absent():
    """
    The log file must NOT exist before the exercise begins.
    """
    assert not LOG_FILE.exists(), (
        f"Precondition failed: unexpected file {LOG_FILE} already exists. "
        "Remove it before performing the task."
    )


def test_projects_directory_writable_or_creatable():
    """
    If /home/user/projects already exists, it must be a writable directory.
    If it does not yet exist, its parent (/home/user) must be writable so
    that the student can create it.
    """
    if PROJECTS_DIR.exists():
        # Path exists; it must be a directory.
        assert PROJECTS_DIR.is_dir(), (
            f"{PROJECTS_DIR} exists but is not a directory. "
            "Please remove or rename it before starting the task."
        )

        # Directory must be writable by the current user.
        assert _is_writable(PROJECTS_DIR), (
            f"{PROJECTS_DIR} exists but is not writable by the current user. "
            "Adjust permissions (e.g., chmod 755) before continuing."
        )
    else:
        # Directory does not yet exist; parent (/home/user) must be writable.
        parent = PROJECTS_DIR.parent
        assert parent.exists(), (
            f"Parent directory {parent} does not exist. "
            "The exercise expects /home/user to be present."
        )
        assert _is_writable(parent), (
            f"Cannot create {PROJECTS_DIR}: parent directory {parent} is not writable "
            "by the current user. Adjust permissions before continuing."
        )