# test_initial_state.py
#
# This pytest file validates that the operating-system / filesystem
# is in the expected “clean slate” before the student begins work on
# the firewall-change staging task.  If any of these tests fail, the
# environment is already in a mutated state and the assignment cannot
# be graded reliably.

import os
import stat
import pytest

HOME_DIR = "/home/user"
SCRIPT_PATH = f"{HOME_DIR}/firewall_update.sh"
LOG_PATH = f"{HOME_DIR}/firewall_config.log"
BIN_BASH = "/bin/bash"


def test_home_directory_exists():
    """The base directory /home/user must exist."""
    assert os.path.isdir(HOME_DIR), (
        f"Expected the home directory {HOME_DIR!r} to exist, "
        "but it was not found."
    )


def test_bin_bash_exists_and_executable():
    """The /bin/bash interpreter must be present and executable."""
    assert os.path.isfile(BIN_BASH), (
        f"Expected {BIN_BASH!r} to be a regular file, but it does not exist."
    )
    assert os.access(BIN_BASH, os.X_OK), (
        f"{BIN_BASH!r} exists but is not executable. "
        "A valid bash interpreter is required for the assignment."
    )


def test_firewall_script_absent():
    """
    The firewall_update.sh script must NOT exist yet.
    Creating this script is part of the student’s task.
    """
    assert not os.path.exists(SCRIPT_PATH), (
        f"The file {SCRIPT_PATH!r} already exists. "
        "The environment must start without this file so that its creation "
        "can be graded."
    )


def test_firewall_log_absent():
    """
    The firewall_config.log file must NOT exist yet.
    Creating this log is part of the student’s task.
    """
    assert not os.path.exists(LOG_PATH), (
        f"The file {LOG_PATH!r} already exists. "
        "The environment must start without this file so that its creation "
        "can be graded."
    )