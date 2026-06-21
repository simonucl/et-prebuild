# test_initial_state.py
#
# Pytest suite to validate the *initial* state of the operating system
# before the student performs any actions for the “DailyHello” compliance
# task.  These tests assert that:
#
# 1. The current (non-root) user has NO crontab installed.
# 2. /home/user/compliance/ does NOT exist.
# 3. /home/user/hello.log does NOT exist.
#
# Only the Python standard library and pytest are used.

import os
import subprocess
import sys
from pathlib import Path

import pytest


HOME_DIR = Path("/home/user")
COMPLIANCE_DIR = HOME_DIR / "compliance"
HELLO_LOG = HOME_DIR / "hello.log"


@pytest.fixture(scope="module")
def crontab_listing():
    """
    Attempt to list the current user's crontab.
    Returns (returncode, stdout + stderr lower-cased).
    """
    # `crontab -l` exits with a non-zero status code and prints a
    # “no crontab …” message when the user has no crontab.
    result = subprocess.run(
        ["crontab", "-l"],
        capture_output=True,
        text=True,
    )
    combined_output = (result.stdout + result.stderr).lower()
    return result.returncode, combined_output


def test_home_directory_exists():
    assert HOME_DIR.is_dir(), (
        f"Expected home directory {HOME_DIR!s} to exist for the tests to be "
        f"meaningful, but it was not found."
    )


def test_no_user_crontab(crontab_listing):
    rc, output = crontab_listing
    assert rc != 0, (
        "There should be NO crontab for the current user, but `crontab -l` "
        "returned exit code 0 (indicating a crontab is present)."
    )
    assert "no crontab" in output, (
        "Expected `crontab -l` to report 'no crontab' for the current user, "
        f"but got this instead:\n{output}"
    )


def test_compliance_directory_absent():
    assert not COMPLIANCE_DIR.exists(), (
        f"Directory {COMPLIANCE_DIR!s} must NOT exist before the student’s "
        "commands are executed."
    )


def test_hello_log_absent():
    assert not HELLO_LOG.exists(), (
        f"File {HELLO_LOG!s} must NOT exist before the student’s commands "
        "are executed."
    )