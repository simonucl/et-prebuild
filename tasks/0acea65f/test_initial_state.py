# test_initial_state.py
#
# Pytest suite that validates the *initial* environment for the
# “Compliance audit – failed SSH log-in summary” exercise.
#
# The checks intentionally fail if any prerequisite is missing *before*
# the student starts working on the task.  They verify that:
#
# 1. /home/user/audit_logs/            – exists and is a directory
# 2. /home/user/audit_logs/auth.log    – exists, is a regular file and
#                                       contains exactly the expected
#                                       twelve log lines
# 3. /home/user/audit_logs/compliance_summary.csv
#                                    – does *not* exist yet
#
# Only stdlib + pytest are used.


from pathlib import Path
import stat
import pytest

AUDIT_DIR = Path("/home/user/audit_logs")
AUTH_LOG = AUDIT_DIR / "auth.log"
SUMMARY_CSV = AUDIT_DIR / "compliance_summary.csv"

# Expected byte-for-byte content of auth.log (final newline included)
EXPECTED_AUTH_CONTENT = (
    "Jan 10 10:01:02 server sshd[12345]: Failed password for invalid user admin from 203.0.113.10 port 54321 ssh2\n"
    "Jan 10 10:05:22 server sshd[12346]: Failed password for invalid user test from 198.51.100.42 port 54421 ssh2\n"
    "Jan 10 10:07:11 server sshd[12347]: Failed password for root from 203.0.113.10 port 54456 ssh2\n"
    "Jan 10 10:15:45 server sshd[12348]: Failed password for invalid user guest from 203.0.113.10 port 54671 ssh2\n"
    "Jan 10 11:20:13 server sshd[12349]: Failed password for invalid user admin from 192.0.2.77 port 54781 ssh2\n"
    "Jan 10 12:25:39 server sshd[12350]: Failed password for invalid user user from 198.51.100.42 port 54931 ssh2\n"
    "Jan 10 13:02:54 server sshd[12351]: Failed password for root from 198.51.100.42 port 55043 ssh2\n"
    "Jan 10 15:14:22 server sshd[12352]: Failed password for invalid user admin from 203.0.113.10 port 55211 ssh2\n"
    "Jan 10 16:55:03 server sshd[12353]: Failed password for invalid user admin from 198.51.100.42 port 55344 ssh2\n"
    "Jan 10 17:35:49 server sshd[12354]: Failed password for invalid user guest from 198.51.100.42 port 55433 ssh2\n"
    "Jan 10 18:42:05 server sshd[12355]: Failed password for root from 203.0.113.10 port 55510 ssh2\n"
    "Jan 10 19:12:37 server sshd[12356]: Failed password for invalid user noob from 192.0.2.77 port 55688 ssh2\n"
)


def _mode_is_writable(mode: int) -> bool:
    """Return True if 'others', 'group', or 'user' have write permission."""
    return bool(mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def test_audit_directory_exists_and_is_writable():
    assert AUDIT_DIR.exists(), (
        f"Required directory {AUDIT_DIR} is missing. "
        "It must exist before the exercise begins."
    )
    assert AUDIT_DIR.is_dir(), f"{AUDIT_DIR} exists but is not a directory."
    mode = AUDIT_DIR.stat().st_mode
    assert _mode_is_writable(mode), (
        f"Directory {AUDIT_DIR} is not writable. "
        "Ensure it has write permission for the current user."
    )


def test_auth_log_exists_and_is_correct():
    assert AUTH_LOG.exists(), f"Log file {AUTH_LOG} is missing."
    assert AUTH_LOG.is_file(), f"{AUTH_LOG} exists but is not a regular file."

    content = AUTH_LOG.read_text(encoding="utf-8")
    assert content == EXPECTED_AUTH_CONTENT, (
        f"{AUTH_LOG} content differs from the expected initial data.\n"
        "The file must contain exactly the twelve provided log lines "
        "so the student can parse predictable input."
    )


def test_summary_csv_does_not_exist_yet():
    assert not SUMMARY_CSV.exists(), (
        f"{SUMMARY_CSV} already exists, but the student has not yet generated "
        "the compliance summary.  Remove the file so the exercise starts from "
        "a clean slate."
    )