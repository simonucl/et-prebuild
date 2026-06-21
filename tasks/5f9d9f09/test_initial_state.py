# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any actions for the “Compliance scenario – simple
# regex-based log filtering” exercise.
#
# The tests assert that:
#   1. The audit directory exists and is writable.
#   2. The original sample log exists and contains exactly the expected
#      13 lines (including order and trailing newline characters).
#   3. None of the three output artefacts that the student is supposed to
#      create are present yet.
#
# Only Python’s stdlib and pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
AUDIT_DIR = HOME / "audit"
SYSLOG = AUDIT_DIR / "syslog_sample.log"

# Output files that must *not* exist yet
FAILED_LOG = AUDIT_DIR / "extracted_failed.log"
ROOT_SESSIONS_LOG = AUDIT_DIR / "root_sessions.log"
COUNTS_TXT = AUDIT_DIR / "audit_counts.txt"

# The 13 canonical lines that have to be present in syslog_sample.log
EXPECTED_SYSLOG_LINES = [
    "Jan 12 14:35:02 server1 sshd[1024]: Failed password for invalid user admin from 192.168.1.25 port 54421 ssh2\n",
    "Jan 12 14:36:15 server1 sshd[1025]: Session opened for user root by (uid=0)\n",
    "Jan 12 14:37:20 server1 sshd[1025]: Session closed for user root\n",
    "Jan 12 14:40:55 server1 sshd[1030]: Failed password for root from 192.168.1.26 port 54422 ssh2\n",
    "Jan 12 14:42:03 server1 sshd[1031]: Accepted password for user bob from 192.168.1.27 port 54423 ssh2\n",
    "Jan 12 14:42:04 server1 sshd[1031]: session opened for user bob by (uid=0)\n",
    "Jan 12 14:45:10 server1 sudo: pam_unix(sudo:session): session opened for user root by bob(uid=0)\n",
    "Jan 12 14:46:33 server1 sshd[1036]: Failed password for invalid user guest from 192.168.1.28 port 54424 ssh2\n",
    "Jan 12 14:48:57 server1 sshd[1040]: Failed password for root from 192.168.1.29 port 54425 ssh2\n",
    "Jan 12 14:49:01 server1 sshd[1040]: Failed password for root from 192.168.1.29 port 54425 ssh2\n",
    "Jan 12 14:50:12 server1 sshd[1045]: Session opened for user root by (uid=0)\n",
    "Jan 12 14:51:20 server1 sshd[1045]: Session closed for user root\n",
    "Jan 12 14:52:30 server1 sshd[1050]: Failed password for invalid user test from 192.168.1.30 port 54426 ssh2\n",
]


def test_audit_directory_exists_and_is_writable():
    assert AUDIT_DIR.exists(), (
        f"The audit directory {AUDIT_DIR} is missing. It must exist before "
        "the exercise starts."
    )
    assert AUDIT_DIR.is_dir(), (
        f"{AUDIT_DIR} exists but is not a directory."
    )
    assert os.access(AUDIT_DIR, os.W_OK), (
        f"The audit directory {AUDIT_DIR} is not writable by the current user."
    )


def test_syslog_sample_exists_with_exact_content():
    assert SYSLOG.exists(), (
        f"The sample syslog file {SYSLOG} is missing."
    )
    assert SYSLOG.is_file(), (
        f"{SYSLOG} exists but is not a regular file."
    )

    with SYSLOG.open("r", encoding="utf-8") as fp:
        actual_lines = fp.readlines()

    # Fail fast if the number of lines is wrong
    assert len(actual_lines) == len(EXPECTED_SYSLOG_LINES), (
        f"{SYSLOG} should contain exactly {len(EXPECTED_SYSLOG_LINES)} lines "
        f"but contains {len(actual_lines)}."
    )

    # Line-by-line comparison for full fidelity (order, spelling, trailing \n)
    mismatches = [
        (idx + 1, exp, act)
        for idx, (exp, act) in enumerate(zip(EXPECTED_SYSLOG_LINES, actual_lines))
        if exp != act
    ]
    assert not mismatches, (
        "The content of syslog_sample.log does not match the expected lines. "
        "First mismatch:\n"
        f"  Line {mismatches[0][0]} expected: {mismatches[0][1]!r}\n"
        f"  Line {mismatches[0][0]} actual:   {mismatches[0][2]!r}"
    )


@pytest.mark.parametrize(
    "path_", [FAILED_LOG, ROOT_SESSIONS_LOG, COUNTS_TXT],
    ids=["extracted_failed.log", "root_sessions.log", "audit_counts.txt"],
)
def test_output_files_do_not_yet_exist(path_):
    assert not path_.exists(), (
        f"Output file {path_} already exists. The student task has not yet "
        "been executed, so no output files should be present."
    )