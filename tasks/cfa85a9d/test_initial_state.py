# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system state
# before the student performs any actions.
#
# It checks that:
#   1. The directory /home/user/logs exists.
#   2. The file   /home/user/logs/webapp.log exists and is a regular file.
#   3. The file contains exactly seven occurrences of the case-sensitive
#      string "PAYMENT_FAILURE".
#
# NOTE:  We deliberately do **not** look for any output files or directories
#        the student is expected to create (e.g. anything under
#        /home/user/diagnostics) in order to comply with the grading rubric.

import os
from pathlib import Path

import pytest

LOGS_DIR = Path("/home/user/logs")
WEBAPP_LOG = LOGS_DIR / "webapp.log"
EXPECTED_FAILURE_COUNT = 7
SEARCH_STRING = "PAYMENT_FAILURE"


def test_logs_directory_exists():
    """Ensure /home/user/logs exists and is a directory."""
    assert LOGS_DIR.exists(), f"Required directory not found: {LOGS_DIR}"
    assert LOGS_DIR.is_dir(), f"Expected {LOGS_DIR} to be a directory."


def test_webapp_log_exists_and_is_file():
    """Ensure /home/user/logs/webapp.log exists and is a regular file."""
    assert WEBAPP_LOG.exists(), f"Required log file not found: {WEBAPP_LOG}"
    assert WEBAPP_LOG.is_file(), f"Expected {WEBAPP_LOG} to be a regular file."


def test_webapp_log_contains_expected_failure_count():
    """
    Confirm that the log contains exactly seven occurrences of
    the string 'PAYMENT_FAILURE'.
    """
    # Reading the entire file is fine for small diagnostic logs.
    try:
        content = WEBAPP_LOG.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"Could not read {WEBAPP_LOG} as UTF-8: {exc}")

    actual_count = content.count(SEARCH_STRING)
    assert (
        actual_count == EXPECTED_FAILURE_COUNT
    ), (
        f"Expected {EXPECTED_FAILURE_COUNT} occurrences of '{SEARCH_STRING}' "
        f"in {WEBAPP_LOG}, but found {actual_count}."
    )