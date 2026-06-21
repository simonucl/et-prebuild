# test_initial_state.py
#
# This pytest suite validates the *initial* file-system state that must be
# present before the student starts working on the conversion task.
#
# It purposefully does **NOT** check for any of the files that the student is
# supposed to create (raw_metrics.json, summary.json, conversion.log), because
# at this point they must not exist yet.  It only asserts that the required
# source CSV file and its containing directory are present and correctly
# formed.

import os
import csv
from pathlib import Path

import pytest

# Constant paths so the checks are explicit and easy to read.
TEST_DATA_DIR = Path("/home/user/project/test_data")
RAW_CSV_PATH = TEST_DATA_DIR / "raw_metrics.csv"


@pytest.fixture(scope="module")
def csv_lines():
    """
    Read the CSV file once and return the list of lines.
    Will raise a helpful error if the file cannot be read.
    """
    if not RAW_CSV_PATH.exists():
        pytest.fail(
            f"Required file missing: {RAW_CSV_PATH}. "
            "Create this file before running the conversion script."
        )
    if not RAW_CSV_PATH.is_file():
        pytest.fail(f"{RAW_CSV_PATH} exists but is not a regular file.")

    try:
        content = RAW_CSV_PATH.read_text(encoding="utf-8").splitlines()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {RAW_CSV_PATH}: {exc}")

    if not content:
        pytest.fail(f"{RAW_CSV_PATH} is empty. It must contain header and data rows.")
    return content


def test_data_directory_exists():
    """The containing directory must exist and be a directory."""
    assert TEST_DATA_DIR.exists(), f"Missing directory: {TEST_DATA_DIR}"
    assert TEST_DATA_DIR.is_dir(), f"{TEST_DATA_DIR} exists but is not a directory."


def test_raw_metrics_csv_exists_and_readable():
    """The raw CSV must exist and be a regular file."""
    assert RAW_CSV_PATH.exists(), f"Missing file: {RAW_CSV_PATH}"
    assert RAW_CSV_PATH.is_file(), f"{RAW_CSV_PATH} exists but is not a regular file."
    # Additional read attempt to ensure readability
    try:
        RAW_CSV_PATH.open("r", encoding="utf-8").close()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Cannot open {RAW_CSV_PATH} for reading: {exc}")


def test_csv_header_is_correct(csv_lines):
    """The header must exactly match the required column names."""
    expected_header = "test_case,module,status,execution_time"
    header = csv_lines[0].strip()
    assert (
        header == expected_header
    ), f"CSV header mismatch.\nExpected: {expected_header!r}\nFound   : {header!r}"


def test_csv_rows_are_well_formed(csv_lines):
    """
    Every data row must contain exactly four comma-separated values.
    The execution_time field must parse as a float.
    """
    reader = csv.reader(csv_lines)
    # Skip header
    next(reader, None)

    row_count = 0
    for lineno, row in enumerate(reader, start=2):  # start=2 accounts for header
        row_count += 1
        assert len(row) == 4, (
            f"Line {lineno} in {RAW_CSV_PATH} does not have 4 columns: {row!r}"
        )
        test_case, module, status, execution_time = row

        # Basic sanity checks (non-empty strings)
        assert test_case, f"Empty test_case on line {lineno}"
        assert module, f"Empty module on line {lineno}"
        assert status in {"pass", "fail"}, (
            f"Invalid status '{status}' on line {lineno}; expected 'pass' or 'fail'"
        )

        # execution_time must convert to float
        try:
            float(execution_time)
        except ValueError:
            pytest.fail(
                f"execution_time '{execution_time}' on line {lineno} is not a number"
            )

    assert row_count > 0, (
        f"{RAW_CSV_PATH} must contain at least one data row after the header."
    )