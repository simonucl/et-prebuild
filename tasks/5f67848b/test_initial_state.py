# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student’s solution runs.  It confirms that the Gradle build log is in
# place and that no output artefacts have been generated yet.
#
# Requirements verified:
#   • /home/user/build_logs exists, is a directory and is writable.
#   • /home/user/build_logs/gradle_build.log exists and contains the exact,
#     canonical content expected by subsequent tooling.
#   • /home/user/build_logs/failed_tasks.csv does NOT yet exist.
#
# Any deviation from these expectations will raise a descriptive assertion
# error, guiding the student to fix the environment before proceeding.

import os
import stat
import pytest

BUILD_LOG_DIR = "/home/user/build_logs"
BUILD_LOG_FILE = os.path.join(BUILD_LOG_DIR, "gradle_build.log")
CSV_FILE = os.path.join(BUILD_LOG_DIR, "failed_tasks.csv")

EXPECTED_LOG_LINES = [
    "Task :app:compileDebugJava FAILED",
    "Task :app:compileDebugResources",
    "Task :lib:compileDebugKotlin FAILED",
    "Task :lib:processDebugResources",
    "Task :network:compileReleaseJava",
    "Task :app:assembleDebug FAILED",
    "BUILD FAILED in 1m 46s",
    "7 actionable tasks: 7 executed",
]


def test_build_logs_directory_exists_and_writable():
    assert os.path.exists(
        BUILD_LOG_DIR
    ), f"Directory expected at {BUILD_LOG_DIR} but was not found."
    assert os.path.isdir(
        BUILD_LOG_DIR
    ), f"Expected {BUILD_LOG_DIR} to be a directory, but it is not."
    # Check for write permission
    can_write = os.access(BUILD_LOG_DIR, os.W_OK)
    assert can_write, (
        f"The directory {BUILD_LOG_DIR} is not writable by the current user. "
        "Downstream tooling must be able to create / overwrite artefacts here."
    )


def test_gradle_build_log_exists_with_correct_content():
    assert os.path.exists(
        BUILD_LOG_FILE
    ), f"Gradle build log expected at {BUILD_LOG_FILE} but was not found."

    assert os.path.isfile(
        BUILD_LOG_FILE
    ), f"Expected {BUILD_LOG_FILE} to be a regular file, but it is not."

    # Read file with UTF-8 encoding; it must parse without errors.
    with open(BUILD_LOG_FILE, "r", encoding="utf-8") as fh:
        raw_content = fh.read()

    # Strip a single trailing newline for comparison, but preserve internal LFs.
    if raw_content.endswith("\n"):
        raw_content = raw_content[:-1]

    lines = raw_content.split("\n")
    assert (
        lines == EXPECTED_LOG_LINES
    ), (
        f"The contents of {BUILD_LOG_FILE} do not match the expected pre-populated "
        "Gradle build log.\n\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_LOG_LINES)
        + "\n\nActual lines:\n"
        + "\n".join(lines)
    )


def test_failed_tasks_csv_does_not_exist_yet():
    assert not os.path.exists(
        CSV_FILE
    ), (
        f"The file {CSV_FILE} already exists, but it should only be created by the "
        "student's solution. Remove it before running the task."
    )