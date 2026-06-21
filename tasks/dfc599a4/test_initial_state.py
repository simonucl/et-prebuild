# test_initial_state.py
#
# Pytest suite to validate the pristine filesystem state BEFORE the student
# starts working on the assignment.  These tests check only the *existing*
# input artefacts and purposely avoid touching anything the student is
# expected to create later (e.g. /home/user/analysis or its contents).

from pathlib import Path
import pytest

HOME = Path("/home/user")
DATA_DIR = HOME / "data"

EXPECTED_FILES = [
    "sales_q1_2022.csv",
    "sales_q2_2022.csv",
    "sales_q3_2022.csv",
    "sales_q4_2022.csv",
]

HEADER = "Region,Product,Units,Unit_Price,Transaction_Date"


def read_lines(path: Path):
    """
    Helper: return the list of lines in the file with trailing newlines stripped.
    """
    return path.read_text(encoding="utf-8").rstrip("\n").split("\n")


def test_data_directory_exists():
    """Verify that /home/user/data exists and is a directory."""
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} does not exist."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."


@pytest.mark.parametrize("filename", EXPECTED_FILES)
def test_each_csv_file_exists(filename):
    """Each expected quarterly CSV file must be present in /home/user/data."""
    path = DATA_DIR / filename
    assert path.exists(), f"Expected file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."


@pytest.mark.parametrize("filename", EXPECTED_FILES)
def test_csv_header_and_line_counts(filename):
    """
    Every quarterly CSV must:
      • start with the correct header line
      • contain exactly 1 header + 3 data rows = 4 lines
    """
    path = DATA_DIR / filename
    lines = read_lines(path)

    # Header check
    assert lines[0] == HEADER, (
        f"{path} has an unexpected header.\n"
        f"Expected: {HEADER}\n"
        f"Actual  : {lines[0]}"
    )

    # Line-count check
    assert len(lines) == 4, (
        f"{path} should have exactly 4 lines "
        f"(1 header + 3 data rows) but has {len(lines)}."
    )


def test_total_data_rows_across_all_files():
    """Across all four CSV files there must be exactly 12 data rows in total."""
    total_rows = 0
    for fname in EXPECTED_FILES:
        lines = read_lines(DATA_DIR / fname)
        # subtract 1 for the header
        total_rows += len(lines) - 1

    assert total_rows == 12, (
        "The combined number of data rows across the quarterly files should be 12 "
        f"but is {total_rows}."
    )