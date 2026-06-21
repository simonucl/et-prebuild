# test_initial_state.py
#
# This pytest file validates the *initial* state of the operating‐system
# environment **before** the student performs any action.  It confirms that
# the required directory and log file exist, are accessible, and contain the
# expected data against which the student’s solution will be graded.
#
# NOTE:  We explicitly **do not** test for the existence of the student’s
# output file (/home/user/logs/failed_login_report.txt) because it should not
# exist yet.  Any such validation belongs in the *post-exercise* test suite.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"
AUTH_LOG = LOG_DIR / "auth.log"

# Expected exact (stripped) lines inside /home/user/logs/auth.log
EXPECTED_AUTH_LOG_LINES = [
    "Jan 21 10:10:10 host sshd[12345]: Failed password for invalid user admin from 192.168.1.20 port 55874 ssh2",
    "Jan 21 10:10:12 host sshd[12346]: Failed password for root from 192.168.1.30 port 55875 ssh2",
    "Jan 21 10:10:13 host sshd[12347]: Accepted password for user1 from 192.168.1.40 port 55876 ssh2",
    "Jan 21 10:10:15 host sshd[12348]: Failed password for user2 from 192.168.1.50 port 55877 ssh2",
    "Jan 21 11:00:00 host sshd[12349]: Failed password for invalid user test from 192.168.1.60 port 55878 ssh2",
    "Jan 21 11:05:00 host sshd[12350]: Failed password for user3 from 192.168.1.70 port 55879 ssh2",
    "Jan 21 12:00:00 host sshd[12351]: Accepted password for user4 from 192.168.1.80 port 55880 ssh2",
]


def _strip_newlines(lines):
    """
    Helper to strip trailing CR/LF from a list of byte or str lines.
    Returns a list of str without line terminators.
    """
    cleaned = []
    for ln in lines:
        if isinstance(ln, bytes):
            ln = ln.decode("utf-8", errors="replace")
        cleaned.append(ln.rstrip("\r\n"))
    return cleaned


@pytest.mark.order(1)
def test_logs_directory_exists_and_writable():
    """
    Verify that /home/user/logs exists, is a directory, and is writable by the
    current user.
    """
    assert LOG_DIR.exists(), f"Directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."

    # Check writability: user must have write permission on the directory
    can_write = os.access(LOG_DIR, os.W_OK)
    if not can_write:
        perms = oct(LOG_DIR.stat().st_mode & 0o777)
        raise AssertionError(
            f"Directory {LOG_DIR} is not writable by the current user "
            f"(mode: {perms})."
        )


@pytest.mark.order(2)
def test_auth_log_exists_with_expected_content():
    """
    Ensure that /home/user/logs/auth.log exists and contains the exact seven
    lines provided in the exercise description, and that exactly five of those
    lines include the phrase 'Failed password'.
    """
    assert AUTH_LOG.exists(), f"Log file {AUTH_LOG} is missing."
    assert AUTH_LOG.is_file(), f"{AUTH_LOG} exists but is not a regular file."

    with AUTH_LOG.open("rb") as fh:
        raw_lines = fh.readlines()

    # Strip newline characters for comparison
    lines = _strip_newlines(raw_lines)

    # 1. Exact line count
    assert len(lines) == 7, (
        f"{AUTH_LOG} should contain exactly 7 lines, but it contains "
        f"{len(lines)} line(s)."
    )

    # 2. Exact content match
    if lines != EXPECTED_AUTH_LOG_LINES:
        diff_lines = [
            f"EXPECTED: {exp}\nACTUAL  : {act}"
            for exp, act in zip(EXPECTED_AUTH_LOG_LINES, lines)
            if exp != act
        ]
        extra = ""
        if len(lines) != len(EXPECTED_AUTH_LOG_LINES):
            extra = (
                f"\nLine count differs. Expected {len(EXPECTED_AUTH_LOG_LINES)}, "
                f"got {len(lines)}."
            )
        raise AssertionError(
            f"The content of {AUTH_LOG} does not match the expected lines.\n"
            + "\n".join(diff_lines)
            + extra
        )

    # 3. Validate the metric that the learner must report
    failed_count = sum("Failed password" in ln for ln in lines)
    assert (
        failed_count == 5
    ), f"Expected 5 lines containing 'Failed password', found {failed_count}."