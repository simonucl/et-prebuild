# test_initial_state.py
#
# This test-suite validates the **initial** operating-system / filesystem
# state *before* the student performs any actions for the “ML project”
# exercise.  It purposefully **does not** inspect any of the expected
# output paths (e.g. /home/user/ml_project, raw_data, processed_data,
# permissions_report.log) so that it remains a pure pre-flight check.
#
# The tests ensure that the required source data is present and correct,
# giving students a reliable starting point.
#
# Only Python’s standard library and pytest are used.


import os
import stat
import pytest

SOURCE_DIR = "/home/user/source_data"
CSV_PATH = os.path.join(SOURCE_DIR, "iris.csv")

EXPECTED_CSV_CONTENT = (
    "sepal_length,sepal_width,petal_length,petal_width,species\n"
    "5.1,3.5,1.4,0.2,setosa\n"
    "7.0,3.2,4.7,1.4,versicolor\n"
    "6.3,3.3,6.0,2.5,virginica\n"
)

EXPECTED_CSV_PERMS = 0o644  # octal literal


def test_source_data_directory_exists():
    """Ensure the /home/user/source_data directory is present."""
    assert os.path.isdir(
        SOURCE_DIR
    ), f"Required directory missing: {SOURCE_DIR}"


def test_iris_csv_exists_and_is_file():
    """Verify that the iris.csv file exists at the expected location."""
    assert os.path.isfile(
        CSV_PATH
    ), f"Required file missing: {CSV_PATH}"


def test_iris_csv_content_exact_match():
    """
    The iris.csv file must match the canonical 4-line CSV exactly,
    including newlines and header order.
    """
    with open(CSV_PATH, "r", newline="") as fh:
        actual = fh.read()

    assert actual == EXPECTED_CSV_CONTENT, (
        "Content mismatch in iris.csv.\n"
        "If you believe the file is correct, double-check for extra "
        "spaces, missing newlines, or DOS line endings (\\r\\n)."
    )


def test_iris_csv_permissions_are_644():
    """Confirm that iris.csv starts with permission bits 644."""
    mode = os.stat(CSV_PATH).st_mode & 0o777
    assert mode == EXPECTED_CSV_PERMS, (
        f"iris.csv permissions are {oct(mode)[2:]} but should be 644."
    )