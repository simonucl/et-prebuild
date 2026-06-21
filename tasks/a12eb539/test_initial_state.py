# test_initial_state.py
#
# This test-suite validates the *initial* operating-system / filesystem
# state **before** the student performs any actions for the “alpha321
# error-log isolation” task.
#
# It verifies that:
#   1. The source log file exists in the expected location **and** has the
#      exact, unmodified contents that the grading rubric is built upon.
#   2. The output directory and result files that the student is supposed
#      to create do **not** exist yet.
#
# Any failure here means the environment is not in the pristine state that
# the assignment requires.

import os
import pytest

RAW_LOG_PATH = "/home/user/deployment/logs/raw_device.log"
PROCESSED_DIR = "/home/user/deployment/processed"
ERROR_LOG_PATH = "/home/user/deployment/processed/alpha321_errors.log"
SUMMARY_LOG_PATH = "/home/user/deployment/processed/alpha321_errors_summary.log"

EXPECTED_RAW_CONTENT = (
    "[2023-08-12 14:03:22] [INFO]  DeviceID=alpha321 Temperature=23.4C\n"
    "[2023-08-12 14:04:03] [WARN]  DeviceID=beta654  Battery=15%\n"
    "[2023-08-12 14:05:10] [ERROR] DeviceID=alpha321 SensorFailure=Temp\n"
    "[2023-08-12 14:05:46] [ERROR] DeviceID=gamma999 ConnectionLost\n"
    "[2023-08-12 14:06:22] [INFO]  DeviceID=alpha321 Reconnected\n"
    "[2023-08-12 14:07:00] [ERROR] DeviceID=alpha321 SensorFailure=Humidity\n"
)


def test_raw_log_exists_with_correct_content():
    """
    The raw log must exist and match exactly the expected baseline content.
    """
    assert os.path.isfile(
        RAW_LOG_PATH
    ), f"Required source log file is missing at {RAW_LOG_PATH!r}."

    with open(RAW_LOG_PATH, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    assert (
        actual_content == EXPECTED_RAW_CONTENT
    ), (
        "The contents of the source log file do not match the expected "
        "initial state. If the file was modified, restore it to the exact "
        "original lines defined in the assignment specification."
    )


def test_processed_directory_absent_or_clean():
    """
    Before the student runs their solution, the processed directory
    should either not exist or exist without the target output files.
    """
    if os.path.exists(PROCESSED_DIR):
        # Directory is present; ensure expected output files are still absent.
        assert not os.path.exists(
            ERROR_LOG_PATH
        ), f"Output file {ERROR_LOG_PATH!r} already exists but should not."
        assert not os.path.exists(
            SUMMARY_LOG_PATH
        ), f"Output file {SUMMARY_LOG_PATH!r} already exists but should not."
    else:
        # Directory is absent, which is an acceptable pristine state.
        assert True, "Processed directory does not yet exist (this is expected)."