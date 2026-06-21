# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system /
# filesystem before the learner starts working on the “optimized bundle” task.
#
# The assertions are derived from the public task description and the
# accompanying “truth value”.  Any failure means the sandbox is not in the
# expected pristine state and the learner would start from a wrong baseline.

import os
import pytest
from pathlib import Path
import csv

HOME = Path("/home/user")
RAW_DIR = HOME / "raw_data"
OPTIMIZED_DIR = HOME / "optimized_data"

CSV_FILES = [
    "records_A.csv",
    "records_B.csv",
]

EXPECTED_FILE_SIZE = 24          # bytes
EXPECTED_ROW_COUNT = 3           # data rows (header not counted)


def read_csv_row_count(csv_path: Path) -> int:
    """
    Return the number of data rows in the CSV file, excluding the header.
    Assumes the file is small and well-formed (per task description).
    """
    with csv_path.open(newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)  # consume header
        return sum(1 for _ in reader)


def test_raw_data_directory_exists():
    assert RAW_DIR.exists(), f"Directory {RAW_DIR} is missing."
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."


@pytest.mark.parametrize("filename", CSV_FILES)
def test_raw_csv_presence_and_contents(filename):
    csv_path = RAW_DIR / filename

    # --- presence ---
    assert csv_path.exists(), f"Expected CSV file {csv_path} is missing."
    assert csv_path.is_file(), f"{csv_path} exists but is not a regular file."

    # --- size ---
    size = csv_path.stat().st_size
    assert size == EXPECTED_FILE_SIZE, (
        f"{csv_path} has size {size} bytes; expected {EXPECTED_FILE_SIZE} bytes."
    )

    # --- row count ---
    rows = read_csv_row_count(csv_path)
    assert rows == EXPECTED_ROW_COUNT, (
        f"{csv_path} contains {rows} data rows; expected {EXPECTED_ROW_COUNT}."
    )


def test_no_optimized_data_yet():
    """
    Before the learner starts, the /home/user/optimized_data directory (and
    everything under it) must *not* exist.  Its presence would indicate that
    the workspace is dirty or the task was already partially executed.
    """
    assert not OPTIMIZED_DIR.exists(), (
        f"Found unexpected directory {OPTIMIZED_DIR}. "
        "The workspace is not in the pristine initial state."
    )