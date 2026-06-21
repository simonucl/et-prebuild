# test_initial_state.py
"""
Pytest suite to verify the **initial** state of the operating system / filesystem
*before* the student carries out the provisioning-log task.

According to the assignment requirements, the student will eventually create:

    /home/user/provisioning/logs/initial_diagnostics.log     (file)
    /home/user/provisioning/logs                             (directory)

with very specific contents and permission modes.

These tests therefore assert that none of those artefacts exist yet.
If they already exist, the environment is not in the expected clean state and
the student would be starting from an incorrect baseline.
"""

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
PROVISIONING_DIR = HOME / "provisioning"
LOGS_DIR = PROVISIONING_DIR / "logs"
LOG_FILE = LOGS_DIR / "initial_diagnostics.log"


def _perm_str(mode: int) -> str:
    """Return a symbolic rwx string (e.g. '755') for human-readable error output."""
    return oct(mode & 0o777)[2:]


@pytest.fixture(scope="module")
def path_existence_snapshot():
    """
    Gather a snapshot of whether the key paths exist **before** the student runs
    their solution.  This is consumed by multiple tests so the filesystem is
    only touched once.
    """
    return {
        "provisioning_exists": PROVISIONING_DIR.exists(),
        "logs_exists": LOGS_DIR.exists(),
        "log_file_exists": LOG_FILE.exists(),
    }


def test_logs_directory_absent(path_existence_snapshot):
    assert not path_existence_snapshot["logs_exists"], (
        f"The directory {LOGS_DIR} already exists, "
        "but the student is expected to create it. "
        "Remove the directory (or run tests in a fresh environment) "
        "so the student starts from a clean slate."
    )


def test_log_file_absent(path_existence_snapshot):
    assert not path_existence_snapshot["log_file_exists"], (
        f"The file {LOG_FILE} already exists, "
        "but the student is required to create it with specific contents. "
        "Delete the file (or run tests in a fresh environment) "
        "before handing the task to the student."
    )


def test_provisioning_directory_state(path_existence_snapshot):
    """
    If /home/user/provisioning already exists for some unrelated reason,
    ensure it does NOT already have unexpected contents that might interfere
    with the upcoming exercise (e.g., a stray 'logs' folder or other files).
    """
    if path_existence_snapshot["provisioning_exists"]:
        # Provisioning directory is present.  Ensure it is *empty*.
        unexpected_entries = [
            p for p in PROVISIONING_DIR.iterdir() if p.name != "__pycache__"
        ]
        assert not unexpected_entries, (
            f"The directory {PROVISIONING_DIR} should be empty at the start of the "
            "exercise, but found: "
            + ", ".join(str(p) for p in unexpected_entries)
        )


def test_no_leftover_permission_modes():
    """
    If, despite being absent, someone pre-created the directories/files with
    incorrect permissions and later deleted them, we still want to ensure
    that nothing with those exact paths exists with wrong modes (a safety net).
    """
    for path in (LOGS_DIR, LOG_FILE):
        assert not path.exists(), (
            f"Unexpected leftover path detected: {path}. "
            "Please start the exercise in a clean environment."
        )