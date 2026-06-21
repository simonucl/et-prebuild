# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student performs any action for the log-filtering
# task.  It checks that only the provided provisioning.log file is present
# with the exact expected content and that none of the artefacts the student
# is supposed to create already exist.
#
# NOTE: These tests must all pass *before* the student starts their work.

import os
import re
import stat
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME_DIR = "/home/user"
PROVISIONING_DIR = os.path.join(HOME_DIR, "provisioning")
LOGS_DIR = os.path.join(PROVISIONING_DIR, "logs")
OUTPUT_DIR = os.path.join(PROVISIONING_DIR, "output")
FILTER_SCRIPT = os.path.join(PROVISIONING_DIR, "filter_provisioning.sh")
PROVISIONING_LOG = os.path.join(LOGS_DIR, "provisioning.log")

EXPECTED_LOG_LINES = [
    "2023-08-01 10:01:15 INFO: Starting provisioning sequence id=abc123",
    "2023-08-01 10:01:20 WARN: Slow network detected, retries may occur",
    "2023-08-01 10:01:25 ERROR: VM web-01 failed to boot in allotted time",
    "2023-08-01 10:01:30 INFO: Attempting to recover VM web-01",
    "2023-08-01 10:01:35 ERROR: Instance db-02 failed healthcheck after provisioning",
    "2023-08-01 10:01:38 WARN: Provisioning latency above threshold",
    "2023-08-01 10:01:40 INFO: Provisioning sequence id=abc123 completed with errors",
]

# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def _read_log_lines(path):
    with open(path, encoding="utf-8") as fp:
        return [line.rstrip("\n") for line in fp.readlines()]

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_provisioning_log_exists_and_is_regular_file():
    """
    The provided provisioning.log must exist and be a regular file.
    """
    assert os.path.exists(PROVISIONING_LOG), (
        f"Expected provisioning log file at {PROVISIONING_LOG} is missing."
    )
    mode = os.stat(PROVISIONING_LOG).st_mode
    assert stat.S_ISREG(mode), (
        f"{PROVISIONING_LOG} exists but is not a regular file."
    )


def test_provisioning_log_content_exact_match():
    """
    provisioning.log must contain exactly the 7 expected lines in order.
    """
    lines = _read_log_lines(PROVISIONING_LOG)
    assert lines == EXPECTED_LOG_LINES, (
        "provisioning.log content mismatch.\n"
        f"Expected ({len(EXPECTED_LOG_LINES)} lines):\n"
        + "\n".join(EXPECTED_LOG_LINES)
        + "\n\nActual ({len(lines)} lines):\n"
        + "\n".join(lines)
    )


@pytest.mark.parametrize(
    "path, description",
    [
        (OUTPUT_DIR, "output directory"),
        (FILTER_SCRIPT, "filter_provisioning.sh script"),
        (os.path.join(OUTPUT_DIR, "error_summary.log"), "error_summary.log"),
        (os.path.join(OUTPUT_DIR, "last_run.status"), "last_run.status file"),
    ],
)
def test_student_artifacts_do_not_exist_yet(path, description):
    """
    None of the artefacts that the student is supposed to create should exist
    before the task starts.
    """
    assert not os.path.exists(path), (
        f"The {description} ({path}) should NOT exist before the student "
        "performs the task, but it is present."
    )


def test_no_extra_entries_in_provisioning_dir():
    """
    Ensure that within /home/user/provisioning/ we only have the 'logs'
    directory and its provisioning.log file.  This guards against any
    unexpected pre-existing artefacts.
    """
    expected_entries = {"logs"}
    actual_entries = set(os.listdir(PROVISIONING_DIR))
    assert actual_entries == expected_entries, (
        "Unexpected files or directories are present in "
        f"{PROVISIONING_DIR}.\nExpected only: {expected_entries}\n"
        f"Found: {actual_entries}"
    )