# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present **before** the student starts implementing the data-engineering
# workflow described in the task.  It deliberately checks only the required
# source directory and its CSV contents; it does *not* touch any of the output
# paths the student will later create.

import os
from pathlib import Path

import pytest

SOURCE_DIR = Path("/home/user/source_data")

# Expected CSV files and their uncompressed byte-sizes
EXPECTED_CSVS = {
    "customers.csv": 22,
    "orders.csv": 56,
    "products.csv": 54,
}


def _get_csv_files(directory: Path):
    """
    Return a dict mapping every *.csv file directly inside `directory` to its
    size in bytes.
    """
    result = {}
    for entry in directory.iterdir():
        if entry.is_file() and entry.suffix.lower() == ".csv":
            result[entry.name] = entry.stat().st_size
    return result


def test_source_directory_exists_and_is_directory():
    """Verify that /home/user/source_data exists and is a directory."""
    assert SOURCE_DIR.exists(), (
        f"Expected directory {SOURCE_DIR} to exist, but it is missing."
    )
    assert SOURCE_DIR.is_dir(), (
        f"Expected {SOURCE_DIR} to be a directory, but it is not."
    )


def test_expected_csv_files_present_with_correct_sizes():
    """
    Ensure that all required CSV files are present in the source directory and
    each has the exact expected byte-size.
    """
    for filename, expected_size in EXPECTED_CSVS.items():
        file_path = SOURCE_DIR / filename
        assert file_path.exists(), (
            f"Required file {file_path} is missing."
        )
        assert file_path.is_file(), (
            f"Expected {file_path} to be a regular file."
        )
        actual_size = file_path.stat().st_size
        assert (
            actual_size == expected_size
        ), (
            f"File {file_path} has size {actual_size} bytes; "
            f"expected {expected_size} bytes."
        )


def test_no_extra_csv_files_present():
    """
    Confirm that **only** the three required CSV files are present; no extras.
    """
    found_csvs = _get_csv_files(SOURCE_DIR)
    extra_files = set(found_csvs) - set(EXPECTED_CSVS)
    missing_files = set(EXPECTED_CSVS) - set(found_csvs)

    assert not missing_files, (
        f"Missing required CSV files in {SOURCE_DIR}: {', '.join(sorted(missing_files))}"
    )
    assert not extra_files, (
        f"Unexpected CSV files present in {SOURCE_DIR}: {', '.join(sorted(extra_files))}"
    )
    # (Size mismatches are handled in a separate test.)