# test_initial_state.py
"""
Pytest suite to validate the initial filesystem state **before** the student
works on help-desk ticket #551.

Checks performed:
1. /home/user/mock_logs/ exists and is a directory.
2. /home/user/mock_logs/auth.log exists, is a file, and contains the exact six
   expected lines (including newlines, order, and spacing).
3. /home/user/ticket-551-failed-passwords.log must NOT exist yet (it will be
   created by the student).

Only stdlib and pytest are used, and full absolute paths are tested.
"""

import os
from pathlib import Path

import pytest

# Absolute paths to be used throughout the tests
MOCK_LOG_DIR = Path("/home/user/mock_logs")
AUTH_LOG_PATH = MOCK_LOG_DIR / "auth.log"
TARGET_PATH = Path("/home/user/ticket-551-failed-passwords.log")

# Expected exact contents (each line must end with '\n')
EXPECTED_AUTH_LOG_LINES = [
    "Jun  1 08:14:52 localhost sshd[1245]: Failed password for invalid user admin from 10.0.0.15 port 42422 ssh2\n",
    "Jun  1 08:14:55 localhost sshd[1245]: Connection closed by 10.0.0.15 port 42422 [preauth]\n",
    "Jun  1 08:15:02 localhost sshd[1247]: Failed password for root from 10.0.0.15 port 42423 ssh2\n",
    "Jun  1 08:15:04 localhost sshd[1247]: Connection closed by 10.0.0.15 port 42423 [preauth]\n",
    "Jun  1 08:16:27 localhost sshd[1251]: Accepted password for john from 10.0.0.16 port 42424 ssh2\n",
    "Jun  1 08:16:30 localhost sshd[1251]: Failed password for user john from 10.0.0.16 port 42424 ssh2\n",
]


def test_mock_log_directory_exists_and_is_dir():
    """Ensure /home/user/mock_logs/ exists and is a directory."""
    assert MOCK_LOG_DIR.exists(), (
        f"Required directory {MOCK_LOG_DIR} is missing."
    )
    assert MOCK_LOG_DIR.is_dir(), (
        f"{MOCK_LOG_DIR} exists but is not a directory."
    )


def test_auth_log_exists_and_exact_contents():
    """Ensure auth.log exists and contains exactly the expected six lines."""
    assert AUTH_LOG_PATH.exists(), (
        f"Required file {AUTH_LOG_PATH} is missing."
    )
    assert AUTH_LOG_PATH.is_file(), (
        f"{AUTH_LOG_PATH} exists but is not a regular file."
    )

    with AUTH_LOG_PATH.open("r", encoding="utf-8") as f:
        actual_lines = f.readlines()

    assert actual_lines == EXPECTED_AUTH_LOG_LINES, (
        "Contents of auth.log do not match the expected initial state.\n"
        "Expected:\n"
        + "".join(EXPECTED_AUTH_LOG_LINES)
        + "\nActual:\n"
        + "".join(actual_lines)
    )


def test_target_file_does_not_exist_yet():
    """
    Ensure the output file does NOT exist before the student runs their command.
    """
    assert not TARGET_PATH.exists(), (
        f"The target file {TARGET_PATH} should NOT exist yet. "
        "It must be created by the student's solution."
    )