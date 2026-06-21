# test_initial_state.py
#
# This pytest suite validates the pre-seeded filesystem state
# BEFORE the student performs any actions.  It checks only the
# input CSVs that the task description guarantees must already
# be present.  It explicitly does *not* look for any output or
# archive artefacts that the student is expected to create.
#
# Requirements verified:
#   • /home/user/data/csvs/ exists and is a directory.
#   • The three required CSV files exist at the given absolute
#     paths, are regular files, are readable, and have the exact
#     byte sizes specified by the grading rubric.
#   • Each CSV has the correct header row and the expected number
#     of data rows (header is *not* counted).
#
# Only stdlib + pytest are used.

import os
from pathlib import Path

import pytest


CSV_DIR = Path("/home/user/data/csvs")

# Mapping of filename → (expected_size_bytes, expected_row_count)
EXPECTED_CSVS = {
    "sales_2021_q1.csv": (71, 3),
    "sales_2021_q2.csv": (86, 4),
    "sales_2021_q3.csv": (54, 2),
}

HEADER_ROW = "Region,Product,Units"


def test_csv_directory_exists_and_is_dir():
    """Verify /home/user/data/csvs/ exists and is a directory."""
    assert CSV_DIR.exists(), (
        f"Required directory {CSV_DIR} is missing. "
        "The initial dataset must be placed here."
    )
    assert CSV_DIR.is_dir(), f"{CSV_DIR} exists but is not a directory."


@pytest.mark.parametrize("filename,meta", EXPECTED_CSVS.items())
def test_each_csv_exists_and_size_matches(filename, meta):
    """Check existence and exact byte size of every CSV."""
    expected_size, _ = meta
    path = CSV_DIR / filename

    assert path.exists(), (
        f"Required CSV {path} is missing. "
        "Ensure the pre-seeded files are present before starting the task."
    )
    assert path.is_file(), f"{path} exists but is not a regular file."

    actual_size = os.path.getsize(path)
    assert actual_size == expected_size, (
        f"{path} has size {actual_size} bytes, "
        f"but the expected size is {expected_size} bytes. "
        "Do not modify the initial CSVs."
    )


@pytest.mark.parametrize("filename,meta", EXPECTED_CSVS.items())
def test_csv_header_and_row_count(filename, meta):
    """Validate header row text and the number of data rows in each CSV."""
    _, expected_rows = meta
    path = CSV_DIR / filename

    # File already verified to exist in previous test.
    with path.open("rt", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    assert lines, f"{path} is empty."
    assert lines[0] == HEADER_ROW, (
        f"{path} has an unexpected header row:\n"
        f"  Found : {lines[0]!r}\n"
        f"  Expect: {HEADER_ROW!r}"
    )

    data_rows = lines[1:]  # skip header
    actual_row_count = len(data_rows)
    assert actual_row_count == expected_rows, (
        f"{path} should contain {expected_rows} data rows (excluding header), "
        f"but {actual_row_count} were found."
    )