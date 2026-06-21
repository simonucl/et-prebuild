# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the correct initial state *before* the student performs any
# actions for the “mobile-CI error summary” task.

import pathlib
import pytest
import os

HOME = pathlib.Path("/home/user")
MOBILE_CI_DIR = HOME / "mobile_ci"
BUILD_LOG = MOBILE_CI_DIR / "build.log"

EXPECTED_BUILD_LOG_CONTENT = (
    "2023-07-11 09:14:22 INFO: Starting build for app module\n"
    "2023-07-11 09:14:24 WARN: Deprecated API usage in Gradle script\n"
    "2023-07-11 09:14:26 ERROR: Could not locate keystore file 'release.jks'\n"
    "2023-07-11 09:14:29 ERROR: Missing SDK platform 'android-30'\n"
    "2023-07-11 09:14:31 INFO: Downloading dependencies\n"
    "2023-07-11 09:14:45 ERROR: Unable to resolve dependency 'com.google.firebase:firebase-analytics'\n"
    "2023-07-11 09:14:47 ERROR: Lint found fatal errors in the release build\n"
    "2023-07-11 09:14:48 INFO: Attempting to continue despite errors\n"
    "2023-07-11 09:14:50 ERROR: Build failed due to earlier errors\n"
    "2023-07-11 09:14:52 INFO: Build process finished (took 30 sec)\n"
)

def test_mobile_ci_directory_exists():
    """
    Ensure that the /home/user/mobile_ci directory exists before the student
    starts working.  This directory must contain the existing build.log file
    that the student will process.
    """
    assert MOBILE_CI_DIR.is_dir(), (
        f"Required directory not found: {MOBILE_CI_DIR}. "
        "The mobile-CI workspace must exist before starting the task."
    )

def test_build_log_exists_with_expected_content():
    """
    Validate that /home/user/mobile_ci/build.log exists and its exact content
    matches the reference log provided in the task description.  A mismatch
    indicates that the environment is not in the expected initial state.
    """
    assert BUILD_LOG.is_file(), (
        f"Required log file not found: {BUILD_LOG}. "
        "The student cannot proceed without the original build.log."
    )

    actual_content = BUILD_LOG.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_BUILD_LOG_CONTENT, (
        "The content of /home/user/mobile_ci/build.log does not match the "
        "expected initial log.  Make sure the file is unmodified and contains "
        "exactly the lines specified in the task description, including all "
        "newlines."
    )