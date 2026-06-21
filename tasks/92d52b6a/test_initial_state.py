# test_initial_state.py
#
# This test-suite asserts the machine’s *initial* filesystem state
# before the student starts working on the task.  It deliberately
# checks ONLY those artefacts that must already exist (or must **not**
# yet exist) according to the specification.  If any of these tests
# fail, the student’s starting point is incorrect and the exercise
# cannot be reliably graded.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "security" / "logs"
LOG_FILE = LOG_DIR / "2024-credential-rotation.log"

ANALYSIS_DIR = HOME / "security" / "analysis"

CRITICAL_FILE = ANALYSIS_DIR / "critical_rotation_events.log"
SVC_FILE = ANALYSIS_DIR / "svc_account_hits.log"
SUMMARY_FILE = ANALYSIS_DIR / "rotation_summary.txt"

# --------------------------------------------------------------------------- #
# Expected content of the pre-existing raw log (20 lines, LF line endings)
# --------------------------------------------------------------------------- #
EXPECTED_LOG_LINES = [
    "2024-06-11T14:22:01Z [INFO] Service 'api-gateway' credential rotation successful\n",
    "2024-06-11T14:25:47Z [WARNING] Service 'auth-service' credential expired, rotation required\n",
    "2024-06-11T14:26:02Z [ERROR] Service 'auth-service' credential expired, failed automatic rotation\n",
    "2024-06-11T14:30:12Z [INFO] User 'alice' authenticated to 'git-server'\n",
    "2024-06-11T14:35:55Z [INFO] Service 'db-backend' credential rotation scheduled\n",
    "2024-06-11T14:36:07Z [ERROR] Service 'db-backend' credential expired, rotation halted\n",
    "2024-06-11T14:40:11Z [WARNING] Service 'billing-service' credential expired, awaiting rotation\n",
    "2024-06-11T14:45:23Z [INFO] Service 'message-queue' credential rotation successful\n",
    "2024-06-11T14:47:58Z [ERROR] Service 'message-queue' credential expired, failed automatic rotation\n",
    "2024-06-11T14:48:12Z [INFO] User 'svc_analytics' obtained temporary token\n",
    "2024-06-11T14:49:42Z [INFO] User 'svc_billing' token refresh completed\n",
    "2024-06-11T14:50:21Z [WARNING] User 'svc_marketing' failed token refresh attempt\n",
    "2024-06-11T14:52:07Z [INFO] Background job 'rotate-keys' finished\n",
    "2024-06-11T14:53:17Z [INFO] Service 'search-service' credential rotation successful\n",
    "2024-06-11T14:54:20Z [WARNING] Service 'search-service' credential expired, rotation required\n",
    "2024-06-11T14:55:09Z [INFO] User 'bob' logged out\n",
    "2024-06-11T14:56:30Z [INFO] User 'svc_billing' credential renewed\n",
    "2024-06-11T14:57:41Z [ERROR] Service 'auth-service' credential expired, rotation attempt failed again\n",
    "2024-06-11T15:01:26Z [INFO] CRON 'cleanup-temp' completed\n",
    "2024-06-11T15:02:57Z [INFO] User 'svc_reporting' authenticated\n",
]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_logs_directory_exists():
    assert LOG_DIR.is_dir(), (
        f"Required directory missing: {LOG_DIR}. "
        "The exercise expects the raw logs to be under this path."
    )


def test_log_file_exists():
    assert LOG_FILE.is_file(), (
        f"Required log file missing: {LOG_FILE}. "
        "It should already be present *before* the student starts."
    )


def test_log_file_content_exact():
    """Verify that the raw log file has exactly the expected 20 lines."""
    with LOG_FILE.open("r", encoding="utf-8", newline="\n") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == EXPECTED_LOG_LINES, (
        "The content of the raw log file differs from what the exercise specifies.\n"
        f"Expected {len(EXPECTED_LOG_LINES)} lines but found {len(actual_lines)}.\n"
        "The automated grader relies on the exact byte-for-byte content."
    )


@pytest.mark.parametrize(
    "path",
    [ANALYSIS_DIR, CRITICAL_FILE, SVC_FILE, SUMMARY_FILE],
)
def test_analysis_artifacts_do_not_exist_yet(path: Path):
    """
    None of the analysis artefacts should exist *before* the student runs
    their solution.  If any of them are found, it means the environment is
    polluted or the student has already performed some steps.
    """
    assert not path.exists(), (
        f"Unexpected pre-existing artefact: {path}. "
        "The analysis directory and files must be created by the student’s script, "
        "so they should not be present at the start of the exercise."
    )