# test_initial_state.py
#
# Pytest suite to validate the machine *before* the student performs any
# action on the deployment-log task.
#
# This test file checks that:
#   1. The directory /home/user/deployment exists and is a directory.
#   2. The directory is writable by the current (normal) user.
#   3. The file /home/user/deployment/app_update.log exists.
#   4. The file contains exactly the expected lines (no more, no fewer,
#      and in the exact order shown in the task description).
#
# No checks are performed for any output artefacts that the student
# will create (e.g. error_summary.log), in accordance with the rules.

import os
from pathlib import Path
import pytest

DEPLOY_DIR = Path("/home/user/deployment")
LOG_FILE = DEPLOY_DIR / "app_update.log"

# The exact, canonical content expected in app_update.log
EXPECTED_LOG_LINES = [
    "[2023-05-01 10:00:00] INFO Starting deployment v2.3.4",
    "[2023-05-01 10:00:01] ERROR Failed to backup config for v2.3.4",
    "[2023-05-01 10:00:02] WARNING Low disk space on /dev/sda1",
    "[2023-05-01 10:00:03] ERROR Dependency mismatch v2.3.3",
    "[2023-05-01 10:00:04] INFO Copying binaries v2.3.4",
    "[2023-05-01 10:00:05] ERROR Timeout while restarting service v2.3.4",
    "[2023-05-01 10:00:06] INFO Deployment finished v2.3.4",
    "[2023-05-01 10:00:07] ERROR Rollback triggered v2.3.4",
    "[2023-05-01 10:00:08] INFO Cleanup complete",
]

def test_deploy_directory_exists_and_writable():
    """
    The deployment directory must exist and be writable so the student
    can create error_summary.log there.
    """
    assert DEPLOY_DIR.exists(), (
        f"Expected directory {DEPLOY_DIR} to exist, but it is missing."
    )
    assert DEPLOY_DIR.is_dir(), (
        f"Expected {DEPLOY_DIR} to be a directory, but it is not."
    )
    assert os.access(DEPLOY_DIR, os.W_OK), (
        f"Directory {DEPLOY_DIR} is not writable by the current user."
    )

def test_log_file_exists():
    """
    The raw deployment log must already be present.
    """
    assert LOG_FILE.exists(), (
        f"Expected log file {LOG_FILE} to exist, but it is missing."
    )
    assert LOG_FILE.is_file(), (
        f"Expected {LOG_FILE} to be a regular file."
    )

def test_log_file_contents_are_exact():
    """
    The log file should match the expected canonical content exactly.
    """
    with LOG_FILE.open("r", encoding="utf-8") as fh:
        actual_lines = [line.rstrip("\n") for line in fh.readlines()]

    # Provide a detailed diff-like explanation upon failure.
    if actual_lines != EXPECTED_LOG_LINES:
        diff = _pretty_diff(EXPECTED_LOG_LINES, actual_lines)
        pytest.fail(
            "Contents of {0} do not match the expected canonical log.\nDiff:\n{1}"
            .format(LOG_FILE, diff)
        )

def _pretty_diff(expected, actual):
    """
    Helper to generate a unified diff string for easier debugging when the
    comparison fails.  Uses only stdlib functionality.
    """
    import difflib
    diff_lines = difflib.unified_diff(
        expected,
        actual,
        fromfile="expected",
        tofile="actual",
        lineterm=""
    )
    return "\n".join(diff_lines)