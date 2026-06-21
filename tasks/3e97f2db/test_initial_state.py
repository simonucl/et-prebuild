# test_initial_state.py
#
# This pytest suite validates the initial operating-system / filesystem
# state *before* the student performs any action for the “incident-response
# analyst” exercise.  It checks that the provided log file exists with the
# exact expected contents and that the output directory / files that the
# student must create do **not** yet exist.

import os
import stat
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the ground-truth initial state
# ---------------------------------------------------------------------------

AUTH_LOG_PATH = Path("/home/user/logs/auth.log")
IR_DIR_PATH = Path("/home/user/ir")
FAILURES_LOG_PATH = IR_DIR_PATH / "failures.log"

EXPECTED_AUTH_CONTENT = (
    "Nov  5 10:15:42 ubuntu sshd[12345]: Failed password for invalid user admin "
    "from 192.168.1.10 port 54321 ssh2\n"
    "Nov  5 10:15:45 ubuntu sshd[12346]: Failed password for invalid user root "
    "from 192.168.1.10 port 54322 ssh2\n"
    "Nov  5 10:15:50 ubuntu sshd[12347]: Failed password for invalid user admin "
    "from 192.168.1.10 port 54321 ssh2\n"
    "Nov  5 10:16:00 ubuntu sshd[12348]: Failed password for invalid user guest "
    "from 192.168.1.20 port 54323 ssh2\n"
    "Nov  5 10:16:05 ubuntu sshd[12349]: Failed password for invalid user guest "
    "from 192.168.1.20 port 54323 ssh2\n"
    "Nov  5 10:17:10 ubuntu sshd[12350]: Failed password for invalid user test "
    "from 203.0.113.5 port 60001 ssh2\n"
    "Nov  6 09:01:12 ubuntu sshd[22345]: Failed password for invalid user admin "
    "from 192.168.1.10 port 54324 ssh2\n"
)

EXPECTED_AUTH_PERMISSIONS = 0o644  # rw-r--r--


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _file_mode(path: Path) -> int:
    """Return the permission bits (e.g., 0o644) of a file or raise if missing."""
    return stat.S_IMODE(path.stat().st_mode)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_auth_log_exists_and_is_regular_file():
    assert AUTH_LOG_PATH.exists(), (
        f"Required log file not found: {AUTH_LOG_PATH}"
    )
    assert AUTH_LOG_PATH.is_file(), (
        f"Expected {AUTH_LOG_PATH} to be a regular file."
    )


def test_auth_log_permissions():
    mode = _file_mode(AUTH_LOG_PATH)
    assert mode == EXPECTED_AUTH_PERMISSIONS, (
        f"{AUTH_LOG_PATH} should have permissions "
        f"{oct(EXPECTED_AUTH_PERMISSIONS)}, but has {oct(mode)}."
    )


def test_auth_log_exact_contents():
    actual = AUTH_LOG_PATH.read_text(encoding="utf-8")
    assert actual == EXPECTED_AUTH_CONTENT, (
        f"{AUTH_LOG_PATH} contents do not match the expected initial data.\n"
        f"--- Expected ---\n{EXPECTED_AUTH_CONTENT}\n"
        f"--- Actual ---\n{actual}"
    )


def test_ir_directory_does_not_yet_exist():
    assert not IR_DIR_PATH.exists(), (
        f"{IR_DIR_PATH} should not exist before the student runs any commands."
    )


def test_failures_log_does_not_yet_exist():
    assert not FAILURES_LOG_PATH.exists(), (
        f"{FAILURES_LOG_PATH} should not exist before the student creates it."
    )