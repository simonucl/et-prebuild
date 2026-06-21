# test_initial_state.py
#
# Pytest suite that validates the operating-system / file-system
# BEFORE the student begins the “binary-artifact curator” task.
#
# The requirements document lists a set of directories, scripts,
# cron-files, and logs that **must eventually exist**.  Prior to any
# work, however, NONE of them should be present.  These tests make sure
# we start from that clean slate so that subsequent grading is reliable.
#
# We use only the Python standard library + pytest, as required.

import os
import stat
import pytest

# ----------------------------------------------------------------------
# Constants derived from the task description
# ----------------------------------------------------------------------

HOME = "/home/user"

# Directories that should NOT exist yet
REQUIRED_DIRS = [
    f"{HOME}/artifacts",
    f"{HOME}/artifacts/incoming",
    f"{HOME}/artifacts/archive",
    f"{HOME}/artifacts/logs",
    f"{HOME}/scripts",
    f"{HOME}/cron.d",
]

# Script that the student will create
SCRIPT_PATH = f"{HOME}/scripts/archive_old_artifacts.sh"

# Cron file that the student will create
CRON_PATH = f"{HOME}/cron.d/artifact_curator"

# Log file that the student will create
LOG_PATH = f"{HOME}/artifacts/logs/archive.log"

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------


def _msg_path_should_not_exist(path: str) -> str:
    """Return a helpful assertion-failure message."""
    return (
        f"\n\nThe path {path!r} already exists, but it should NOT be present "
        "before the student starts the assignment.\n"
        "Please remove it so that the environment is clean.\n"
    )


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------


@pytest.mark.parametrize("path", REQUIRED_DIRS)
def test_required_directories_absent(path):
    """
    None of the directories that the student must create
    should exist at the starting point.
    """
    assert not os.path.exists(path), _msg_path_should_not_exist(path)


def test_script_absent():
    """
    The archiving script must NOT exist before the student writes it.
    """
    assert not os.path.exists(
        SCRIPT_PATH
    ), _msg_path_should_not_exist(SCRIPT_PATH)


def test_cron_file_absent():
    """
    The cron file must NOT exist before the student creates it.
    """
    assert not os.path.exists(CRON_PATH), _msg_path_should_not_exist(CRON_PATH)


def test_log_file_absent():
    """
    The log file must NOT exist before the first script execution.
    """
    assert not os.path.exists(LOG_PATH), _msg_path_should_not_exist(LOG_PATH)