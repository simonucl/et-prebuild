# test_initial_state.py
#
# This pytest suite validates that the **initial** operating-system state
# matches the specification given in the task description.
#
# IMPORTANT:  These tests only examine the *pre-existing* artefacts that must
#             already be on the filesystem BEFORE the student starts working.
#
# Rules respected:
#   • Uses only stdlib + pytest
#   • Checks absolute paths
#   • Does NOT look for any output artefacts
#   • Provides clear failure messages

import os
import stat
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #

LOG_DIR = Path("/home/user/logs")
ACCESS_LOG = LOG_DIR / "access.log"

# Expected contents of /home/user/logs/access.log (including the final LF)
EXPECTED_LOG_CONTENT = (
    "127.0.0.1 - - [01/Jan/2023:10:00:00 +0000] \"GET /index.html HTTP/1.1\" 200 1024\n"
    "192.168.0.10 - - [01/Jan/2023:10:00:01 +0000] \"GET /about HTTP/1.1\" 200 512\n"
    "10.0.0.5 - - [01/Jan/2023:10:00:02 +0000] \"POST /login HTTP/1.1\" 401 256\n"
    "127.0.0.1 - - [01/Jan/2023:10:00:03 +0000] \"GET /doesnotexist HTTP/1.1\" 404 128\n"
    "127.0.0.1 - - [01/Jan/2023:10:00:04 +0000] \"GET /index.html HTTP/1.1\" 200 1024\n"
    "10.0.0.5 - - [01/Jan/2023:10:00:05 +0000] \"POST /login HTTP/1.1\" 401 256\n"
    "192.168.0.10 - - [01/Jan/2023:10:00:06 +0000] \"GET /contact HTTP/1.1\" 200 512\n"
    "192.168.0.11 - - [01/Jan/2023:10:00:07 +0000] \"GET /index.html HTTP/1.1\" 500 128\n"
    "127.0.0.1 - - [01/Jan/2023:10:00:08 +0000] \"GET /index.html HTTP/1.1\" 200 1024\n"
    "192.168.0.11 - - [01/Jan/2023:10:00:09 +0000] \"GET /index.html HTTP/1.1\" 500 128\n"
    "10.0.0.5 - - [01/Jan/2023:10:00:10 +0000] \"POST /login HTTP/1.1\" 401 256\n"
    "192.168.0.10 - - [01/Jan/2023:10:00:11 +0000] \"GET /about HTTP/1.1\" 200 512\n"
)


# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #

def _mode(path: Path) -> int:
    """Return the permission bits of *path* (e.g. 0o755)."""
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_log_directory_exists_and_permissions():
    """The directory /home/user/logs must exist and be readable (mode 755)."""
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."

    perms = _mode(LOG_DIR)
    expected = 0o755
    assert perms == expected, (
        f"{LOG_DIR} has permissions {oct(perms)}, expected {oct(expected)}."
    )


def test_access_log_exists_and_permissions():
    """The file /home/user/logs/access.log must exist with mode 644."""
    assert ACCESS_LOG.exists(), f"Required log file {ACCESS_LOG} is missing."
    assert ACCESS_LOG.is_file(), f"{ACCESS_LOG} exists but is not a regular file."

    perms = _mode(ACCESS_LOG)
    expected = 0o644
    assert perms == expected, (
        f"{ACCESS_LOG} has permissions {oct(perms)}, expected {oct(expected)}."
    )


def test_access_log_contents_exact_match():
    """
    The access log must contain exactly the expected 12 lines (including the
    trailing newline on the last line).
    """
    actual = ACCESS_LOG.read_text(encoding="utf-8")
    # Direct string comparison gives the clearest diff if the assertion fails.
    assert (
        actual == EXPECTED_LOG_CONTENT
    ), (
        "The content of /home/user/logs/access.log does not match the expected "
        "pre-population.\n"
        "Hint: run 'diff -u expected actual' to see the exact difference."
    )