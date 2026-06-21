# test_initial_state.py
#
# Pytest suite to validate that the filesystem is in the expected
# *initial* state before the student performs any actions for the
# “project_utils / secure_scripts” task.
#
# These tests purposely check that none of the target artefacts
# (directory, script file, verification log) exist yet.  This guarantees
# the environment is clean and that the student’s work will be the only
# thing that creates them.

import os
from pathlib import Path
import pytest

# Constant paths used throughout the assertions
HOME = Path("/home/user")
UTILS_DIR = HOME / "project_utils" / "secure_scripts"
BACKUP_SCRIPT = UTILS_DIR / "backup.sh"
PERM_LOG = HOME / "perm_check.log"


def _format_exists(path: Path) -> str:
    """
    Helper for producing a consistent, readable error message that
    indicates whether a given path exists and, if so, what kind of
    filesystem object it is.
    """
    if not path.exists():
        return f"{path} does not exist (as expected)."
    info = "directory" if path.is_dir() else "file"
    return f"{path} already exists and is a {info}."


def test_home_directory_exists():
    """
    Sanity-check: /home/user itself must exist for the subsequent task.
    We *expect* it to be present.
    """
    assert HOME.exists(), "Precondition failed: /home/user does not exist."
    assert HOME.is_dir(), "/home/user exists but is not a directory."


def test_utils_directory_absent():
    """
    The directory /home/user/project_utils/secure_scripts must NOT exist
    before the student starts the task.
    """
    assert not UTILS_DIR.exists(), (
        "Unexpected pre-existing directory found:\n"
        f"{_format_exists(UTILS_DIR)}\n"
        "Please remove or rename it before running the exercise."
    )


def test_backup_script_absent():
    """
    The backup.sh stub must NOT exist before the student creates it.
    """
    assert not BACKUP_SCRIPT.exists(), (
        "Unexpected pre-existing file found:\n"
        f"{_format_exists(BACKUP_SCRIPT)}\n"
        "Please remove or rename it before running the exercise."
    )


def test_perm_log_absent():
    """
    The verification log perm_check.log must NOT exist yet.
    """
    assert not PERM_LOG.exists(), (
        "Unexpected pre-existing log file found:\n"
        f"{_format_exists(PERM_LOG)}\n"
        "Please remove or rename it before running the exercise."
    )