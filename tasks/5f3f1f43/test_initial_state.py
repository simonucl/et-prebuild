# test_initial_state.py
"""
Pytest suite to validate the filesystem *before* the student performs the
backup → delete → restore drill.

What is tested (and why):
1. The source directory /home/user/data_project must already exist.
2. The two required files must be present inside that directory.
3. Each file must contain the exact expected content.

We explicitly do *not* test for any backup archives, log files, or output
directories, because those should not exist yet.
"""

from pathlib import Path
import pytest

# --- Constants describing the expected initial state -----------------------
DATA_DIR = Path("/home/user/data_project")
IMPORTANT_FILE = DATA_DIR / "important.txt"
NOTES_FILE = DATA_DIR / "notes.md"

EXPECTED_IMPORTANT_CONTENT = "ALPHA BACKUP DATA\n"
EXPECTED_NOTES_CONTENT = "Original notes for the backup-restore test.\n"


# --- Tests -----------------------------------------------------------------
def test_data_directory_exists():
    """
    The main data directory must already be present.
    """
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} is missing.\n"
        "Make sure the initial dataset is in place before starting the task."
    )


def test_important_file_present_and_correct():
    """
    important.txt must exist and have exactly the expected one-line content.
    """
    assert IMPORTANT_FILE.is_file(), (
        f"Required file {IMPORTANT_FILE} is missing inside {DATA_DIR}."
    )

    actual = IMPORTANT_FILE.read_text(encoding="utf-8")
    assert actual == EXPECTED_IMPORTANT_CONTENT, (
        f"Content of {IMPORTANT_FILE} does not match expected value.\n"
        f"Expected: {repr(EXPECTED_IMPORTANT_CONTENT)}\n"
        f"Found   : {repr(actual)}"
    )


def test_notes_file_present_and_correct():
    """
    notes.md must exist and have the expected sentence.
    """
    assert NOTES_FILE.is_file(), (
        f"Required file {NOTES_FILE} is missing inside {DATA_DIR}."
    )

    actual = NOTES_FILE.read_text(encoding="utf-8")
    assert actual == EXPECTED_NOTES_CONTENT, (
        f"Content of {NOTES_FILE} does not match expected value.\n"
        f"Expected: {repr(EXPECTED_NOTES_CONTENT)}\n"
        f"Found   : {repr(actual)}"
    )