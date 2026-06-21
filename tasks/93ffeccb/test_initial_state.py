# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the expected *initial* state before the student executes any
# commands for the “temperature-telemetry” task.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"
LOG_FILE = LOG_DIR / "device_telemetry_2024-06-01.log"

OUTPUT_DIR = HOME / "output"
OUTPUT_FILE = OUTPUT_DIR / "hot_devices_2024-06-01.csv"


# ---------------------------------------------------------------------------
# Helper: the exact log-file contents that must exist *before* the task starts
# ---------------------------------------------------------------------------
EXPECTED_LOG_CONTENT = (
    "2024-06-01T10:00:00Z device_id=101 TEMP=69.0C VOLT=3.6\n"
    "2024-06-01T10:05:00Z device_id=102 TEMP=71.2C VOLT=3.6\n"
    "2024-06-01T10:10:00Z device_id=103 TEMP=66.5C VOLT=3.7\n"
    "2024-06-01T10:15:00Z device_id=104 TEMP=75.8C VOLT=3.5\n"
    "2024-06-01T10:20:00Z device_id=105 TEMP=70.0C VOLT=3.8\n"
    "2024-06-01T10:25:00Z device_id=106 TEMP=80.1C VOLT=3.6\n"
)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_logs_directory_exists():
    """The /home/user/logs directory must already exist."""
    assert LOG_DIR.is_dir(), (
        f"Required directory {LOG_DIR} is missing. "
        "The initial filesystem must provide the raw telemetry log."
    )


def test_log_file_exists():
    """The telemetry log file must already be present."""
    assert LOG_FILE.is_file(), (
        f"Required log file {LOG_FILE} is missing. "
        "Ensure the initial environment contains the raw telemetry data."
    )


def test_log_file_contents_are_exact():
    """
    The log file must contain the six expected lines,
    each terminated by a newline character, and nothing else.
    """
    with LOG_FILE.open("r", encoding="utf-8") as fp:
        actual = fp.read()

    assert actual == EXPECTED_LOG_CONTENT, (
        f"Log file {LOG_FILE} contents do not match the expected template.\n"
        "Differences detected between the actual and expected telemetry lines.\n"
        "Make sure the file is unmodified before the student runs their command."
    )


def test_output_directory_does_not_exist_yet():
    """
    /home/user/output should *not* exist before the student
    creates it in their solution. Its presence would indicate
    residual state from previous runs.
    """
    assert not OUTPUT_DIR.exists(), (
        f"Found unexpected directory {OUTPUT_DIR}. "
        "The output directory must be created by the student's command; "
        "it should not exist beforehand."
    )


def test_output_file_does_not_exist_yet():
    """
    The CSV file that the student must generate must not exist yet.
    """
    assert not OUTPUT_FILE.exists(), (
        f"Found unexpected file {OUTPUT_FILE}. "
        "The hot_devices CSV file must be produced by the student's command; "
        "it should not exist beforehand."
    )