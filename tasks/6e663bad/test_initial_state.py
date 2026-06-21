# test_initial_state.py
#
# This test-suite validates the *initial* operating system / filesystem
# state that must be present **before** the student starts solving the
# assignment.  It intentionally does **not** look for any of the output
# artefacts that the student is supposed to create later on.
#
# Checked invariants:
#   1.  /home/user/logs  exists, is a directory and has permission 0700.
#   2.  The directory contains exactly one file named  auth.log .
#   3.  /home/user/logs/auth.log  exists, is a regular file, has
#       permission 0644, and contains exactly the 14 log-lines that were
#       provided in the task description (with LF line endings).
#
# Any deviation from these expectations is reported via clear pytest
# assertion messages so that the student immediately knows what is
# missing or unexpected.

import os
import stat
from pathlib import Path

import pytest

LOG_DIR = Path("/home/user/logs")
AUTH_LOG = LOG_DIR / "auth.log"

# The 14 expected log lines without the trailing '\n'
EXPECTED_AUTH_LOG_LINES = [
    "Jan 10 12:05:10 server sshd[1234]: Accepted password for alice from 192.168.0.2 port 54022 ssh2",
    "Jan 10 12:07:15 server sshd[1235]: Failed password for bob from 192.168.0.3 port 54023 ssh2",
    "Jan 10 12:08:45 server sshd[1236]: Accepted password for bob from 192.168.0.3 port 54023 ssh2",
    "Jan 10 12:15:01 server sshd[1237]: Failed password for charlie from 192.168.0.4 port 54024 ssh2",
    "Jan 10 12:16:35 server sshd[1238]: Failed password for charlie from 192.168.0.4 port 54024 ssh2",
    "Jan 10 12:16:39 server sshd[1239]: Failed password for charlie from 192.168.0.4 port 54024 ssh2",
    "Jan 10 12:16:40 server sshd[1239]: ACCOUNT LOCKED: charlie; too many failures",
    "Jan 10 12:18:12 server sshd[1240]: Accepted password for alice from 192.168.0.2 port 54022 ssh2",
    "Jan 10 13:01:09 server sshd[1241]: Failed password for bob from 192.168.0.3 port 54023 ssh2",
    "Jan 10 13:05:22 server sshd[1242]: Accepted password for dave from 192.168.0.5 port 54025 ssh2",
    "Jan 10 14:22:33 server sshd[1243]: Failed password for dave from 192.168.0.5 port 54025 ssh2",
    "Jan 10 14:25:37 server sshd[1244]: password expired for eve; account needs password change",
    "Jan 10 14:25:38 server sshd[1245]: Accepted password for eve from 192.168.0.6 port 54026 ssh2",
    "Jan 10 14:30:01 server sshd[1246]: Failed password for alice from 192.168.0.2 port 54022 ssh2",
]


def _mode(path: Path) -> int:
    """Return the permission bits (like 0o700) of a file/directory."""
    return stat.S_IMODE(path.stat().st_mode)


def test_log_directory_exists_and_has_correct_mode():
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."
    expected_mode = 0o700
    actual_mode = _mode(LOG_DIR)
    assert (
        actual_mode == expected_mode
    ), f"{LOG_DIR} should have mode {oct(expected_mode)}, but has {oct(actual_mode)}."


def test_log_directory_contains_only_auth_log():
    contents = sorted(p.name for p in LOG_DIR.iterdir())
    assert (
        contents == ["auth.log"]
    ), f"{LOG_DIR} must contain exactly one file named 'auth.log'. Found: {contents}"


def test_auth_log_exists_is_file_and_has_correct_mode():
    assert AUTH_LOG.exists(), f"Required file {AUTH_LOG} is missing."
    assert AUTH_LOG.is_file(), f"{AUTH_LOG} exists but is not a regular file."
    expected_mode = 0o644
    actual_mode = _mode(AUTH_LOG)
    assert (
        actual_mode == expected_mode
    ), f"{AUTH_LOG} should have mode {oct(expected_mode)}, but has {oct(actual_mode)}."


def test_auth_log_content_matches_expected_lines():
    with AUTH_LOG.open("r", encoding="utf-8", newline="") as fh:
        file_lines = fh.read().splitlines()  # removes the trailing '\n'
    assert (
        file_lines == EXPECTED_AUTH_LOG_LINES
    ), (
        f"{AUTH_LOG} does not contain the expected content.\n"
        f"Expected {len(EXPECTED_AUTH_LOG_LINES)} lines but found {len(file_lines)}.\n"
        "Differences (first mismatch shown by pytest diff):"
    )