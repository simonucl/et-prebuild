# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating
# system / filesystem **before** the student performs any actions for
# the “process-inventory snapshot” task.  The checks make sure that the
# workspace the student is supposed to create does **not** already
# exist and that no pre-existing result file can interfere with the
# grading logic.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
COMPLIANCE_DIR = HOME / "compliance"
AUDIT_FILE = COMPLIANCE_DIR / "process_audit.csv"


def _assert_absent(path: Path):
    """
    Helper that asserts a given path (file, dir, symlink, etc.)
    does not exist in the filesystem.
    """
    assert not path.exists(), (
        f"Pre-check failed: '{path}' already exists. "
        "The student is expected to create this path as part of the task, "
        "so it must be absent before they start."
    )


def test_compliance_directory_absent():
    """
    The directory /home/user/compliance must NOT exist yet.
    """
    _assert_absent(COMPLIANCE_DIR)


def test_process_audit_csv_absent():
    """
    The file /home/user/compliance/process_audit.csv must NOT exist yet.
    """
    # If the directory does not exist we have already passed, but still
    # explicitly check the file path to give a clear failure message
    # should only the file pre-exist.
    _assert_absent(AUDIT_FILE)