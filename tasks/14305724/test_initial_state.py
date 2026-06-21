# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# *before* the student performs any actions for the “slow query” task.
#
# The checks performed are:
#   1. The directory /home/user/db exists and is writable.
#   2. The file /home/user/db/slow_query.log exists with exactly the
#      expected 14 lines (each ending with “\n”, no more, no less, order preserved).
#   3. The output artefacts that the student is supposed to create
#      (/home/user/db/slow_query_frequency.tsv and
#       /home/user/db/slow_query_summary.log) must *not* exist yet.
#
# No third-party libraries are used; only the Python stdlib and pytest.

import os
from pathlib import Path

import pytest

DB_DIR = Path("/home/user/db")
LOG_FILE = DB_DIR / "slow_query.log"
FREQ_FILE = DB_DIR / "slow_query_frequency.tsv"
SUMMARY_FILE = DB_DIR / "slow_query_summary.log"

EXPECTED_LINES = [
    "SELECT * FROM orders WHERE status = 'pending';\n",
    "SELECT id, name FROM customers WHERE country = 'US';\n",
    "UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 42;\n",
    "SELECT * FROM orders WHERE status = 'pending';\n",
    "SELECT * FROM orders WHERE status = 'pending';\n",
    "UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 42;\n",
    "SELECT id, name FROM customers WHERE country = 'US';\n",
    "DELETE FROM sessions WHERE last_active < NOW() - INTERVAL '30 days';\n",
    "SELECT * FROM orders WHERE status = 'pending';\n",
    "DELETE FROM sessions WHERE last_active < NOW() - INTERVAL '30 days';\n",
    "SELECT * FROM orders WHERE status = 'pending';\n",
    "SELECT id, name FROM customers WHERE country = 'US';\n",
    "INSERT INTO audit_log (event, created_at) VALUES ('login', NOW());\n",
    "SELECT * FROM orders WHERE status = 'pending';\n",
]


def test_db_directory_exists_and_writable():
    assert DB_DIR.exists(), f"Required directory {DB_DIR} does not exist."
    assert DB_DIR.is_dir(), f"{DB_DIR} exists but is not a directory."
    # os.access with W_OK returns True if the effective UID can write there
    assert os.access(DB_DIR, os.W_OK), f"Directory {DB_DIR} is not writable by the current user."


def test_original_log_file_contents_exact():
    assert LOG_FILE.exists(), f"Required log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."

    # Read with keepends=True to preserve newline characters for validation
    with LOG_FILE.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert (
        len(lines) == 14
    ), f"{LOG_FILE} should contain exactly 14 lines, found {len(lines)}."

    # Check that every line ends with exactly one '\n'
    for idx, line in enumerate(lines, start=1):
        assert line.endswith(
            "\n"
        ), f"Line {idx} in {LOG_FILE} must end with a newline character."

    assert (
        lines == EXPECTED_LINES
    ), "The contents of slow_query.log do not match the expected lines.\n" \
       "Differences may include line ordering, missing/extra lines, or incorrect text."


def test_output_files_do_not_yet_exist():
    assert not FREQ_FILE.exists(), (
        f"Output file {FREQ_FILE} already exists before the task is run; "
        "it should be created by the student's solution, not pre-existing."
    )
    assert not SUMMARY_FILE.exists(), (
        f"Output file {SUMMARY_FILE} already exists before the task is run; "
        "it should be created by the student's solution, not pre-existing."
    )