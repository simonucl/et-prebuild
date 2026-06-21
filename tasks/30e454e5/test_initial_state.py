# test_initial_state.py
#
# This pytest file verifies that the filesystem is in the correct
# *initial* state before the student performs any actions.
#
# According to the assignment, NOTHING should yet exist under
# /home/user/logs.  These tests therefore assert the absence of both
# the directory and the target log file.  If either one is already
# present, the environment is not clean and the tests will fail with
# clear, actionable messages.

import os
from pathlib import Path
import pytest

LOGS_DIR = Path("/home/user/logs")
LOG_FILE = LOGS_DIR / "test_timestamp.log"


def _human_mode(mode: int) -> str:
    """
    Return a human-readable string (e.g. '100644') for a file mode.
    """
    return oct(mode)


def _describe_existing_path(path: Path) -> str:
    """
    Return a rich description of an existing path for debugging.
    """
    if not path.exists():
        return "does not exist"
    info = path.stat()
    kind = "directory" if path.is_dir() else "file"
    return f"exists ({kind}, mode={_human_mode(info.st_mode)})"


def test_logs_directory_absent():
    """
    The /home/user/logs directory must NOT exist yet.
    """
    assert not LOGS_DIR.exists(), (
        "Pre-existing directory detected: "
        f"{LOGS_DIR} {_describe_existing_path(LOGS_DIR)}.\n"
        "The initial state must be clean so that the student can create "
        "this directory as part of the task."
    )


def test_log_file_absent():
    """
    The /home/user/logs/test_timestamp.log file must NOT exist yet.
    """
    # If the directory already exists, the previous test will have failed,
    # but we still guard against stray files in case the directory is
    # recreated later.
    assert not LOG_FILE.exists(), (
        "Pre-existing log file detected: "
        f"{LOG_FILE} {_describe_existing_path(LOG_FILE)}.\n"
        "The initial state must be clean so that the student can generate "
        "this file with the correct content and permissions."
    )