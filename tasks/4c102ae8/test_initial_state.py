# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system / filesystem
# state *before* the student starts working on the assignment.  It checks that
# the required source CSV files are present at the expected absolute paths and
# that each file contains the correct number of data rows (total lines minus the
# single header line).
#
# IMPORTANT:
#   * Do NOT test for any output artefacts such as
#     /home/user/benchmarks/csv_processing_benchmark.log.
#   * Use only Python’s standard library plus pytest.

import os
import pytest

# --------------------------------------------------------------------------- #
# Configuration: absolute file paths and their expected data-row counts
# --------------------------------------------------------------------------- #
CSV_SPECS = [
    ("/home/user/data/sales_q1.csv", 10),
    ("/home/user/data/sales_q2.csv", 8),
    ("/home/user/data/sales_q3.csv", 12),
]

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _read_lines(path):
    """Read a text file and return a list of its lines.
    The file is opened using universal newlines so all newline conventions are
    handled uniformly.
    """
    with open(path, "r", newline=None, encoding="utf-8") as fh:
        return fh.readlines()

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("csv_path,expected_rows", CSV_SPECS)
def test_csv_file_exists(csv_path, expected_rows):
    """Ensure each required CSV file is present and is a regular file."""
    assert os.path.exists(csv_path), (
        f"Required CSV file is missing: {csv_path!r}"
    )
    assert os.path.isfile(csv_path), (
        f"Path exists but is not a regular file: {csv_path!r}"
    )
    # Basic sanity: ensure file is readable and non-empty
    assert os.access(csv_path, os.R_OK), (
        f"CSV file is not readable by the current user: {csv_path!r}"
    )
    file_size = os.path.getsize(csv_path)
    assert file_size > 0, (
        f"CSV file appears to be empty: {csv_path!r}"
    )

@pytest.mark.parametrize("csv_path,expected_rows", CSV_SPECS)
def test_csv_row_counts(csv_path, expected_rows):
    """Verify each CSV file contains the expected number of data rows
    (total lines minus the single header line).
    """
    lines = _read_lines(csv_path)
    assert len(lines) >= 1, (
        f"CSV file {csv_path!r} should contain at least a header line."
    )

    header, *data_rows = lines
    actual_data_row_count = len(data_rows)

    assert actual_data_row_count == expected_rows, (
        "CSV file {path!r} has {actual} data rows; expected {expected}.\n"
        "Hint: data rows = total lines minus the header line.".format(
            path=csv_path,
            actual=actual_data_row_count,
            expected=expected_rows,
        )
    )