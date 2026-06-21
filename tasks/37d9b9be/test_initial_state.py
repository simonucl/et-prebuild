# test_initial_state.py
#
# Pytest suite that verifies the **initial** operating-system / filesystem
# state *before* the student has carried out any instructions in the task
# “auth-service virtual-environment creation”.
#
# The tests purposefully assert that:
#   1. The virtual-environment directory does **NOT** yet exist.
#   2. The verification log file either does **NOT** exist, or, if it does,
#      its *last* non-empty line is **NOT** the final required marker
#      string ("AUTH-SERVICE VENV READY").
#
# A failing test tells the student that the environment has already been
# modified and must be cleaned up before starting the exercise.

import os
import pytest
from pathlib import Path

# Constants used throughout the test module
VENVS_DIR = Path("/home/user/services/auth-service/venv")
LOG_FILE = Path("/home/user/services/setup_logs/venv_creation.log")
EXPECTED_MARKER = "AUTH-SERVICE VENV READY"


def test_venv_directory_does_not_exist_yet():
    """
    Ensure that the Python virtual-environment directory for auth-service
    does **NOT** exist before the student starts the task.  Presence of this
    directory would indicate that the exercise has already been attempted
    (or that the environment is not pristine).
    """
    assert not VENVS_DIR.exists(), (
        f"The directory {VENVS_DIR} already exists. "
        "Please remove it before proceeding so that you can create a fresh "
        "virtual environment at exactly this path."
    )


def test_log_file_missing_or_without_final_marker():
    """
    The verification log file should either:
      • not exist, or
      • exist but NOT yet contain the required marker string on its very last
        non-empty line.

    If the file is completely absent we pass immediately.
    If it is present, we read it and inspect the last non-empty line.
    """
    if not LOG_FILE.exists():
        # No file yet ⇒ initial state is correct.
        return

    # Read file and obtain last non-empty line (strip newline characters).
    with LOG_FILE.open("r", encoding="utf-8") as fp:
        lines = [ln.rstrip("\n") for ln in fp.readlines()]

    # Filter out any empty lines at the end that could have been left behind.
    while lines and lines[-1] == "":
        lines.pop()

    # If, after stripping, we have no lines, the file is effectively empty.
    if not lines:
        return

    last_line = lines[-1]
    assert last_line != EXPECTED_MARKER, (
        f"The file {LOG_FILE} already ends with the required marker:\n"
        f"    {EXPECTED_MARKER}\n"
        "This suggests the task might have been completed previously. "
        "Please reset the environment (or remove this line) before starting."
    )