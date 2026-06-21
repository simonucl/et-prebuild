# test_initial_state.py
#
# This pytest suite validates that the **starting** operating-system state
# is clean, i.e. none of the artefacts the student is about to create
# already exist.  If any of these tests fail, it means the workspace
# has been pre-populated (or polluted) with files, directories or cron
# jobs that should only appear **after** the student completes the task.

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# Constants for the paths / text we will check.
NETWORK_DIR = "/home/user/network_checks"
LOG_FILE = f"{NETWORK_DIR}/connectivity.log"
EXPECTED_CRON_LINE = (
    "*/5 * * * * ping -c 3 8.8.8.8 >> /home/user/network_checks/connectivity.log 2>&1"
)


def test_network_checks_directory_does_not_exist():
    """
    The directory /home/user/network_checks should NOT exist yet.
    The student will create it as part of the task.
    """
    assert not Path(NETWORK_DIR).exists(), (
        f"The directory {NETWORK_DIR!r} already exists. "
        "It should be created by the student during the exercise, "
        "so it must not be present at the start."
    )


def test_connectivity_log_does_not_exist():
    """
    The log file must not be present before the student starts the task.
    """
    assert not Path(LOG_FILE).exists(), (
        f"The file {LOG_FILE!r} already exists. "
        "It should be created (or touched) by the student during the exercise."
    )


def _get_user_crontab():
    """
    Retrieve the current user's crontab.
    Returns a tuple (return_code, stdout, stderr) similar to subprocess.run.
    If the 'crontab' binary is missing, the test is skipped.
    """
    if shutil.which("crontab") is None:
        pytest.skip("'crontab' command not available on this system.")

    result = subprocess.run(
        ["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # When there is *no* crontab installed for the user, the exit code is non-zero
    # and stderr contains a message such as "no crontab for <user>".
    return result.returncode, result.stdout, result.stderr


def test_user_crontab_is_empty():
    """
    Before the student acts, the user must NOT already have the prescribed
    cron job (or any job at all).  We consider a clean slate to be:
        - no crontab at all, OR
        - an entirely empty crontab (0 lines),
      but *definitely* not one containing the required job line.
    """
    rc, stdout, _stderr = _get_user_crontab()

    if rc != 0:
        # No crontab for user: this is the expected, "clean" situation.
        return

    # A crontab exists.  Strip whitespace and comments; there should be nothing.
    cleaned_lines = [
        ln for ln in stdout.splitlines() if ln.strip() and not ln.lstrip().startswith("#")
    ]

    assert (
        EXPECTED_CRON_LINE not in cleaned_lines
    ), "The target cron job is already present in the user crontab; this should be added *after* the task is attempted."

    assert (
        not cleaned_lines
    ), "The user already has one or more active cron jobs. The initial state must have an empty crontab so the exercise starts from a known baseline."