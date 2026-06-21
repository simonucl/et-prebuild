# test_initial_state.py
#
# This pytest file validates the **initial** state of the filesystem
# for the “SSH authentication failures” exercise.  It checks only the
# prerequisites that must be in place *before* the student carries out
# the task.  It deliberately avoids testing for / creating / referencing
# any of the output artefacts that the student will generate.

import os
import stat
import pytest

LOG_DIR = "/home/user/logs"
AUTH_LOG = os.path.join(LOG_DIR, "auth.log")

# The exact lines that must already be present in /home/user/logs/auth.log
EXPECTED_AUTH_LOG_LINES = [
    "Jan 12 07:21:43 server sshd[24516]: Failed password for invalid user admin from 192.168.1.50 port 53460 ssh2",
    "Jan 12 07:22:10 server sshd[24520]: Failed password for root from 10.0.0.2 port 60234 ssh2",
    "Jan 12 07:24:31 server sshd[24540]: Failed password for user john from 192.168.1.50 port 53480 ssh2",
    "Jan 12 07:25:00 server sshd[24545]: Failed password for invalid user test from 203.0.113.77 port 40022 ssh2",
    "Jan 12 07:25:18 server sshd[24551]: Failed password for invalid user admin from 192.168.1.50 port 53492 ssh2",
    "Jan 12 07:26:02 server sshd[24600]: Failed password for root from 10.0.0.2 port 60288 ssh2",
    "Jan 12 07:27:45 server sshd[24612]: Failed password for invalid user admin from 198.51.100.23 port 42310 ssh2",
    "Jan 12 07:28:01 server sshd[24618]: Failed password for root from 192.168.1.50 port 53504 ssh2",
    "Jan 12 07:29:19 server sshd[24630]: Failed password for invalid user guest from 203.0.113.77 port 40034 ssh2",
    "Jan 12 07:30:00 server sshd[24642]: Failed password for root from 10.0.0.2 port 60312 ssh2",
    "Jan 12 07:31:10 server sshd[24650]: Failed password for invalid user admin from 192.168.1.50 port 53528 ssh2",
    "Jan 12 07:31:55 server sshd[24655]: Failed password for root from 10.0.0.2 port 60324 ssh2",
]


def test_logs_directory_exists_and_writable():
    """Verify that /home/user/logs exists and is writable by the user."""
    assert os.path.isdir(LOG_DIR), (
        f"Required directory '{LOG_DIR}' does not exist."
    )

    # Check that the directory is writable (user-writable bit set)
    mode = os.stat(LOG_DIR).st_mode
    assert bool(mode & stat.S_IWUSR), (
        f"Directory '{LOG_DIR}' is not writable by the user."
    )


def test_auth_log_exists():
    """Verify that /home/user/logs/auth.log exists and is a regular file."""
    assert os.path.isfile(AUTH_LOG), (
        f"Required file '{AUTH_LOG}' is missing."
    )


def test_auth_log_permissions():
    """auth.log must be world-readable (0644)."""
    mode = os.stat(AUTH_LOG).st_mode & 0o777
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"File '{AUTH_LOG}' permissions are {oct(mode)}, expected {oct(expected_mode)}."
    )


def test_auth_log_contents_exact():
    """Check that auth.log contains exactly the expected 12 lines (order + text)."""
    with open(AUTH_LOG, "r", encoding="utf-8") as fh:
        actual_lines = [line.rstrip("\n") for line in fh.readlines()]

    assert actual_lines == EXPECTED_AUTH_LOG_LINES, (
        "The contents of 'auth.log' do not match the expected initial dataset.\n"
        "If you modified or replaced the file, restore it to its original state."
    )