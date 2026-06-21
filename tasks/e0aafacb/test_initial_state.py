# test_initial_state.py
#
# This pytest suite validates the **initial** state of the filesystem
# before the student performs any actions.
#
# It confirms that:
#   1. The directory /home/user/data exists.
#   2. The file  /home/user/data/alerts.csv exists.
#   3. The contents of alerts.csv are **exactly** as specified
#      (including the final trailing newline).
#
# NOTE: Per grading-framework rules we do **not** test any output
#       files or directories.

import os
from pathlib import Path

import pytest


DATA_DIR = Path("/home/user/data")
ALERTS_CSV = DATA_DIR / "alerts.csv"

# The exact, byte-for-byte expected contents of alerts.csv
EXPECTED_ALERTS_CSV = (
    "id,timestamp,severity,description\n"
    "A1,2024-07-15T11:22:33Z,high,CPU usage >90%\n"
    "A2,2024-07-15T11:25:10Z,medium,Disk read latency\n"
    "A3,2024-07-15T11:30:22Z,high,Unauthorised login attempt\n"
    "A4,2024-07-15T11:35:42Z,low,Service restart completed\n"
)


def test_data_directory_exists():
    """/home/user/data must exist and be a directory."""
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."


def test_alerts_csv_exists():
    """alerts.csv must be present in /home/user/data."""
    assert ALERTS_CSV.exists(), f"Required file {ALERTS_CSV} is missing."
    assert ALERTS_CSV.is_file(), f"{ALERTS_CSV} exists but is not a regular file."


def test_alerts_csv_contents_exact():
    """alerts.csv must match the expected contents exactly (including final newline)."""
    with ALERTS_CSV.open("r", encoding="utf-8") as f:
        actual_contents = f.read()

    # Use pytest's assertion rewriting to show a diff if it mismatches.
    assert (
        actual_contents == EXPECTED_ALERTS_CSV
    ), (
        "The contents of /home/user/data/alerts.csv do not match the expected "
        "initial state. Please ensure the file is unmodified and contains:\n\n"
        f"{EXPECTED_ALERTS_CSV}"
    )