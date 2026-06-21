# test_initial_state.py
#
# Pytest suite to verify the initial on-disk state before the learner begins
# working on the CI-summary task.  These tests assert the presence (or absence)
# of specific files/directories and the exact contents of the raw CI log.

import os
import pytest

HOME = "/home/user"
LOG_DIR = os.path.join(HOME, "build", "logs")
LOG_FILE = os.path.join(LOG_DIR, "mobile_ci_2023-10-07.log")
REPORTS_DIR = os.path.join(HOME, "build", "reports")
SUMMARY_FILE = os.path.join(REPORTS_DIR, "ci_summary.txt")


@pytest.fixture(scope="module")
def log_contents():
    """Read and return the CI log file contents as a list of lines (stripped)."""
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def test_log_directory_exists():
    assert os.path.isdir(LOG_DIR), (
        f"Expected directory {LOG_DIR} to exist, but it is missing."
    )


def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), (
        f"Expected log file {LOG_FILE} to exist, but it is missing."
    )


def test_reports_directory_absent():
    # The reports directory should not exist yet; it will be created by the task.
    assert not os.path.exists(REPORTS_DIR), (
        f"Directory {REPORTS_DIR} should not exist before the task starts."
    )


def test_summary_file_absent():
    # The summary file must not exist at the outset.
    assert not os.path.exists(SUMMARY_FILE), (
        f"File {SUMMARY_FILE} should not exist before the task starts."
    )


def test_log_file_line_count(log_contents):
    assert len(log_contents) == 8, (
        f"Log file is expected to have 8 lines, but has {len(log_contents)}."
    )


def test_log_file_exact_contents(log_contents):
    expected_lines = [
        "[00:01:12] MODULE=app_core PLATFORM=android RESULT=SUCCESS DURATION=120",
        "[00:03:15] MODULE=app_ui PLATFORM=android RESULT=WARNING DURATION=60",
        "[00:04:55] MODULE=networking PLATFORM=ios RESULT=FAILURE DURATION=45",
        "[00:06:01] MODULE=database PLATFORM=android RESULT=SUCCESS DURATION=75",
        "[00:07:40] MODULE=push_service PLATFORM=ios RESULT=FAILURE DURATION=30",
        "[00:08:25] MODULE=analytics PLATFORM=android RESULT=SUCCESS DURATION=90",
        "[00:10:55] MODULE=billing PLATFORM=ios RESULT=SUCCESS DURATION=110",
        "[00:12:05] MODULE=crash_reporter PLATFORM=android RESULT=WARNING DURATION=55",
    ]
    assert log_contents == expected_lines, (
        "The contents of the CI log file do not match the expected initial state."
    )