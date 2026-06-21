# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the student carries out the assignment described in the prompt.
#
# What we assert:
#   • /home/user exists                        (sanity check)
#   • /home/user/api_checks  does NOT exist    (student must create it)
#   • /home/user/api_checks/api_test_report.log does NOT exist
#   • The `curl` executable is available in PATH (required tool)
#
# All assertions fail with explicit, human-readable error messages.

import os
import shutil
import stat
import pytest

HOME_DIR = "/home/user"
API_DIR = os.path.join(HOME_DIR, "api_checks")
LOG_FILE = os.path.join(API_DIR, "api_test_report.log")


def test_home_directory_exists():
    """Ensure the base home directory is present."""
    assert os.path.isdir(HOME_DIR), (
        f"Expected home directory '{HOME_DIR}' to exist, "
        "but it is missing."
    )


def test_api_checks_directory_absent():
    """
    The /home/user/api_checks directory should NOT exist yet.
    The student is responsible for creating it.
    """
    assert not os.path.exists(API_DIR), (
        f"Directory '{API_DIR}' already exists, but it should NOT be present "
        "before the student runs their solution."
    )


def test_api_test_report_log_absent():
    """
    The final CSV log file must not be present before the student acts.
    """
    assert not os.path.exists(LOG_FILE), (
        f"Found unexpected pre-existing file '{LOG_FILE}'. "
        "The system should be in a clean state before the task starts."
    )


def test_curl_is_available():
    """curl must be available in the execution environment."""
    curl_path = shutil.which("curl")
    assert curl_path is not None, (
        "The 'curl' executable was not found in PATH. "
        "It is required for the assignment."
    )
    # Extra sanity: ensure the path points to an executable file
    assert os.path.isfile(curl_path) and os.access(curl_path, os.X_OK), (
        f"The path '{curl_path}' is not an executable file."
    )