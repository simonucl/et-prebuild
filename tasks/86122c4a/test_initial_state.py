# test_initial_state.py
#
# Pytest suite that validates the operating-system state
# *before* the user begins solving the exercise.  It checks
# only the pre-existing artefacts; it does NOT touch or look
# for any of the files that the user is asked to create.
#
# Requirements verified:
#   • /home/user/logs/          exists and is a directory
#   • /home/user/logs/auth.log  exists, is a file, has 8 exact lines
#
# The “output” directory and files are *not* inspected here,
# per the specification.

import os
import stat
import pytest


LOG_DIR = "/home/user/logs"
AUTH_LOG = os.path.join(LOG_DIR, "auth.log")

# The authoritative list of log lines expected in auth.log
EXPECTED_LOG_LINES = [
    "Jan 10 10:00:00 localhost sshd[12345]: Accepted password for alice from 192.168.1.5 port 52222 ssh2",
    "Jan 10 10:00:05 localhost sshd[12346]: Failed password for bob from 192.168.1.6 port 52223 ssh2",
    "Jan 10 10:00:10 localhost sshd[12347]: Failed password for alice from 192.168.1.7 port 52224 ssh2",
    "Jan 10 10:00:15 localhost sshd[12348]: Accepted password for carol from 192.168.1.8 port 52225 ssh2",
    "Jan 10 10:00:20 localhost sshd[12349]: Failed password for carol from 192.168.1.9 port 52226 ssh2",
    "Jan 10 10:00:25 localhost sshd[12350]: Accepted password for bob from 192.168.1.10 port 52227 ssh2",
    "Jan 10 10:00:30 localhost sshd[12351]: Accepted password for alice from 192.168.1.11 port 52228 ssh2",
    "Jan 10 10:00:35 localhost sshd[12352]: Failed password for dave from 192.168.1.12 port 52229 ssh2",
]


def _mode_bits(path):
    "Return permission bits (e.g., 0o755) for a path."
    return stat.S_IMODE(os.stat(path).st_mode)


def test_log_directory_exists_and_permissions():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory {LOG_DIR!r} is missing. "
        "It must exist before the student starts."
    )
    perms = _mode_bits(LOG_DIR)
    expected = 0o755
    assert perms == expected, (
        f"Directory {LOG_DIR!r} exists but permissions are {oct(perms)}, "
        f"expected {oct(expected)}."
    )


def test_auth_log_file_exists_and_permissions():
    assert os.path.isfile(AUTH_LOG), (
        f"Required file {AUTH_LOG!r} is missing. "
        "Create or place the initial log file before running the exercise."
    )
    perms = _mode_bits(AUTH_LOG)
    expected = 0o644
    assert perms == expected, (
        f"File {AUTH_LOG!r} exists but permissions are {oct(perms)}, "
        f"expected {oct(expected)}."
    )


def test_auth_log_has_exact_expected_content():
    """
    The auth.log file must contain *exactly* the eight prescribed lines.
    Trailing whitespace and the final newline are ignored for robustness,
    but every logical line must match the specification.
    """
    with open(AUTH_LOG, "r", encoding="utf-8") as fh:
        raw_lines = fh.readlines()

    # Strip newline and trailing spaces for comparison
    cleaned_lines = [ln.rstrip() for ln in raw_lines]

    assert cleaned_lines == EXPECTED_LOG_LINES, (
        f"{AUTH_LOG!r} does not contain the expected contents.\n"
        f"Expected ({len(EXPECTED_LOG_LINES)} lines):\n"
        + "\n".join(EXPECTED_LOG_LINES)
        + "\n\n"
        f"Found ({len(cleaned_lines)} lines):\n"
        + "\n".join(cleaned_lines)
        + "\n"
    )