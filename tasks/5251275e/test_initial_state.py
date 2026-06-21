# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student begins the exercise.
#
# EXPECTED INITIAL CONDITIONS
#   • /home/user/incident_logs         MUST **NOT** exist.
#   • /home/user/incident_logs/incident_report.log MUST **NOT** exist.
#
# If any of these resources are already present, the tests will fail with
# a clear, actionable message so the learner knows they must begin from a
# clean slate.

import os
import stat
import pytest

HOME_DIR = "/home/user"
INCIDENT_DIR = os.path.join(HOME_DIR, "incident_logs")
INCIDENT_FILE = os.path.join(INCIDENT_DIR, "incident_report.log")


def _path_readable(path: str) -> str:
    """
    Helper that returns a human-readable description of a path’s
    existence and type for error messages.
    """
    if not os.path.exists(path):
        return f"'{path}' does not exist."
    mode = os.stat(path).st_mode
    if stat.S_ISDIR(mode):
        return f"'{path}' exists and is a directory."
    if stat.S_ISREG(mode):
        return f"'{path}' exists and is a file."
    return f"'{path}' exists but is neither a regular file nor a directory (mode {oct(mode)})."


def test_home_directory_exists():
    """Sanity check that the base /home/user directory is present."""
    assert os.path.isdir(HOME_DIR), (
        "The base directory '/home/user' is missing. "
        "This environment is not set up as expected."
    )


def test_incident_directory_absent():
    """
    The incident_logs directory must NOT exist at the beginning
    of the exercise.
    """
    assert not os.path.exists(INCIDENT_DIR), (
        "Pre-existing directory detected: /home/user/incident_logs\n"
        "A clean state is required before you start. "
        f"Current status: {_path_readable(INCIDENT_DIR)}"
    )


def test_incident_file_absent():
    """
    The incident_report.log file must NOT exist at the beginning
    of the exercise.
    """
    assert not os.path.exists(INCIDENT_FILE), (
        "Pre-existing file detected: /home/user/incident_logs/incident_report.log\n"
        "A clean state is required before you start. "
        f"Current status: {_path_readable(INCIDENT_FILE)}"
    )