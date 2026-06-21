# test_initial_state.py
#
# This test-suite verifies that the *starting* state of the operating-system /
# file-system is exactly as described in the task specification – before the
# student’s solution is executed.  If any of these tests fail, the environment
# is not in the expected pristine state and subsequent grading steps would be
# unreliable.

import os
import pytest

HOME = "/home/user"
REMOTE_DIR = os.path.join(HOME, "remote_logs")
CENTRAL_DIR = os.path.join(HOME, "central_logs")
ANALYSIS_DIR = os.path.join(HOME, "analysis")

# --------------------------------------------------------------------------- #
# Expected, *pre-existing* content
# --------------------------------------------------------------------------- #
REMOTE_EXPECTED = {
    "app1_20230910.log": [
        "2023-09-10 08:00:01 INFO Startup complete",
        "2023-09-10 08:05:14 ERROR Failed to connect to database",
        "2023-09-10 08:07:55 INFO Retrying connection",
        "2023-09-10 08:08:02 ERROR Database connection timeout",
        "2023-09-10 08:09:10 INFO Shutdown initiated",
    ],
    "app2_20230910.log": [
        "2023-09-10 09:00:00 INFO Service started",
        "2023-09-10 09:15:22 WARN High memory usage",
        "2023-09-10 09:20:37 ERROR Out of memory",
        "2023-09-10 09:21:00 ERROR Could not allocate buffer",
        "2023-09-10 09:22:45 INFO Service restarted",
    ],
}

CENTRAL_PREEXISTING = {
    "app1_20230909.log": [
        "2023-09-09 07:59:59 INFO Previous day startup",
        "2023-09-09 08:10:10 ERROR Sample error",
        "2023-09-09 08:20:20 INFO Shutdown",
    ],
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _assert_file_lines(path, expected_lines):
    """Assert that file at *path* exists and its lines match *expected_lines*."""
    assert os.path.isfile(path), f"Expected file {path} to exist"
    with open(path, encoding="utf-8") as fh:
        actual_lines = fh.read().splitlines()
    assert (
        actual_lines == expected_lines
    ), f"Contents of {path} do not match the expected reference data."


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_directories_exist_and_absent():
    """remote_logs and central_logs must exist; analysis must NOT exist yet."""
    assert os.path.isdir(
        REMOTE_DIR
    ), f"Missing directory {REMOTE_DIR}.  The remote drop-box must be present."
    assert os.path.isdir(
        CENTRAL_DIR
    ), f"Missing directory {CENTRAL_DIR}.  The analyst archive must be present."
    assert not os.path.exists(
        ANALYSIS_DIR
    ), f"Directory {ANALYSIS_DIR} should NOT exist before the student's script runs."


@pytest.mark.parametrize("filename,lines", REMOTE_EXPECTED.items())
def test_remote_log_files_exist_with_correct_content(filename, lines):
    """Every expected *.log file must already be present in the remote share."""
    path = os.path.join(REMOTE_DIR, filename)
    _assert_file_lines(path, lines)


@pytest.mark.parametrize("filename,lines", CENTRAL_PREEXISTING.items())
def test_central_log_files_preexisting_and_correct(filename, lines):
    """Certain older log files should already be in the central archive."""
    path = os.path.join(CENTRAL_DIR, filename)
    _assert_file_lines(path, lines)


def test_central_archive_does_not_yet_contain_new_logs():
    """The new 20230910 logs must NOT be inside central_logs before the sync."""
    forbidden = [
        os.path.join(CENTRAL_DIR, "app1_20230910.log"),
        os.path.join(CENTRAL_DIR, "app2_20230910.log"),
    ]
    for path in forbidden:
        assert not os.path.exists(
            path
        ), f"{path} should NOT exist yet – student must copy it during the task."


def test_error_summary_and_analysis_directory_absent():
    """No summary report must exist prior to running the student's code."""
    summary = os.path.join(ANALYSIS_DIR, "error_summary_20230910.txt")
    assert not os.path.exists(
        summary
    ), f"Error summary {summary} should not pre-exist before the task is performed."