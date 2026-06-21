# test_initial_state.py
#
# This pytest test-suite verifies the pristine state of the operating system
# before the student begins their work on the “myapp” configuration report.
#
# It asserts that the input audit-log file exists at the expected absolute
# location and contains exactly the four audit entries specified in the task
# description (each terminated by a single newline).  No checks are performed
# on any output artefacts that the student will later create.

import os
import stat
import pytest

AUDIT_LOG_PATH = "/home/user/config_audit.log"

EXPECTED_LINES = [
    "2023-07-01 12:00:00 | myapp.conf | ADDED   | enable_feature=true\n",
    "2023-07-01 12:05:00 | myapp.conf | CHANGED | max_connections 100->150\n",
    "2023-07-02 08:00:00 | myapp.conf | CHANGED | timeout 30->45\n",
    "2023-07-03 09:30:00 | myapp.conf | REMOVED | debug_mode\n",
]


def test_audit_log_exists_and_is_regular_file():
    """
    The audit log must exist and be a regular file, not a directory, symlink,
    device, etc.
    """
    assert os.path.exists(AUDIT_LOG_PATH), (
        f"Expected audit log not found at {AUDIT_LOG_PATH}"
    )
    assert os.path.isfile(AUDIT_LOG_PATH), (
        f"{AUDIT_LOG_PATH} exists but is not a regular file"
    )


def test_audit_log_permissions():
    """
    The file should have user-writable default permissions (rw-r--r-- == 0o644).
    The test is lenient to umask variations by merely ensuring the owner can
    read/write and that no execute bits are set.
    """
    mode = os.stat(AUDIT_LOG_PATH).st_mode
    # Owner must have read/write; no execute bits for anyone.
    owner_perms = stat.S_IRUSR | stat.S_IWUSR
    forbidden_exec = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    assert mode & owner_perms == owner_perms, (
        f"{AUDIT_LOG_PATH} should be readable and writable by owner"
    )
    assert mode & forbidden_exec == 0, (
        f"{AUDIT_LOG_PATH} must not be executable"
    )


def test_audit_log_contents_exact_match():
    """
    The file must contain exactly the four predefined lines, each with a
    trailing newline character and no extra content before or after.
    """
    with open(AUDIT_LOG_PATH, encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == EXPECTED_LINES, (
        "The contents of the audit log do not match the expected initial "
        "state.\n"
        "Expected lines:\n"
        f"{''.join(EXPECTED_LINES)}\n"
        "Actual lines:\n"
        f"{''.join(actual_lines)}"
    )