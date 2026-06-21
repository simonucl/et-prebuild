# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem is in the
# expected **initial** state *before* the student begins the assignment that
# creates the diagnostics directory and log file.
#
# It intentionally checks for the ABSENCE of the directory and file that the
# student is about to create, guaranteeing that the environment is clean and
# that any subsequent creation work can be attributed solely to the student’s
# actions.

import os
import pathlib
import pwd
import pytest

HOME = pathlib.Path("/home/user")
DIAG_DIR = HOME / "db_net_diagnostics"
LOG_FILE = DIAG_DIR / "2024-connection-summary.log"


def _current_username():
    """Return the username corresponding to the current real uid."""
    return pwd.getpwuid(os.getuid()).pw_name


def test_home_directory_exists_and_is_directory():
    """
    Sanity-check that /home/user exists and is a directory.  This test protects
    against mis-configured containers or CI runners where the expected home
    directory has not been provisioned.
    """
    assert HOME.exists(), "Expected home directory '/home/user' is missing."
    assert HOME.is_dir(), "'/home/user' exists but is not a directory."


def test_diagnostics_directory_does_not_exist_yet():
    """
    The diagnostics directory SHOULD NOT exist before the student starts
    working.  Its presence would indicate left-over artefacts from a previous
    run and could cause the real grader to obtain a false positive.
    """
    assert not DIAG_DIR.exists(), (
        f"'{DIAG_DIR}' already exists. The environment is not clean; please "
        "remove it before starting the exercise."
    )


def test_log_file_does_not_exist_yet():
    """
    The diagnostics log file SHOULD NOT exist before the student creates it.
    Its presence would short-circuit the exercise and hide mistakes in the
    student’s implementation.
    """
    assert not LOG_FILE.exists(), (
        f"'{LOG_FILE}' already exists. The environment is not clean; please "
        "remove it before starting the exercise."
    )