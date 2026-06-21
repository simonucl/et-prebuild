# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student’s solution runs.  It checks that
#
# 1. /home/user/build_logs exists.
# 2. /home/user/build_logs/agent_status.log exists and its contents exactly
#    match the specification (including the trailing newline).
# 3. /home/user/build_reports does *not* exist yet.
#
# If any of these conditions are not met, the tests will fail with
# clear, actionable messages.
#
# NOTE:  No tests are written for the expected *output* of the student’s
#        script—only the required starting conditions.

import pathlib
import pytest

# Base paths
HOME = pathlib.Path("/home/user")
BUILD_LOGS_DIR = HOME / "build_logs"
STATUS_LOG_FILE = BUILD_LOGS_DIR / "agent_status.log"
BUILD_REPORTS_DIR = HOME / "build_reports"

# The exact contents expected inside agent_status.log,
# including the single trailing newline character at the end.
EXPECTED_STATUS_LOG_CONTENT = (
    "agent_id:A01 status:OK latency_ms:94\n"
    "agent_id:A12 status:FAIL latency_ms:256\n"
    "agent_id:B03 status:OK latency_ms:101\n"
    "agent_id:C07 status:FAIL latency_ms:305\n"
    "agent_id:D99 status:OK latency_ms:87\n"
)


def test_build_logs_directory_exists():
    """
    /home/user/build_logs must exist and be a directory.
    """
    assert BUILD_LOGS_DIR.exists(), (
        f"Required directory {BUILD_LOGS_DIR} is missing. "
        "The build logs directory must exist before running the task."
    )
    assert BUILD_LOGS_DIR.is_dir(), (
        f"{BUILD_LOGS_DIR} exists but is not a directory."
    )


def test_agent_status_log_file_exists_and_is_correct():
    """
    The health file /home/user/build_logs/agent_status.log must exist
    and contain exactly the five specified lines, including the trailing newline.
    """
    assert STATUS_LOG_FILE.exists(), (
        f"Required log file {STATUS_LOG_FILE} is missing."
    )
    assert STATUS_LOG_FILE.is_file(), (
        f"{STATUS_LOG_FILE} exists but is not a file."
    )

    content = STATUS_LOG_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_STATUS_LOG_CONTENT, (
        f"The contents of {STATUS_LOG_FILE} do not match the expected "
        "initial state.\n\n"
        "EXPECTED:\n"
        f"{EXPECTED_STATUS_LOG_CONTENT!r}\n"
        "FOUND:\n"
        f"{content!r}"
    )


def test_build_reports_directory_not_present_yet():
    """
    /home/user/build_reports must *not* exist before the student's code runs.
    The student's solution is responsible for creating it.
    """
    assert not BUILD_REPORTS_DIR.exists(), (
        f"Directory {BUILD_REPORTS_DIR} should not exist yet. "
        "It must be created by the student's script."
    )