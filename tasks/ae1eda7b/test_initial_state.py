# test_initial_state.py
#
# This pytest suite validates that the operating-system state is ready for the
# student.  It checks ONLY the pre-existing resources that the assignment
# depends on.  It does *not* look for any files or directories the student is
# supposed to create.
#
# What we verify:
#   1. /home/user/incidents exists and is a directory.
#   2. /home/user/incidents/alerts.log exists, is a regular file, is readable,
#      and contains exactly the expected 11 lines (no more, no less, no extra
#      whitespace).

import os
import stat
import pytest

INCIDENTS_DIR = "/home/user/incidents"
ALERTS_LOG = os.path.join(INCIDENTS_DIR, "alerts.log")

EXPECTED_LINES = [
    "2024-05-06T12:01:02Z ERROR auth-service",
    "2024-05-06T12:01:03Z WARN payment-service",
    "2024-05-06T12:01:04Z ERROR auth-service",
    "2024-05-06T12:01:05Z CRITICAL inventory-service",
    "2024-05-06T12:01:06Z ERROR payment-service",
    "2024-05-06T12:01:07Z ERROR auth-service",
    "2024-05-06T12:01:08Z WARN auth-service",
    "2024-05-06T12:01:09Z ERROR shipping-service",
    "2024-05-06T12:01:10Z ERROR payment-service",
    "2024-05-06T12:01:11Z CRITICAL auth-service",
]

def test_incidents_directory_exists():
    """The base directory for incident files must be present."""
    assert os.path.exists(INCIDENTS_DIR), (
        f"Required directory {INCIDENTS_DIR!r} is missing."
    )
    assert os.path.isdir(INCIDENTS_DIR), (
        f"{INCIDENTS_DIR!r} exists but is not a directory."
    )

def test_alerts_log_file_presence_and_type():
    """alerts.log must exist and be a regular readable file."""
    assert os.path.exists(ALERTS_LOG), (
        f"Required file {ALERTS_LOG!r} is missing."
    )
    st = os.stat(ALERTS_LOG)
    assert stat.S_ISREG(st.st_mode), (
        f"{ALERTS_LOG!r} exists but is not a regular file."
    )
    # Confirm read permissions for the current user (owner/group/other).
    # Any one of these is enough for open() to work.
    user_can_read = bool(st.st_mode & stat.S_IRUSR)
    group_can_read = bool(st.st_mode & stat.S_IRGRP)
    other_can_read = bool(st.st_mode & stat.S_IROTH)
    assert user_can_read or group_can_read or other_can_read, (
        f"{ALERTS_LOG!r} is not readable by the current user."
    )

def test_alerts_log_file_contents_exact_match():
    """
    The seed alerts.log must contain exactly the 11 expected lines
    (no trailing/leading spaces, no extra blank lines).
    """
    with open(ALERTS_LOG, "r", encoding="utf-8") as fh:
        actual_lines = [line.rstrip("\n") for line in fh]

    # Helpful failure diagnostics
    assert len(actual_lines) == len(EXPECTED_LINES), (
        f"{ALERTS_LOG!r} should have {len(EXPECTED_LINES)} lines but has "
        f"{len(actual_lines)}."
    )

    mismatches = [
        (idx + 1, exp, act)
        for idx, (exp, act) in enumerate(zip(EXPECTED_LINES, actual_lines))
        if exp != act
    ]
    assert not mismatches, (
        "alerts.log content mismatch on the following lines:\n" +
        "\n".join(
            f"  Line {ln}: expected {exp!r} but found {act!r}"
            for ln, exp, act in mismatches
        )
    )