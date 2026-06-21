# test_initial_state.py
#
# Pytest suite that verifies the machine is in the expected
# *initial* state – i.e. nothing related to the forthcoming
# “compliance” exercise is present yet.
#
# These checks purposefully fail as soon as they detect any
# artefact that the student is supposed to create later
# (/home/user/compliance, its script, its logs, or the summary
# file).  If any of those items already exist, the environment
# has been tampered with or the student ran their solution
# prematurely, and the test suite must alert them.

import os
import re
import stat
import pytest

COMPLIANCE_DIR = "/home/user/compliance"
SCRIPT_PATH = os.path.join(COMPLIANCE_DIR, "audit_trail.sh")
SUMMARY_PATH = os.path.join(COMPLIANCE_DIR, "latest_audit_summary.txt")
LOG_REGEX = re.compile(r"^audit_[0-9]{8}_[0-9]{6}\.log$")


def _collect_matching_logs():
    """Return a list of log files that already match the required name."""
    if not os.path.isdir(COMPLIANCE_DIR):
        return []
    return [
        entry
        for entry in os.listdir(COMPLIANCE_DIR)
        if LOG_REGEX.match(entry)
    ]


def test_compliance_directory_absent():
    """
    The /home/user/compliance directory must NOT exist before the student starts.
    """
    assert not os.path.exists(COMPLIANCE_DIR), (
        f"Directory {COMPLIANCE_DIR} already exists; "
        "it should be created by the student during the exercise, "
        "not before."
    )


def test_audit_script_absent():
    """
    The audit_trail.sh script must NOT exist yet.
    """
    assert not os.path.exists(SCRIPT_PATH), (
        f"File {SCRIPT_PATH} already exists; "
        "it must be written by the student later."
    )


def test_no_log_files_present():
    """
    No audit_YYYYMMDD_HHMMSS.log files should be present yet.
    """
    stray_logs = _collect_matching_logs()
    assert not stray_logs, (
        f"Found unexpected log file(s) in {COMPLIANCE_DIR}: {', '.join(stray_logs)}. "
        "No log files should exist before the audit script is first run."
    )


def test_summary_file_absent():
    """
    The latest_audit_summary.txt file must NOT exist yet.
    """
    assert not os.path.exists(SUMMARY_PATH), (
        f"File {SUMMARY_PATH} already exists; "
        "it should be generated only after the student runs their script."
    )