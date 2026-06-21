# test_initial_state.py
#
# This test-suite verifies that the *initial* filesystem state is present
# before the learner performs any actions.  These checks ensure the starting
# data is intact and nothing from the target solution already exists.
#
# NOTE:  Per the grading rubric we do *not* assert anything about the
#        eventual output artefacts (/home/user/backups, the .tar.gz file,
#        or the log file).  We only inspect the pre-existing “raw” data.

import os
import pytest

HOME = "/home/user"
RAW_DIR = os.path.join(HOME, "etl_project", "raw_data")

# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def _read_lines(path):
    """Return a list of lines with trailing newlines stripped."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().splitlines()


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_raw_data_directory_exists():
    assert os.path.isdir(RAW_DIR), (
        f"Expected directory {RAW_DIR!r} to exist, but it is missing."
    )


@pytest.mark.parametrize(
    "filename,expected_lines",
    [
        (
            "customers.csv",
            [
                "id,name",
                "1,Alice",
                "2,Bob",
            ],
        ),
        (
            "orders.csv",
            [
                "id,customer_id,total",
                "101,1,19.95",
                "102,2,5.00",
            ],
        ),
        (
            "products.csv",
            [
                "id,description,price",
                "501,Widget,9.99",
                "502,Gadget,5.00",
            ],
        ),
    ],
)
def test_each_csv_exists_and_has_expected_contents(filename, expected_lines):
    path = os.path.join(RAW_DIR, filename)

    # 1. File existence
    assert os.path.isfile(path), (
        f"Required file {path!r} is missing. The initial dataset must include "
        f"this file before the backup task can begin."
    )

    # 2. Contents
    actual_lines = _read_lines(path)
    assert actual_lines == expected_lines, (
        f"Contents of {path!r} do not match the expected initial data.\n"
        f"Expected lines:\n{expected_lines!r}\nGot:\n{actual_lines!r}"
    )


def test_no_unexpected_files_in_raw_data():
    """Ensure only the three expected CSV files are present at top level."""
    expected = {"customers.csv", "orders.csv", "products.csv"}
    try:
        observed = set(os.listdir(RAW_DIR))
    except FileNotFoundError:
        pytest.skip(f"Directory {RAW_DIR!r} is missing; handled in earlier test.")

    unexpected = observed - expected
    assert not unexpected, (
        f"Found unexpected files/directories in {RAW_DIR!r}: {sorted(unexpected)}. "
        "The initial state should contain only the specified CSV files."
    )