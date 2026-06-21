# test_initial_state.py
# Pytest suite that validates the initial state of the workstation **before**
# the student performs any actions for the “filtered copy” exercise.
#
# This test file checks only the pre-existing historical log at
#     /home/user/logs/config_changes.log
# and nothing related to the expected output directory or file.
#
# Requirements verified:
#   • File exists and is a regular file.
#   • File permissions are exactly 0644 (rw-r--r--).
#   • File contents match the canonical reference _byte-for-byte_,
#     including a single trailing Unix newline and no extra lines.

import os
import stat
from pathlib import Path

import pytest

LOG_PATH = Path("/home/user/logs/config_changes.log")

# Canonical contents of the log file — keep the final \n!
EXPECTED_CONTENT = (
    "[2023-05-01 09:15:23] CHANGED: /etc/nginx/nginx.conf\n"
    "[2023-05-01 09:15:23] BACKUP: /etc/nginx/nginx.conf.bak\n"
    "[2023-05-01 09:18:47] CHANGED: /etc/ssh/sshd_config\n"
    "[2023-05-01 09:20:02] SKIPPED: /etc/hosts\n"
    "[2023-05-01 09:21:10] CHANGED: /etc/php/php.ini\n"
    "[2023-05-01 09:25:30] DRYRUN: /etc/fstab\n"
    "[2023-05-01 09:27:54] CHANGED: /etc/systemd/system.conf\n"
)


def test_log_file_exists_and_is_regular():
    """Verify that the source log file exists and is a regular file."""
    assert LOG_PATH.exists(), (
        f"Expected log file {LOG_PATH} is missing."
    )
    assert LOG_PATH.is_file(), (
        f"Expected log file {LOG_PATH} exists but is not a regular file."
    )


def test_log_file_permissions():
    """Verify that the log file has mode 0644 (rw-r--r--)."""
    mode = LOG_PATH.stat().st_mode
    actual_perms = stat.S_IMODE(mode)
    expected_perms = 0o644
    assert actual_perms == expected_perms, (
        f"Permissions for {LOG_PATH} are {oct(actual_perms)}, "
        f"expected {oct(expected_perms)}."
    )


def test_log_file_contents_exact_match():
    """
    Verify that the contents of the log file match EXACTLY the expected
    reference, including a single trailing newline.
    """
    with LOG_PATH.open("r", encoding="utf-8", newline="") as fh:
        data = fh.read()

    assert data == EXPECTED_CONTENT, (
        "Contents of the log file do not match the canonical reference.\n"
        "----- Expected -----\n"
        f"{EXPECTED_CONTENT!r}\n"
        "------ Actual ------\n"
        f"{data!r}\n"
        "--------------------"
    )