# test_initial_state.py
#
# Pytest suite that verifies the *initial* filesystem / dataset state
# before the student runs any command for the “error summary” exercise.
#
# DO NOT modify this file.  If any of the tests below fail, the exercise
# setup is incomplete or has been altered.

import csv
import os
from pathlib import Path

# ---------- Constants --------------------------------------------------------

DATA_FILE = Path("/home/user/data/logs.csv")
EXPECTED_HEADER = ["timestamp", "node_id", "level", "message"]
ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}

# ---------- Helper Functions -------------------------------------------------


def _read_csv_rows(path: Path):
    """
    Read all rows from the given CSV file using the standard library `csv`
    and UTF-8 decoding.  Returns a list of row dicts (header → value).
    """
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


# ---------- Tests ------------------------------------------------------------


def test_source_file_exists_and_is_file():
    """
    The source data file must exist and be a regular file that can be read.
    """
    assert DATA_FILE.exists(), (
        f"Expected source data file not found: {DATA_FILE!s}\n"
        "Make sure the exercise data has been copied to the correct location."
    )
    assert DATA_FILE.is_file(), f"{DATA_FILE!s} exists but is not a regular file."


def test_csv_header_is_correct():
    """
    The first row of the CSV must contain the expected four columns in order.
    """
    with DATA_FILE.open("r", encoding="utf-8", newline="") as fh:
        header_line = fh.readline().rstrip("\n")
    header_cols = header_line.split(",")
    assert header_cols == EXPECTED_HEADER, (
        "CSV header mismatch.\n"
        f"Expected: {EXPECTED_HEADER}\n"
        f"Found   : {header_cols}"
    )


def test_csv_rows_are_well_formed():
    """
    Every data row must have exactly four fields; the 'level' field must
    contain only INFO, WARN or ERROR.
    """
    rows = _read_csv_rows(DATA_FILE)

    # --- structural checks ---------------------------------------------------
    for idx, row in enumerate(rows, start=2):  # start=2 accounts for header line
        assert set(row.keys()) == set(EXPECTED_HEADER), (
            f"Row {idx} does not contain the expected columns.\n"
            f"Expected columns: {EXPECTED_HEADER}\n"
            f"Found columns   : {list(row.keys())}"
        )

        # Validate 'level' field content
        level_value = row["level"]
        assert level_value in ALLOWED_LEVELS, (
            f"Invalid 'level' value in row {idx}: {level_value!r}\n"
            f"Allowed values: {sorted(ALLOWED_LEVELS)}"
        )


def test_error_row_counts_match_truth():
    """
    Verify that the distribution of ERROR rows per node_id matches the
    exercise description.  This guards against accidental data corruption.
    """
    rows = _read_csv_rows(DATA_FILE)
    error_counts = {}

    for row in rows:
        if row["level"] == "ERROR":
            error_counts[row["node_id"]] = error_counts.get(row["node_id"], 0) + 1

    expected_counts = {"node-1": 3, "node-2": 2, "node-3": 1}

    assert error_counts == expected_counts, (
        "ERROR count per node_id does not match the expected dataset.\n"
        f"Expected: {expected_counts}\n"
        f"Found   : {error_counts}"
    )