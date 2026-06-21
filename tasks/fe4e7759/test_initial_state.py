# test_initial_state.py
#
# This test-suite validates the OS / filesystem *before* the student starts
# working on the task.  It ensures that the expected input data is present
# and correct.  It deliberately avoids checking for any of the artefacts
# that the student is supposed to create later.

import csv
from pathlib import Path

import pytest

# Constants ---------------------------------------------------------------

CSV_PATH = Path("/home/user/device_data/devices.csv")

EXPECTED_HEADER = ["id", "location", "temp_c", "battery_v"]

EXPECTED_ROWS = [
    ["dev-001", "roof-nw", "68.3", "3.7"],
    ["dev-002", "roof-se", "72.4", "3.8"],
    ["dev-003", "lab-south", "75.0", "3.6"],
    ["dev-004", "lab-north", "70.0", "3.9"],
    ["dev-005", "warehouse", "71.2", "3.8"],
]


# Helpers -----------------------------------------------------------------


def read_csv_rows(path: Path):
    """
    Read a CSV file and return a tuple (header, rows).

    Each row is a list of strings as read from the file; no type coercion
    is applied because we just need exact textual equality.
    """
    with path.open(newline="") as fp:
        reader = csv.reader(fp)
        rows = list(reader)

    if not rows:
        pytest.fail(f"{path} is empty; expected header and 5 data rows.")

    return rows[0], rows[1:]


# Tests -------------------------------------------------------------------


def test_csv_file_exists_and_is_regular():
    """
    The device data CSV must exist and be a regular readable file.
    """
    assert CSV_PATH.exists(), f"Required file {CSV_PATH} is missing."
    assert CSV_PATH.is_file(), f"{CSV_PATH} exists but is not a regular file."
    assert CSV_PATH.stat().st_size > 0, f"{CSV_PATH} is zero-length; data expected."


def test_csv_content_matches_expected():
    """
    Validate header and data rows in devices.csv exactly match
    what the grading environment is supposed to provide.
    """
    header, rows = read_csv_rows(CSV_PATH)

    # Header check
    assert (
        header == EXPECTED_HEADER
    ), f"Header mismatch in {CSV_PATH}. Expected {EXPECTED_HEADER}, got {header}."

    # Row count check
    assert (
        len(rows) == 5
    ), f"{CSV_PATH} should contain exactly 5 data rows; found {len(rows)}."

    # Row-by-row content check
    for index, (expected, actual) in enumerate(zip(EXPECTED_ROWS, rows), start=1):
        assert (
            expected == actual
        ), (
            f"Row {index} in {CSV_PATH} does not match expectation.\n"
            f"Expected: {expected}\nActual  : {actual}"
        )