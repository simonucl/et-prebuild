# test_initial_state.py
"""
Pytest suite that validates the **initial** state of the operating system / filesystem
_before_ the student starts working on the “credential-rotation” exercise.

These tests make sure that the student begins from a completely clean slate so that
the subsequent grading (which checks for the **presence** of the virtual environment,
uninstalled “wheel” package, and audit log) can run without interference.

All paths are absolute and rooted at /home/user as required.
Only the Python standard library and pytest are used.
"""

import os
import pytest
from pathlib import Path

# --- Constants for the exercise ---------------------------------------------

VENV_DIR = Path("/home/user/cred_rotate_env")
ROTATION_LOGS_DIR = VENV_DIR / "rotation_logs"
FREEZE_LOG = ROTATION_LOGS_DIR / "after_uninstall_freeze.txt"


# --- Tests -------------------------------------------------------------------

def test_virtualenv_directory_absent():
    """
    The virtual environment directory must NOT exist yet.
    This guarantees the student really creates it during the assignment.
    """
    assert not VENV_DIR.exists(), (
        f"The directory {VENV_DIR} already exists. "
        "Start from a clean state with no residual virtual environments."
    )


def test_activate_script_absent():
    """
    The activate script inside the would-be venv must NOT exist.
    """
    activate_script = VENV_DIR / "bin" / "activate"
    assert not activate_script.exists(), (
        f"Found unexpected activate script at {activate_script}. "
        "A fresh virtual environment has not yet been created."
    )


def test_rotation_logs_directory_absent():
    """
    The rotation_logs directory must NOT be present before the exercise begins.
    """
    assert not ROTATION_LOGS_DIR.exists(), (
        f"Unexpected directory {ROTATION_LOGS_DIR} found. "
        "The student should create it only after setting up the venv."
    )


def test_freeze_log_absent():
    """
    The audit snapshot file must NOT exist at the beginning.
    """
    assert not FREEZE_LOG.exists(), (
        f"Unexpected log file {FREEZE_LOG} found. "
        "The student must generate this file as part of the task."
    )