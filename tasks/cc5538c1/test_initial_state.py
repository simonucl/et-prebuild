# test_initial_state.py
#
# This test-suite validates the operating-system state *before* the student
# carries out any actions.  It asserts that the two source log files are
# present with the exact expected contents and that none of the artefacts
# the student is supposed to create already exist.

import os
import pytest

HOME = "/home/user"
LOG_DIR = os.path.join(HOME, "support", "logs")
DIAG_DIR = os.path.join(HOME, "support", "diagnostics")

APP_LOG = os.path.join(LOG_DIR, "app.log")
APP2_LOG = os.path.join(LOG_DIR, "app2.log")

EXPECTED_APP_LOG_CONTENT = (
    "[2023-07-01 10:00:01] INFO Starting service\n"
    "[2023-07-01 10:01:15] ERROR Failed to connect to database\n"
    "[2023-07-01 10:02:20] WARN Low disk space\n"
    "[2023-07-01 10:03:25] INFO Service running\n"
    "[2023-07-01 10:04:30] ERROR Timeout while reading response\n"
)

EXPECTED_APP2_LOG_CONTENT = (
    "2023-07-01T11:00:00Z INFO scheduled job start\n"
    "2023-07-01T11:00:05Z ERROR job crashed with code 1\n"
    "2023-07-01T11:00:10Z INFO scheduled job end\n"
    "2023-07-01T11:05:00Z ERROR unable to send email\n"
)


def _assert_file_exists(path: str) -> None:
    assert os.path.isfile(path), f"Required file is missing: {path}"


def _assert_not_path_exists(path: str) -> None:
    assert not os.path.exists(path), (
        f"Path {path} should NOT exist before the student runs their solution."
    )


def test_log_files_present_with_correct_content():
    """
    The two source log files must be present and match the exact expected
    content (including trailing newlines and line order).
    """
    # 1. Presence
    _assert_file_exists(APP_LOG)
    _assert_file_exists(APP2_LOG)

    # 2. Exact content check
    with open(APP_LOG, "r", encoding="utf-8") as fp:
        app_log_content = fp.read()
    with open(APP2_LOG, "r", encoding="utf-8") as fp:
        app2_log_content = fp.read()

    assert (
        app_log_content == EXPECTED_APP_LOG_CONTENT
    ), "The content of app.log does not match the expected pre-existing data."

    assert (
        app2_log_content == EXPECTED_APP2_LOG_CONTENT
    ), "The content of app2.log does not match the expected pre-existing data."

    # 3. Quick sanity checks on line counts
    assert app_log_content.count("\n") == 5, "app.log should contain exactly 5 lines."
    assert app2_log_content.count("\n") == 4, "app2.log should contain exactly 4 lines."


def test_diagnostics_directory_and_output_files_absent():
    """
    The diagnostics directory and the two output files must not exist yet.
    They will be created by the student's solution.
    """
    _assert_not_path_exists(DIAG_DIR)
    _assert_not_path_exists(os.path.join(DIAG_DIR, "errors_combined.log"))
    _assert_not_path_exists(os.path.join(DIAG_DIR, "diagnostic_report.txt"))