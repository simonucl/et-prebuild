# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem starts
# in the correct **initial** condition *before* the student’s solution is run.
#
# What we assert:
# 1. The directory /home/user/test_env exists.
# 2. The file   /home/user/test_env/qa_cases.log exists and contains the
#    expected 10 lines (in the exact order shown in the task description).
# 3. The file   /home/user/test_env/freq_report.txt must NOT exist yet.
#
# Any failure message should make it clear what is missing or out of place.
#
# NOTE: We do *not* test for any output artefacts that should be created
#       by the student (except that we assert they do **not** exist yet).

from pathlib import Path
import pytest

# Absolute paths used throughout the assertions
BASE_DIR = Path("/home/user/test_env")
QA_LOG   = BASE_DIR / "qa_cases.log"
FREQ_REPORT = BASE_DIR / "freq_report.txt"

# The exact contents that must already be in qa_cases.log
EXPECTED_QA_LOG_LINES = [
    "SEC_Login",
    "SEC_Login",
    "SEC_Logout",
    "UI_Homepage_Load",
    "UI_Homepage_Load",
    "UI_Homepage_Load",
    "API_GetUser",
    "API_GetUser",
    "API_GetUser",
    "API_GetUser",
]

def test_directory_exists():
    """Ensure the /home/user/test_env directory is present."""
    assert BASE_DIR.is_dir(), (
        f"Required directory missing: {BASE_DIR}. "
        "Create the directory before proceeding."
    )

def test_qa_cases_file_exists():
    """Ensure qa_cases.log exists as a regular file."""
    assert QA_LOG.is_file(), (
        f"Required file missing: {QA_LOG}. "
        "It must be present before generating the frequency report."
    )

def test_qa_cases_file_contents():
    """
    Verify that qa_cases.log contains exactly the 10 expected lines
    and nothing else.
    """
    with QA_LOG.open("r", encoding="utf-8") as fh:
        # .splitlines() removes the trailing newline (if any) and
        # returns a list of lines without line-ending characters.
        actual_lines = fh.read().splitlines()

    assert actual_lines == EXPECTED_QA_LOG_LINES, (
        "The contents of qa_cases.log do not match the expected initial "
        "state.\n\n"
        f"Expected ({len(EXPECTED_QA_LOG_LINES)} lines):\n"
        + "\n".join(EXPECTED_QA_LOG_LINES)
        + "\n\n"
        f"Actual ({len(actual_lines)} lines):\n"
        + "\n".join(actual_lines)
    )

def test_freq_report_not_present_yet():
    """freq_report.txt should NOT exist before the student runs their command."""
    assert not FREQ_REPORT.exists(), (
        f"Output file already exists: {FREQ_REPORT}. "
        "The initial state should not include this file."
    )