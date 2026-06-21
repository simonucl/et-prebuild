# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state before the student performs any work on the “backup-operations”
# exercise.  These checks guarantee that the starting situation is exactly
# what the subsequent, action-oriented tests (run after the student’s
# commands) expect.
#
# Only the Python standard library and pytest are used, per specification.

import os
from pathlib import Path

import pytest

# Constants for absolute paths used throughout the exercise
HOME_DIR = Path("/home/user")
DATA_DIR = HOME_DIR / "data"
REQ_FILE = DATA_DIR / "backup_requirements.txt"
BACKUP_ENV_DIR = HOME_DIR / "backup_env"
BACKUP_REPORT_DIR = HOME_DIR / "backup_report"


###############################################################################
# Helper functions
###############################################################################

EXPECTED_REQUIREMENTS_LINES = [
    "certifi==2023.7.22",
    "charset-normalizer==3.3.2",
    "idna==3.4",
    "urllib3==2.0.7",
    "requests==2.31.0",
]

def _read_requirements_file() -> bytes:
    """
    Read the entire requirements file as raw bytes.
    A separate helper makes unit tests easier to follow.
    """
    return REQ_FILE.read_bytes()


###############################################################################
# Tests
###############################################################################

def test_requirements_file_exists():
    """The backup_requirements.txt file must be present at the exact location."""
    assert REQ_FILE.exists(), (
        f"Required file {REQ_FILE} does not exist. "
        "The exercise must start with this file already on disk."
    )
    assert REQ_FILE.is_file(), (
        f"{REQ_FILE} exists but is not a regular file."
    )


def test_requirements_file_content_and_format():
    """
    The requirements file must contain exactly five lines, in the specified
    order, each ending with LF, and with *no* CR characters.  The file must
    also end with a single trailing LF (no extra blank lines).
    """
    raw = _read_requirements_file()

    # a) Ensure the file ends with a single LF
    assert raw.endswith(b"\n"), (
        f"{REQ_FILE} must end with a single newline character (LF)."
    )

    # b) Reject CRLF or stray CR characters
    assert b"\r" not in raw, (
        f"{REQ_FILE} must use Unix line endings (LF only), "
        "but carriage-return characters (CR) were found."
    )

    # c) Split lines (rstrip only final LF to avoid empty last element)
    lines = raw.decode("utf-8").rstrip("\n").split("\n")

    # d) Verify exact content and order
    assert lines == EXPECTED_REQUIREMENTS_LINES, (
        f"{REQ_FILE} has unexpected content.\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_REQUIREMENTS_LINES)
    )


def test_virtualenv_not_yet_created():
    """
    No virtual environment should exist at /home/user/backup_env prior to the
    student's actions.
    """
    assert not BACKUP_ENV_DIR.exists(), (
        f"Directory {BACKUP_ENV_DIR} should *not* exist before the task begins. "
        "The student will create the virtual environment there."
    )


def test_backup_report_directory_absent():
    """
    There must be no /home/user/backup_report directory at the outset.
    """
    assert not BACKUP_REPORT_DIR.exists(), (
        f"Directory {BACKUP_REPORT_DIR} should not exist yet. "
        "It will be created by the student's commands."
    )