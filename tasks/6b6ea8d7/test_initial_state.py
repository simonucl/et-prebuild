# test_initial_state.py
#
# This pytest suite validates that the OS / filesystem is in the expected
# pristine state *before* the student performs any work.  It only touches the
# input data that must already exist and deliberately avoids testing for any of
# the output artefacts the student is expected to create later.
#
# Requirements verified:
#   • /home/user/data exists and is a directory
#   • Exactly two raw CSV files are present:
#       - /home/user/data/raw_run1.csv
#       - /home/user/data/raw_run2.csv
#   • Each CSV file contains the exact, line-for-line content specified in the
#     task description (header + 5 data rows, 6 lines total).
#
# If any of these checks fail, the assertion messages should make it clear
# what is missing or unexpected.

import os
import pytest

DATA_DIR = "/home/user/data"

# Expected contents for each CSV, expressed as tuples of lines so the order
# is unambiguous and easy to compare.
EXPECTED_CSV_CONTENT = {
    "/home/user/data/raw_run1.csv": (
        "timestamp,endpoint,latency_ms",
        "2023-09-01T10:00:00Z,/api/login,120",
        "2023-09-01T10:00:01Z,/api/items,200",
        "2023-09-01T10:00:02Z,/api/login,110",
        "2023-09-01T10:00:03Z,/api/items,220",
        "2023-09-01T10:00:04Z,/api/items,180",
    ),
    "/home/user/data/raw_run2.csv": (
        "timestamp,endpoint,latency_ms",
        "2023-09-01T11:00:00Z,/api/login,130",
        "2023-09-01T11:00:01Z,/api/items,210",
        "2023-09-01T11:00:02Z,/api/login,140",
        "2023-09-01T11:00:03Z,/api/items,190",
        "2023-09-01T11:00:04Z,/api/login,150",
    ),
}

################################################################################
# Basic directory checks
################################################################################


def test_data_directory_exists_and_is_dir():
    assert os.path.exists(
        DATA_DIR
    ), f"Required directory {DATA_DIR} does not exist."
    assert os.path.isdir(
        DATA_DIR
    ), f"Expected {DATA_DIR} to be a directory but it is not."


################################################################################
# File-presence checks
################################################################################


@pytest.mark.parametrize("csv_path", EXPECTED_CSV_CONTENT.keys())
def test_csv_file_present(csv_path):
    assert os.path.exists(
        csv_path
    ), f"Expected CSV file {csv_path} is missing."
    assert os.path.isfile(
        csv_path
    ), f"{csv_path} exists but is not a regular file."
    # Sanity-check file is non-empty
    assert (
        os.path.getsize(csv_path) > 0
    ), f"{csv_path} is empty; expected it to contain data."


################################################################################
# Exact content checks
################################################################################


@pytest.mark.parametrize(
    "csv_path,expected_lines", EXPECTED_CSV_CONTENT.items()
)
def test_csv_file_contents_exact(csv_path, expected_lines):
    """
    Validate that each CSV file matches the exact content (line-for-line)
    provided in the task specification. Newline differences (LF vs CRLF) are
    normalised away for comparison.
    """
    with open(csv_path, "r", encoding="utf-8") as fh:
        actual_lines = [line.rstrip("\r\n") for line in fh]

    assert (
        actual_lines == list(expected_lines)
    ), (
        f"Contents of {csv_path} do not match the expected specification.\n"
        f"Expected ({len(expected_lines)} lines):\n"
        f"    " + "\n    ".join(expected_lines) + "\n"
        f"Actual ({len(actual_lines)} lines):\n"
        f"    " + "\n    ".join(actual_lines)
    )