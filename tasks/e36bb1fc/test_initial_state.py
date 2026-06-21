# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the correct *initial* state **before** the learner runs any
# commands.  It checks only the artefacts that must already exist
# according to the exercise description, and nothing about the files
# that the learner is expected to create later.
#
# Rules honoured:
#   • uses only stdlib + pytest
#   • does not test for any output files / directories
#   • provides clear assertion messages on failure
#   • works with absolute paths
# ---------------------------------------------------------------------

import os
import stat
import pytest

LOG_DIR = "/home/user/logs"
AUTH_LOG = os.path.join(LOG_DIR, "auth.log")

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def _perm_bits(path):
    """Return the permission bits (the lowest 9 bits) of a file/dir."""
    return stat.S_IMODE(os.stat(path).st_mode)


# ---------------------------------------------------------------------
# Expected data for /home/user/logs/auth.log
# ---------------------------------------------------------------------

EXPECTED_LINES = [
    "Jan 10 12:00:01 host sshd[12345]: Failed password for invalid user admin from 192.168.1.100 port 51234 ssh2\n",
    "Jan 10 12:01:05 host sshd[12346]: Failed password for root from 10.0.0.5 port 49822 ssh2\n",
    "Jan 10 12:02:30 host sshd[12347]: Accepted password for john from 192.168.1.101 port 51235 ssh2\n",
    "Jan 10 12:04:44 host sshd[12348]: Failed password for alice from 172.16.0.3 port 60122 ssh2\n",
    "Jan 10 12:05:50 host sshd[12349]: Failed password for invalid user test from 203.0.113.55 port 33918 ssh2\n",
    "Jan 10 12:06:23 host sshd[12350]: Accepted password for jane from 192.168.1.102 port 51236 ssh2\n",
    "Jan 10 12:07:10 host sshd[12351]: Failed password for invalid user admin from 192.168.1.100 port 51300 ssh2\n",
    "Jan 10 12:07:35 host sshd[12352]: Failed password for invalid user guest from 192.168.1.100 port 51310 ssh2\n",
    "Jan 10 12:08:01 host sshd[12353]: Failed password for root from 10.0.0.5 port 49823 ssh2\n",
    "Jan 10 12:09:15 host sshd[12354]: Failed password for admin from 192.168.1.100 port 51320 ssh2\n",
]


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------


def test_logs_directory_exists():
    """The directory /home/user/logs/ must exist with mode >= 0755."""
    assert os.path.isdir(LOG_DIR), f"Required directory {LOG_DIR!r} is missing or not a directory."
    perms = _perm_bits(LOG_DIR)
    assert perms & 0o755 == 0o755, (
        f"Directory {LOG_DIR!r} should have permissions at least 0755 "
        f"(rwxr-xr-x); current mode is {oct(perms)}."
    )


def test_auth_log_file_exists_and_permissions():
    """Validate presence and basic properties of /home/user/logs/auth.log."""
    assert os.path.isfile(
        AUTH_LOG
    ), f"Required log file {AUTH_LOG!r} is missing or not a regular file."
    perms = _perm_bits(AUTH_LOG)
    assert perms & 0o644 == 0o644, (
        f"File {AUTH_LOG!r} must be world-readable (mode 0644 or looser); "
        f"current mode is {oct(perms)}."
    )


def test_auth_log_contents_exact():
    """The log file must contain exactly the 10 expected lines in order."""
    with open(AUTH_LOG, encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    # Check the exact number of lines
    assert (
        len(actual_lines) == 10
    ), f"{AUTH_LOG!r} should contain exactly 10 lines, found {len(actual_lines)}."

    # Check every line verbatim
    for idx, (exp, act) in enumerate(zip(EXPECTED_LINES, actual_lines), start=1):
        assert (
            exp == act
        ), f"Mismatch on line {idx} of {AUTH_LOG!r}.\nExpected: {exp!r}\nFound:    {act!r}"

    # Ensure no extra content beyond the expected
    assert actual_lines == EXPECTED_LINES, (
        f"{AUTH_LOG!r} does not match the expected content exactly."
    )