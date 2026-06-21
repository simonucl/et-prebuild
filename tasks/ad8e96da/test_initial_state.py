# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the operating system /
filesystem before the learner begins the “compliance_project” task.

The expectations are that **nothing has been created yet**—no project
directory, no virtual-environment, no requirements file, and no audit trail.

If any of those artefacts already exist, the test suite will fail with a
clear, actionable message.
"""

import os
from pathlib import Path

# Absolute paths that must NOT yet exist
BASE_DIR = Path("/home/user/compliance_project")
VENV_DIR = BASE_DIR / "env"
REQ_FILE = BASE_DIR / "requirements.txt"
AUDIT_FILE = BASE_DIR / "audit_trail.csv"


def _assert_absent(path: Path):
    """
    Helper that asserts the given path does not exist and produces a
    descriptive failure message if it does.
    """
    assert not path.exists(), (
        f"\n[Initial‐State Error]\n"
        f"The path '{path}' already exists, but it should NOT be present at "
        f"the start of the assignment. Please begin with a clean slate.  "
        f"Delete or move this path before proceeding."
    )


def test_base_directory_absent():
    """Project root directory must not exist yet."""
    _assert_absent(BASE_DIR)


def test_virtualenv_directory_absent():
    """Virtual-environment directory must not exist yet."""
    _assert_absent(VENV_DIR)


def test_requirements_file_absent():
    """requirements.txt must not exist yet."""
    _assert_absent(REQ_FILE)


def test_audit_trail_file_absent():
    """audit_trail.csv must not exist yet."""
    _assert_absent(AUDIT_FILE)