# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must
# exist **before** the student executes any commands for the task
# “CRITICAL vulnerabilities policy-as-code”.
#
# DO NOT modify this file.  It deliberately **does not** test for any of
# the artefacts the student is supposed to create (e.g. the
# critical_vulns.csv file or the new log entry).  Instead, it confirms
# that the starting environment is exactly as specified in the
# task description so that later grading steps are meaningful.
#
# The tests rely only on Python’s standard library plus pytest.

import os
from pathlib import Path

HOME = Path("/home/user")
REPORTS_DIR = HOME / "reports"
POLICY_DIR = REPORTS_DIR / "policy"
VULN_REPORT = REPORTS_DIR / "vuln_report.csv"
ACTION_LOG = REPORTS_DIR / "action.log"


def test_reports_directory_exists():
    assert REPORTS_DIR.is_dir(), (
        f"Required directory {REPORTS_DIR} is missing. "
        "The task description states that /home/user/reports must pre-exist."
    )


def test_policy_directory_exists_and_is_empty():
    assert POLICY_DIR.is_dir(), (
        f"Required directory {POLICY_DIR} is missing. "
        "It must exist (and be writable) before the student starts."
    )

    # The policy directory must be empty at the outset so that the
    # student’s new file appears there unambiguously.
    remaining_entries = [p.name for p in POLICY_DIR.iterdir() if not p.name.startswith(".")]
    assert remaining_entries == [], (
        f"{POLICY_DIR} is expected to be empty initially, but found: {remaining_entries}"
    )


def test_vuln_report_exists_and_correct_content():
    assert VULN_REPORT.is_file(), (
        f"Required CSV report {VULN_REPORT} is missing. "
        "The student cannot proceed without this source file."
    )

    expected_lines = [
        "CVE_ID,SEVERITY,DESCRIPTION,AFFECTED_PACKAGE\n",
        "CVE-2023-1111,MEDIUM,OpenSSL minor issue,openssl\n",
        "CVE-2023-2222,CRITICAL,Kernel privilege escalation,linux-kernel\n",
        "CVE-2023-3333,LOW,Typo in man page,man-db\n",
        "CVE-2023-4444,CRITICAL,Remote code execution,libssh\n",
        "CVE-2023-5555,HIGH,Potential DoS in zlib,zlib\n",
    ]

    with VULN_REPORT.open("r", encoding="utf-8") as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, (
        f"The contents of {VULN_REPORT} do not match the expected initial "
        "report.  Any discrepancy would break downstream grading.\n"
        "Expected:\n"
        + "".join(expected_lines)
        + "\nActual:\n"
        + "".join(actual_lines)
    )

    # Ensure UNIX line endings only.
    assert all("\r" not in line for line in actual_lines), (
        f"{VULN_REPORT} must use UNIX (LF) line endings only; "
        "carriage-return characters were found."
    )


def test_action_log_absent_or_valid_file():
    """
    The action.log file may or may not exist initially.
    If it does exist, verify that it is a regular file (not a directory).
    Its contents are *not* validated here because they are unspecified.
    """
    if ACTION_LOG.exists():
        assert ACTION_LOG.is_file(), (
            f"{ACTION_LOG} exists but is not a regular file. "
            "It should either be absent or an ordinary file that "
            "the student can append to."
        )