# test_initial_state.py
#
# Pytest suite that verifies the operating-system state **before** the student
# performs any action for the “failed SSH-login summary” task.
#
# The expected pristine state is:
#   • Directory  /home/user/logs            exists and is writable.
#   • File       /home/user/logs/auth.log   exists with exactly the 5 log lines
#     listed in the specification (and nothing else in that directory).
#   • File       /home/user/logs/failed_ssh_summary.log  MUST NOT exist yet.
#
# These checks ensure the environment matches the truth table supplied in the
# task description.  Any deviation will surface as a clear, actionable pytest
# failure message.

import os
import stat
from pathlib import Path

import pytest

LOGS_DIR = Path("/home/user/logs")
AUTH_LOG = LOGS_DIR / "auth.log"
SUMMARY_LOG = LOGS_DIR / "failed_ssh_summary.log"

EXPECTED_AUTH_LINES = [
    "Jan 10 2025 08:23:45 server sshd[12345]: Failed password for invalid user admin from 192.168.1.10 port 54321 ssh2",
    "Jan 10 2025 09:15:02 server sshd[23456]: Failed password for root from 203.0.113.5 port 54433 ssh2",
    "Jan 11 2025 10:00:00 server sshd[34567]: Failed password for user john from 198.51.100.7 port 60000 ssh2",
    "Jan 11 2025 10:05:25 server sshd[34568]: Failed password for user mike from 198.51.100.8 port 60001 ssh2",
    "Jan 11 2025 23:59:59 server sshd[40000]: Failed password for invalid user test from 198.51.100.9 port 60002 ssh2",
]


def test_logs_directory_exists_and_writable():
    """The /home/user/logs directory must exist and be writable by the user."""
    assert LOGS_DIR.is_dir(), (
        f"Directory {LOGS_DIR} is expected to exist, "
        "but it is missing."
    )

    # Check that the current user can write to the directory.
    can_write = os.access(LOGS_DIR, os.W_OK)
    assert can_write, (
        f"Directory {LOGS_DIR} exists but is not writable by the current user."
    )


def test_auth_log_exists_with_expected_content():
    """auth.log must exist and contain exactly the five specified lines."""
    assert AUTH_LOG.is_file(), (
        f"Expected file {AUTH_LOG} to exist, but it is missing."
    )

    with AUTH_LOG.open("r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh.readlines()]

    assert len(lines) == 5, (
        f"{AUTH_LOG} should contain exactly 5 lines, "
        f"but found {len(lines)} line(s)."
    )

    for idx, (found, expected) in enumerate(zip(lines, EXPECTED_AUTH_LINES), start=1):
        assert found == expected, (
            f"Line {idx} of {AUTH_LOG} does not match the expected content.\n"
            f"Expected: {expected!r}\n"
            f"Found:    {found!r}"
        )


def test_failed_summary_log_does_not_exist_yet():
    """failed_ssh_summary.log should NOT exist before the student runs their solution."""
    assert not SUMMARY_LOG.exists(), (
        f"{SUMMARY_LOG} should not exist yet. "
        "The student’s script is expected to create it."
    )


def test_no_extra_files_present():
    """
    The logs directory must contain only the initial auth.log file
    (no summary log or any other stray files/directories).
    """
    contents = sorted(p.name for p in LOGS_DIR.iterdir())
    expected_contents = ["auth.log"]
    assert contents == expected_contents, (
        f"{LOGS_DIR} contains unexpected items.\n"
        f"Expected: {expected_contents}\n"
        f"Found:    {contents}"
    )