# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem state
# *before* the student performs any action for the “transactions cleaning” task.
#
# This file must reside in the same directory from which pytest is executed.
# It requires only the Python standard library and pytest.
#
# What we check for:
#   1. Required directories exist (/home/user/data and /home/user/task_logs).
#   2. /home/user/data/raw_transactions.csv exists and contains exactly the
#      four expected UTF-8 lines (one header + three data rows).
#   3. /home/user/task_logs is empty and writable by the current user.
#
# We explicitly DO NOT check for any artefacts that belong to the student’s
# solution (locale_timezone_check.log, cleaned CSV, cleaning_steps.log, or the
# cleaned/ directory), in accordance with the assessment rules.

import os
from pathlib import Path

import pytest

# Constants for paths we will validate
HOME_DIR = Path("/home/user")
DATA_DIR = HOME_DIR / "data"
RAW_CSV = DATA_DIR / "raw_transactions.csv"
TASK_LOGS_DIR = HOME_DIR / "task_logs"


def test_data_directory_exists():
    """Ensure /home/user/data directory exists."""
    assert DATA_DIR.exists(), "Required directory '/home/user/data' is missing."
    assert DATA_DIR.is_dir(), "'/home/user/data' exists but is not a directory."


def test_raw_transactions_file_exact_content():
    """
    Confirm that the raw CSV exists, is a file, is readable, and contains the
    exact four expected lines in UTF-8.
    """
    assert RAW_CSV.exists(), (
        "Required file '/home/user/data/raw_transactions.csv' is missing."
    )
    assert RAW_CSV.is_file(), (
        "'/home/user/data/raw_transactions.csv' exists but is not a regular file."
    )

    # Read the file as UTF-8; an exception here will naturally fail the test.
    with RAW_CSV.open("r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    expected_lines = [
        "id,product,price_usd,utc_time",
        "1,Book,12.99,2022-03-13T06:30:00Z",
        "2,Pen,1.50,2022-11-06T05:15:00Z",
        "3,Notebook,4.20,2022-12-01T16:00:00Z",
    ]

    assert (
        lines == expected_lines
    ), (
        f"'/home/user/data/raw_transactions.csv' does not contain the expected "
        f"content.\nExpected {len(expected_lines)} lines:\n{expected_lines}\n\n"
        f"Got {len(lines)} lines:\n{lines}"
    )


def test_task_logs_directory_state():
    """
    Ensure /home/user/task_logs directory exists, is empty, and is writable by
    the current user.
    """
    assert TASK_LOGS_DIR.exists(), "Required directory '/home/user/task_logs' is missing."
    assert TASK_LOGS_DIR.is_dir(), "'/home/user/task_logs' exists but is not a directory."

    # Directory must be empty at the beginning of the task.
    contents = list(TASK_LOGS_DIR.iterdir())
    assert (
        len(contents) == 0
    ), (
        f"'/home/user/task_logs' should be empty initially, but contains: "
        f"{[p.name for p in contents]}"
    )

    # Check writability: attempt to create and delete a temporary file.
    tmp_file = TASK_LOGS_DIR / ".pytest_write_test"
    try:
        with tmp_file.open("w") as fh:
            fh.write("write-test")
    except PermissionError as exc:
        pytest.fail(
            f"'/home/user/task_logs' is not writable by the current user: {exc}"
        )
    finally:
        # Clean up the temporary file if it was created
        try:
            tmp_file.unlink()
        except FileNotFoundError:
            pass
        except PermissionError as exc:
            pytest.fail(
                f"Temporary file in '/home/user/task_logs' could not be removed: {exc}"
            )