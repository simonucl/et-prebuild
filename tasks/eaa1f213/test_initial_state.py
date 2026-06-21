# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem state
BEFORE the student starts working on the “Sort & uniq frequency counting for
QA test results” exercise.

Truth table for this kata
-------------------------
1. /home/user/qa_env/                     -> MUST exist (dir)
2. /home/user/qa_env/test_results/        -> MUST exist (dir)
3. /home/user/qa_env/test_results/raw_results.txt
                                          -> MUST exist (file) *with exact seed
                                             data shown in the task*
4. /home/user/qa_env/logs                 -> MUST *NOT* exist yet
5. /home/user/qa_env/test_results/summary.log
                                          -> MUST *NOT* exist yet
"""

import os
from pathlib import Path

import pytest

# Absolute paths used throughout the tests
HOME = Path("/home/user")
QA_ENV = HOME / "qa_env"
TEST_RESULTS_DIR = QA_ENV / "test_results"
RAW_RESULTS = TEST_RESULTS_DIR / "raw_results.txt"
LOGS_DIR = QA_ENV / "logs"
SUMMARY_LOG = TEST_RESULTS_DIR / "summary.log"

# The canonical contents of raw_results.txt, taken verbatim from the spec
EXPECTED_RAW_CONTENT = [
    "auth PASS",
    "auth PASS",
    "auth FAIL",
    "payment PASS",
    "payment PASS",
    "payment PASS",
    "payment FAIL",
    "search PASS",
    "search FAIL",
    "search FAIL",
    "search FAIL",
    "report PASS",
    "report PASS",
    "report PASS",
    "report PASS",
]


def test_qa_env_directory_present():
    """The top-level /home/user/qa_env directory must already exist."""
    assert QA_ENV.is_dir(), (
        f"Expected directory {QA_ENV} to exist, "
        "but it is missing. The starter repository is corrupted."
    )


def test_test_results_directory_present():
    """Sub-directory /home/user/qa_env/test_results must already exist."""
    assert TEST_RESULTS_DIR.is_dir(), (
        f"Expected directory {TEST_RESULTS_DIR} to exist, "
        "but it is missing. The starter repository is corrupted."
    )


def test_raw_results_file_exists_and_content_is_correct():
    """
    1. raw_results.txt must exist.
    2. It must be a regular file.
    3. Its exact trimmed line content must match the canonical list.
    """
    assert RAW_RESULTS.exists(), (
        f"Required seed file {RAW_RESULTS} is missing."
    )
    assert RAW_RESULTS.is_file(), (
        f"{RAW_RESULTS} exists but is not a regular file."
    )

    with RAW_RESULTS.open(encoding="utf-8") as fh:
        # Strip the trailing newline characters but keep internal whitespace
        content = [line.rstrip("\n") for line in fh]

    assert content == EXPECTED_RAW_CONTENT, (
        "The contents of raw_results.txt do not match the canonical starter "
        "data. Ensure the file has not been modified.\n"
        f"Expected ({len(EXPECTED_RAW_CONTENT)} lines):\n"
        f"{EXPECTED_RAW_CONTENT}\n\n"
        f"Found ({len(content)} lines):\n"
        f"{content}"
    )


def test_logs_directory_must_not_exist_initially():
    """
    The 'logs' directory is to be created by the student; therefore it must
    NOT exist in the initial state.
    """
    assert not LOGS_DIR.exists(), (
        f"Directory {LOGS_DIR} already exists, but it should be absent before "
        "the student begins. Remove it from the starter files."
    )


def test_summary_log_must_not_exist_initially():
    """
    summary.log is produced by the student. It must not be present to avoid
    false positives.
    """
    assert not SUMMARY_LOG.exists(), (
        f"File {SUMMARY_LOG} already exists, but it should be absent before "
        "the student begins. Remove it from the starter files."
    )