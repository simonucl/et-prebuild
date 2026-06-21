# test_initial_state.py
#
# Pytest suite that verifies the initial operating-system / filesystem
# state *before* the student begins the “capacity-planner” task.
#
# These tests intentionally assert that none of the artefacts the
# student is supposed to create already exist.  If any of them are
# found, the environment is in an unexpected state and the exercise
# cannot start from a clean slate.

import os
from pathlib import Path

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"

PRIVATE_KEY = SSH_DIR / "capacity_planner"
PUBLIC_KEY = SSH_DIR / "capacity_planner.pub"
REPORT_FILE = HOME / "capacity_planner_report.log"


def _describe(path: Path) -> str:
    """
    Return a human-readable description of the full path, used
    in assertion-failure messages to make debugging easier.
    """
    return f"‘{path}’ (full path: {path.resolve()})"


def test_private_key_does_not_exist():
    """
    The private key must NOT exist before the student generates it.
    """
    assert not PRIVATE_KEY.exists(), (
        f"The private key {_describe(PRIVATE_KEY)} already exists.  "
        "The environment is not clean — remove it before starting the task."
    )


def test_public_key_does_not_exist():
    """
    The public key must NOT exist before the student generates it.
    """
    assert not PUBLIC_KEY.exists(), (
        f"The public key {_describe(PUBLIC_KEY)} already exists.  "
        "The environment is not clean — remove it before starting the task."
    )


def test_report_file_does_not_exist():
    """
    The capacity-planner report must NOT exist before the student creates it.
    """
    assert not REPORT_FILE.exists(), (
        f"The report file {_describe(REPORT_FILE)} already exists.  "
        "The environment is not clean — remove it before starting the task."
    )