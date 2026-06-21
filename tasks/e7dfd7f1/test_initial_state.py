# test_initial_state.py
#
# This pytest suite validates the initial, pre-task operating-system state.
# It checks ONLY the prerequisite artefacts that must already exist before
# the student performs any actions.  In particular, it confirms that the
# simulated APT session log is present, has the correct permissions, and
# contains the exact expected content.
#
# NOTE:  Per the grading-infrastructure rules *no tests are made for any of
#        the output files or directories that the student is asked to create
#        (e.g. /home/user/devops or pkg_debug.log).  This file is concerned
#        solely with the starting conditions.

import os
import stat
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------

LOG_DIR = Path("/home/user/sim_logs")
LOG_FILE = LOG_DIR / "apt_history.log"
EXPECTED_PERMS = 0o644

EXPECTED_LINES = [
    "Start-Date: 2024-04-15  09:21:07",
    "Commandline: apt-get install nginx",
    "Install: nginx:amd64 (1.18.0-6ubuntu14.3, automatic)",
    "End-Date: 2024-04-15  09:21:09",
    "Start-Date: 2024-04-15  09:22:45",
    "Commandline: apt-get upgrade",
    "E: Sub-process /usr/bin/dpkg returned an error code (1)",
    "Err:1 http://archive.ubuntu.com/ubuntu focal-updates/main amd64 libc6 amd64 2.31-0ubuntu9.9",
    "Fetched 0 B in 3s (0 B/s)",
    "End-Date: 2024-04-15  09:22:48",
]

# ---------------------------------------------------------------------------


def test_log_directory_exists():
    """
    The directory /home/user/sim_logs must exist and be a directory.
    """
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_log_file_exists():
    """
    The log file must exist and be a regular file.
    """
    assert LOG_FILE.exists(), f"Required log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."


def test_log_file_permissions():
    """
    The log file must have 0644 permissions (rw-r--r--).
    """
    mode = LOG_FILE.stat().st_mode
    perms = stat.S_IMODE(mode)
    assert (
        perms == EXPECTED_PERMS
    ), f"{LOG_FILE} permissions are {oct(perms)}, expected {oct(EXPECTED_PERMS)}."


def test_log_file_contents():
    """
    The log file must contain exactly the 10 expected lines, in order,
    with no extra or missing lines.
    """
    with LOG_FILE.open("r", encoding="utf-8") as fp:
        actual_lines = [line.rstrip("\n") for line in fp.readlines()]

    assert (
        actual_lines == EXPECTED_LINES
    ), (
        "Contents of apt_history.log do not match the expected initial state.\n"
        "Differences:\n"
        f"EXPECTED ({len(EXPECTED_LINES)} lines):\n"
        + "\n".join(EXPECTED_LINES)
        + "\n\n"
        f"ACTUAL ({len(actual_lines)} lines):\n"
        + "\n".join(actual_lines)
    )