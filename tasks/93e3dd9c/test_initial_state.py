# test_initial_state.py
#
# Pytest suite that validates the machine’s initial state **before**
# the learner performs any action for the “CSV disk-usage summary”
# task.  Only the pre-existing files and directories are inspected;
# nothing related to the expected *output* directory or log file
# is tested here.

import os
import stat
import pytest

CSV_DIR = "/home/user/data/csv"

# Mapping of expected CSV files to their exact on-disk sizes (bytes)
EXPECTED_FILES = {
    "customers.csv": 1250,
    "orders.csv": 2750,
    "returns.csv": 500,
}


def _full(path_fragment: str) -> str:
    """Return an absolute path under the CSV directory."""
    return os.path.join(CSV_DIR, path_fragment)


def test_csv_directory_exists_and_is_directory():
    assert os.path.exists(CSV_DIR), (
        f"The directory {CSV_DIR!r} is missing. It must exist and contain "
        "the CSV datasets before you begin the task."
    )
    assert os.path.isdir(CSV_DIR), (
        f"{CSV_DIR!r} exists but is not a directory. "
        "It must be a directory that stores the CSV datasets."
    )


@pytest.mark.parametrize("fname,size", EXPECTED_FILES.items())
def test_each_expected_csv_file_exists_with_correct_size(fname, size):
    fpath = _full(fname)

    assert os.path.exists(fpath), (
        f"Expected CSV file {fpath!r} is missing. "
        "Make sure the initial data is present before running the task."
    )

    # Ensure it is a regular file (not a dir, pipe, etc.)
    st_mode = os.stat(fpath).st_mode
    assert stat.S_ISREG(st_mode), (
        f"{fpath!r} exists but is not a regular file. "
        "It should be a normal CSV file."
    )

    actual_size = os.path.getsize(fpath)
    assert actual_size == size, (
        f"{fpath!r} has size {actual_size} bytes, "
        f"but {size} bytes were expected. "
        "Verify that the correct dataset versions are in place."
    )


def test_no_extra_csv_files_present():
    """
    Ensure there are *only* the expected CSV files in the directory.
    Extra files could change the total-size computation and break
    downstream logic.
    """
    present_csv_files = sorted(
        f
        for f in os.listdir(CSV_DIR)
        if os.path.isfile(_full(f)) and f.lower().endswith(".csv")
    )
    expected_csv_files = sorted(EXPECTED_FILES.keys())

    assert present_csv_files == expected_csv_files, (
        "The CSV directory contains a different set of .csv files than "
        "expected.\n"
        f"Expected only: {expected_csv_files}\n"
        f"Found: {present_csv_files}\n"
        "Remove any unexpected files or rename them, and ensure the three "
        "required datasets are present before proceeding."
    )