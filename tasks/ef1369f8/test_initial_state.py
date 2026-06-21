# test_initial_state.py
#
# Pytest suite that validates the expected *initial* operating-system
# / filesystem state before the student’s solution is executed.
#
# The checks performed:
#   1. /home/user/logs/ssh_auth.log
#        • must exist
#        • must be a regular, readable file
#        • must contain the exact eight log lines specified (including \n)
#   2. /home/user/compliance  MUST NOT exist
#   3. /home/user/compliance/login_audit.csv MUST NOT exist (implicitly
#      covered by #2 but checked explicitly for clarity)
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest

LOG_PATH = "/home/user/logs/ssh_auth.log"
COMPLIANCE_DIR = "/home/user/compliance"
AUDIT_CSV = os.path.join(COMPLIANCE_DIR, "login_audit.csv")

# The eight expected lines of the ssh authentication log
EXPECTED_LOG_LINES = [
    "Jan 12 10:23:45 server sshd[12345]: Accepted password for alice from 192.168.1.10 port 53422 ssh2\n",
    "Jan 12 10:25:12 server sshd[12346]: Failed password for invalid user dave from 192.168.1.20 port 53468 ssh2\n",
    "Jan 12 10:30:01 server sshd[12347]: Accepted password for bob from 192.168.1.11 port 53478 ssh2\n",
    "Jan 12 11:01:02 server sshd[12348]: Accepted password for carol from 192.168.1.12 port 53479 ssh2\n",
    "Jan 12 11:15:22 server sshd[12349]: Accepted password for alice from 192.168.1.10 port 53490 ssh2\n",
    "Jan 12 12:45:22 server sshd[12350]: Accepted password for bob from 192.168.1.11 port 53500 ssh2\n",
    "Jan 12 12:55:22 server sshd[12351]: Failed password for root from 192.168.1.31 port 53501 ssh2\n",
    "Jan 12 13:25:22 server sshd[12352]: Accepted password for alice from 192.168.1.10 port 53502 ssh2\n",
]


def assert_readable_regular_file(path: str) -> None:
    """Helper that asserts *path* exists, is a regular file and is readable."""
    assert os.path.exists(path), f"Expected file {path!s} to exist, but it does not."
    assert os.path.isfile(path), f"{path!s} exists but is not a regular file."
    mode = os.stat(path).st_mode
    is_readable = bool(mode & (stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH))
    assert is_readable, f"File {path!s} exists but is not readable."


def test_ssh_auth_log_exists_and_contents():
    """Validate presence, readability, and exact contents of ssh_auth.log."""
    assert_readable_regular_file(LOG_PATH)

    with open(LOG_PATH, "r", encoding="utf-8", newline="") as fh:
        lines = fh.readlines()

    # Easy-to-diagnose failures:
    assert (
        len(lines) == len(EXPECTED_LOG_LINES)
    ), (
        f"{LOG_PATH} is expected to contain {len(EXPECTED_LOG_LINES)} lines, "
        f"but actually contains {len(lines)} lines."
    )

    for i, (actual, expected) in enumerate(zip(lines, EXPECTED_LOG_LINES), start=1):
        assert (
            actual == expected
        ), (
            f"Line {i} of {LOG_PATH} does not match expected content.\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}"
        )


def test_compliance_directory_absent():
    """Ensure /home/user/compliance does NOT exist at the outset."""
    assert not os.path.exists(
        COMPLIANCE_DIR
    ), (
        f"The directory {COMPLIANCE_DIR} should NOT exist before the task "
        "is performed, but it does."
    )


def test_login_audit_csv_absent():
    """Even if the directory were present, login_audit.csv must not yet exist."""
    assert not os.path.exists(
        AUDIT_CSV
    ), (
        f"The file {AUDIT_CSV} should NOT exist before the task is performed, "
        "but it does."
    )