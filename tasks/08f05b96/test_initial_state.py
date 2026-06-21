# test_initial_state.py
#
# This test-suite validates the *initial* operating-system / filesystem
# state before the student begins the task.  It verifies that the raw
# log material is present and that none of the “output” artefacts yet
# exist.  All paths are absolute and rooted at /home/user.

import os
from pathlib import Path

import pytest

# Base directories
HOME = Path("/home/user")
AUDIT_DIR = HOME / "audit_logs"
RAW_DIR = AUDIT_DIR / "raw"
PROCESSED_DIR = AUDIT_DIR / "processed"

# Expected raw files
AUTH_LOG = RAW_DIR / "auth.log"
SYSLOG = RAW_DIR / "syslog"

# The expected *exact* contents of auth.log (five lines, LF endings)
EXPECTED_AUTH_LOG_LINES = [
    "Oct  1 14:32:18 ubuntu2004 sudo:    alice : TTY=pts/0 ; PWD=/home/alice ; USER=root ; COMMAND=/bin/apt update",
    "Oct  1 15:01:03 ubuntu2004 sudo:    bob : TTY=pts/1 ; PWD=/home/bob ; USER=root ; COMMAND=/usr/bin/systemctl restart nginx",
    "Oct  1 16:45:55 ubuntu2004 sudo:    charlie : TTY=pts/2 ; PWD=/home/charlie ; USER=root ; COMMAND=/bin/cat /etc/shadow",
    "Oct  2 08:11:08 ubuntu2004 sshd[4242]: Failed password for invalid user guest from 203.0.113.9 port 52892 ssh2",
    "Oct  2 09:27:44 ubuntu2004 CRON[4321]: pam_unix(cron:session): session closed for user root",
]


def test_raw_directory_exists():
    """The /home/user/audit_logs/raw directory must exist."""
    assert RAW_DIR.is_dir(), f"Required directory {RAW_DIR} is missing."


def test_auth_log_exists_and_contents():
    """auth.log must exist and contain the exact five expected lines."""
    assert AUTH_LOG.is_file(), f"Required file {AUTH_LOG} is missing."

    with AUTH_LOG.open("r", encoding="utf-8") as fh:
        contents = fh.read().splitlines()

    assert (
        contents == EXPECTED_AUTH_LOG_LINES
    ), (
        f"{AUTH_LOG} does not contain the expected lines.\n"
        "Differences:\n"
        + "\n".join(
            f"  expected: {exp!r}\n       got: {got!r}"
            for exp, got in zip(EXPECTED_AUTH_LOG_LINES, contents)
            if exp != got
        )
        + (
            f"\nNumber of lines expected: {len(EXPECTED_AUTH_LOG_LINES)}, got: {len(contents)}"
            if len(contents) != len(EXPECTED_AUTH_LOG_LINES)
            else ""
        )
    )


def test_syslog_exists():
    """syslog must exist (contents are not validated)."""
    assert SYSLOG.is_file(), f"Required file {SYSLOG} is missing."


def test_processed_directory_absent():
    """The processed directory must NOT yet exist."""
    assert not PROCESSED_DIR.exists(), (
        f"Directory {PROCESSED_DIR} should not exist before the task begins."
    )


def test_audit_summary_log_absent():
    """audit_summary.log must NOT yet exist."""
    summary_log = AUDIT_DIR / "audit_summary.log"
    assert not summary_log.exists(), (
        f"{summary_log} should not exist before the task begins."
    )


def test_no_unexpected_items_under_audit_logs():
    """
    Apart from 'raw', there should be no other files/directories under
    /home/user/audit_logs/ at the start.
    """
    items = {p.name for p in AUDIT_DIR.iterdir()}
    unexpected = items - {"raw"}
    assert not unexpected, (
        "Unexpected items present in "
        f"{AUDIT_DIR}: {', '.join(sorted(unexpected))}"
    )