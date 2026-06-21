# test_initial_state.py
#
# Pytest suite that validates the *initial* file-system state expected
# before the student runs any commands for the “quarterly sales CSV” task.
#
# The tests deliberately focus on the presence and contents of the source
# CSV files and the *absence* of the output artefact that the student is
# supposed to create later (/home/user/analysis/row_counts.log).

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the required initial state of the system.
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/data/csvs")
ARCHIVE_DIR = BASE_DIR / "archive"

CSV_FILES_INFO = {
    BASE_DIR / "sales_central.csv": 3,
    BASE_DIR / "sales_east.csv": 4,
    BASE_DIR / "sales_west.csv": 2,
    ARCHIVE_DIR / "sales_north.csv": 5,
}

CSV_HEADER = "OrderID,Product,Quantity"

ANALYSIS_DIR = Path("/home/user/analysis")
ROW_COUNT_LOG = ANALYSIS_DIR / "row_counts.log"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _read_file_lines(path: Path):
    """Return a list of lines *without* their trailing newline characters."""
    with path.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f.readlines()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directory_structure_exists():
    """Verify that the expected directories exist and are directories."""
    assert BASE_DIR.is_dir(), f"Missing directory: {BASE_DIR}"
    assert ARCHIVE_DIR.is_dir(), f"Missing directory: {ARCHIVE_DIR}"


@pytest.mark.parametrize("csv_path,expected_rows", CSV_FILES_INFO.items())
def test_csv_files_exist_and_row_counts(csv_path: Path, expected_rows: int):
    """
    Ensure every CSV exists, is a regular file, has the correct header,
    and the expected number of data rows (lines after the header).
    """
    # Existence & type
    assert csv_path.exists(), f"Expected CSV file is missing: {csv_path}"
    assert csv_path.is_file(), f"Path exists but is not a file: {csv_path}"

    # Content checks
    lines = _read_file_lines(csv_path)

    # At minimum we need header + at least one data row
    assert len(lines) >= 2, (
        f"{csv_path} should contain at least one data row plus the header."
    )

    # Header equality
    assert (
        lines[0] == CSV_HEADER
    ), f"Header of {csv_path} is incorrect. Expected: {CSV_HEADER!r}"

    # Data-row count
    data_row_count = len(lines) - 1
    assert (
        data_row_count == expected_rows
    ), f"{csv_path} should have {expected_rows} data rows, found {data_row_count}."


def test_no_analysis_log_yet():
    """
    The row_counts.log file should NOT exist before the student runs their command.
    The directory may or may not exist, but the artefact must be absent to
    guarantee that the student's work is actually creating it.
    """
    assert not ROW_COUNT_LOG.exists(), (
        f"Output artefact already exists: {ROW_COUNT_LOG}. "
        "The exercise requires the student to create this file."
    )