# test_initial_state.py
#
# This pytest suite validates the *initial* state of the system **before**
# the student performs any action for the “network exposure snapshot” task.
#
# Requirements at this stage:
# 1. The directory /home/user/audit must NOT exist.
# 2. Consequently, the file /home/user/audit/netcheck.log must NOT exist.
#
# Rationale:
# The student is expected to create both the directory and the log file
# during the assignment.  Their pre-existence would indicate that the
# environment has been modified ahead of time and could invalidate the
# assessment.

import os
import stat
import pytest
from pathlib import Path

AUDIT_DIR = Path("/home/user/audit")
LOG_FILE = AUDIT_DIR / "netcheck.log"


def test_audit_directory_absence():
    """
    The /home/user/audit directory should NOT exist prior to the student's work.
    """
    assert not AUDIT_DIR.exists(), (
        f"Precondition failed: {AUDIT_DIR} already exists. "
        "The directory must be created by the student as part of the task."
    )


def test_logfile_absence():
    """
    The target log file should definitely not exist before the task starts.
    If the directory exists for some reason, we still ensure the file is absent.
    """
    assert not LOG_FILE.exists(), (
        f"Precondition failed: {LOG_FILE} already exists. "
        "The student must generate this file during the task."
    )


def test_no_leftover_parents():
    """
    If any parent directories of /home/user/audit exist, ensure they do not
    already contain improperly placed artifacts that could interfere with the test.
    """
    if AUDIT_DIR.exists():
        # Directory exists unexpectedly; ensure it is empty to prevent cheating.
        contents = list(AUDIT_DIR.iterdir())
        assert not contents, (
            f"Precondition failed: unexpected files/directories already present in {AUDIT_DIR}: "
            f"{', '.join(str(p) for p in contents)}"
        )