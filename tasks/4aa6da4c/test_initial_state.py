# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the student’s solution is executed.  It checks that:
#
# 1. The sample log file /home/user/work/logs/auth.log exists,
#    is readable, and contains exactly the 15 expected lines.
# 2. The parent directory /home/user/work/logs exists.
# 3. The target output directory /home/user/work/filtered
#    does NOT yet exist (the student must create it).
#
# Only the Python stdlib and pytest are used.

import os
from pathlib import Path

import pytest

LOGS_DIR = Path("/home/user/work/logs")
AUTH_LOG = LOGS_DIR / "auth.log"
FILTERED_DIR = Path("/home/user/work/filtered")

# The authoritative 15-line fixture for auth.log
EXPECTED_AUTH_LINES = [
    "Jan 23 10:11:03 server sshd[1024]: Failed password for root from 192.168.1.55 port 53422 ssh2",
    "Jan 23 10:11:05 server sshd[1024]: Failed password for invalid user admin from 192.168.1.55 port 53422 ssh2",
    "Jan 23 10:11:10 server sshd[1024]: Failed password for root from 203.0.113.7 port 41702 ssh2",
    "Jan 23 10:11:15 server sshd[1024]: Failed password for user1 from 203.0.113.7 port 41702 ssh2",
    "Jan 23 10:11:19 server sshd[1025]: Accepted password for root from 192.168.1.100 port 53423 ssh2",
    "Jan 23 10:11:23 server sshd[1025]: Accepted password for alice from 192.168.1.100 port 53423 ssh2",
    "Jan 23 10:12:03 server sshd[1026]: Failed password for root from 198.51.100.23 port 60001 ssh2",
    "Jan 23 10:12:30 server sshd[1027]: Accepted password for root from 198.51.100.23 port 60001 ssh2",
    "Jan 23 10:12:35 server sshd[1027]: Failed password for root from 198.51.100.23 port 60001 ssh2",
    "Jan 23 10:12:40 server sshd[1027]: Failed password for guest from 198.51.100.23 port 60001 ssh2",
    "Jan 23 10:13:01 server sshd[1028]: Failed password for root from 10.0.0.5 port 55321 ssh2",
    "Jan 23 10:13:05 server sshd[1028]: Accepted password for root from 10.0.0.5 port 55321 ssh2",
    "Jan 23 10:13:07 server sshd[1028]: Accepted password for bob from 10.0.0.5 port 55321 ssh2",
    "Jan 23 10:13:09 server sshd[1028]: Failed password for background from 10.0.0.5 port 55321 ssh2",
    "Jan 23 10:13:11 server sshd[1028]: Failed password for root from 10.0.0.5 port 55321 ssh2",
]


def test_logs_directory_exists():
    assert LOGS_DIR.is_dir(), (
        f"Required directory {LOGS_DIR} is missing. "
        "The starter files should already include this directory."
    )


def test_auth_log_exists_and_matches_expected_content():
    assert AUTH_LOG.is_file(), (
        f"Required file {AUTH_LOG} is missing. "
        "The starter files should already include this file."
    )

    with AUTH_LOG.open("r", encoding="utf-8") as fh:
        lines = [line.rstrip("\n") for line in fh]

    assert (
        len(lines) == len(EXPECTED_AUTH_LINES)
    ), f"{AUTH_LOG} should have exactly {len(EXPECTED_AUTH_LINES)} lines, found {len(lines)}."

    # Check each line verbatim to catch any accidental modifications
    for idx, (observed, expected) in enumerate(zip(lines, EXPECTED_AUTH_LINES), start=1):
        assert (
            observed == expected
        ), f"Line {idx} of {AUTH_LOG} differs from the expected fixture.\nExpected: {expected}\nFound:    {observed}"


def test_filtered_directory_does_not_yet_exist():
    assert not FILTERED_DIR.exists(), (
        f"Directory {FILTERED_DIR} already exists before the task begins. "
        "The student’s solution is expected to create this directory."
    )