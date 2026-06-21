# test_initial_state.py
#
# This pytest suite verifies that the starting file-system state
# required for the “SSH compliance audit” exercise is present and
# correct *before* the student begins writing any solution code.
#
# WHAT IS CHECKED
# ---------------
# 1. The mandatory directories exist (/home/user/compliance and logs/).
# 2. The log file /home/user/compliance/logs/audit.log exists.
# 3. The log file contains exactly the 11 expected lines—no more,
#    no fewer, and in the correct order.
#
# If any of these conditions are not met the test will fail with a
# clear, actionable error message.

import os
import pytest


COMPLIANCE_DIR = "/home/user/compliance"
LOGS_DIR = os.path.join(COMPLIANCE_DIR, "logs")
AUDIT_LOG = os.path.join(LOGS_DIR, "audit.log")

EXPECTED_LOG_LINES = [
    "2023-10-01T09:15:21Z IP=192.168.1.45 USER=root RESULT=FAIL",
    "2023-10-01T09:15:23Z IP=192.168.1.45 USER=root RESULT=FAIL",
    "2023-10-01T10:05:11Z IP=10.0.0.12 USER=admin RESULT=FAIL",
    "2023-10-02T08:22:04Z IP=172.16.0.4 USER=admin RESULT=SUCCESS",
    "2023-10-03T11:01:45Z IP=192.168.1.45 USER=root RESULT=FAIL",
    "2023-10-04T03:14:07Z IP=203.0.113.8 USER=test RESULT=FAIL",
    "2023-10-04T04:20:23Z IP=203.0.113.8 USER=test RESULT=FAIL",
    "2023-10-04T05:33:18Z IP=203.0.113.8 USER=test RESULT=FAIL",
    "2023-10-05T13:08:55Z IP=10.0.0.12 USER=admin RESULT=FAIL",
    "2023-10-05T14:20:55Z IP=203.0.113.8 USER=test RESULT=SUCCESS",
    "2023-10-06T07:44:33Z IP=198.51.100.2 USER=guest RESULT=FAIL",
]


def test_directories_exist():
    """Ensure the required directory hierarchy exists."""
    assert os.path.isdir(
        COMPLIANCE_DIR
    ), f"Missing directory: {COMPLIANCE_DIR}"
    assert os.path.isdir(
        LOGS_DIR
    ), f"Missing directory: {LOGS_DIR}"


def test_audit_log_exists():
    """Ensure the audit.log file exists at the expected absolute path."""
    assert os.path.isfile(
        AUDIT_LOG
    ), f"Missing file: {AUDIT_LOG}"


def test_audit_log_contents():
    """
    Verify the audit.log file contains exactly the expected 11 lines
    (order and content must match).
    """
    with open(AUDIT_LOG, encoding="utf-8") as fh:
        actual_lines = [ln.rstrip("\n") for ln in fh]

    assert actual_lines == EXPECTED_LOG_LINES, (
        "Contents of audit.log do not match the expected initial data.\n\n"
        "Expected:\n"
        + "\n".join(EXPECTED_LOG_LINES)
        + "\n\nActual:\n"
        + "\n".join(actual_lines)
    )