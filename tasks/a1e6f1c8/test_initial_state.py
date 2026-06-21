# test_initial_state.py
#
# This test-suite validates that the operating system / filesystem is
# in its expected *initial* state **before** the learner generates the
# Maven upload-status summary.
#
# What we assert:
# 1. The raw build log exists at the exact absolute path and contains
#    the expected five lines in the correct order.
# 2. The reports directory already exists and is writable.
# 3. The summary file that the learner is supposed to create does *not*
#    yet exist.  (If it already exists, the environment is not clean.)
#
# No third-party dependencies are used—only the Python standard library
# and `pytest`.

import os
import stat
import pytest

# Absolute paths used throughout the exercise
LOG_PATH = "/home/user/builds/logs/build_2023-08-15.log"
REPORTS_DIR = "/home/user/builds/reports"
SUMMARY_PATH = "/home/user/builds/reports/2023-08-15_summary.txt"

EXPECTED_LOG_LINES = [
    "[INFO] Uploaded: commons-io-2.11.0.jar",
    "[INFO] Uploaded: guava-32.1.0.jar",
    "[ERROR] FAILED to upload: junit-4.13.2.jar",
    "[ERROR] FAILED to upload: log4j-1.2.17.jar",
    "[INFO] Uploaded: slf4j-api-1.7.36.jar",
]


def test_build_log_exists_with_correct_contents():
    """The raw build log must exist and contain the exact expected lines."""
    assert os.path.isfile(LOG_PATH), (
        f"Expected log file does not exist at:\n  {LOG_PATH}"
    )

    with open(LOG_PATH, "r", encoding="utf-8") as fh:
        lines = [line.rstrip("\n") for line in fh.readlines()]

    assert lines == EXPECTED_LOG_LINES, (
        "Log file contents are not as expected.\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_LOG_LINES)
        + "\n\nActual lines:\n"
        + "\n".join(lines)
    )


def test_reports_directory_exists_and_is_writable():
    """The reports directory must pre-exist and allow write access."""
    assert os.path.isdir(REPORTS_DIR), (
        f"Reports directory is missing at:\n  {REPORTS_DIR}"
    )

    # Check that the current user has write permission.
    # This is done by inspecting the directory's mode bits.
    dir_stat = os.stat(REPORTS_DIR)
    is_writable = bool(dir_stat.st_mode & stat.S_IWUSR)
    assert is_writable, (
        f"Reports directory is not writable at:\n  {REPORTS_DIR}"
    )


def test_summary_file_not_present_yet():
    """The summary file should NOT exist before the learner runs their command."""
    assert not os.path.exists(SUMMARY_PATH), (
        "The summary file already exists:\n"
        f"  {SUMMARY_PATH}\n"
        "The environment should start without this file so the learner "
        "can create it."
    )