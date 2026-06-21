# test_initial_state.py
#
# This pytest suite verifies that the **initial** filesystem state is exactly as
# required *before* the student begins any work.  In particular, it checks that
# the two raw CSV files exist at the correct absolute paths and contain the
# expected, unaltered data.  Nothing about the student’s deliverables is tested
# here – those will be validated in a different stage after the student’s
# solution runs.
#
# NOTE:  All paths are absolute and inside /home/user as mandated.

import pathlib

import pytest

# --------------------------------------------------------------------------- #
# Expected constants
# --------------------------------------------------------------------------- #

DATASET_DIR = pathlib.Path("/home/user/datasets")
Q1_FILE = DATASET_DIR / "sales_Q1.csv"
Q2_FILE = DATASET_DIR / "sales_Q2.csv"

EXPECTED_Q1_LINES = [
    "id,category,amount",
    "1,Electronics,120",
    "2,Furniture,300",
    "3,Electronics,80",
    "4,Toys,25",
    "5,Books,15",
    "6,Electronics,200",
    "7,Books,20",
]

EXPECTED_Q2_LINES = [
    "id,category,amount",
    "1,Toys,30",
    "2,Furniture,150",
    "3,Electronics,220",
    "4,Toys,40",
    "5,Books,18",
    "6,Kitchen,80",
    "7,Electronics,130",
]


# --------------------------------------------------------------------------- #
# Helper(s)
# --------------------------------------------------------------------------- #
def _read_csv_lines(path: pathlib.Path):
    """
    Read a file, normalising newlines to '\n' and stripping a single trailing
    newline so comparisons are independent of the final newline character.
    Returns the file as a list of lines (without line‐ending characters).
    """
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n")
    return content.split("\n")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_dataset_directory_exists():
    assert DATASET_DIR.is_dir(), (
        f"Required directory {DATASET_DIR} is missing. "
        "The initial datasets must be placed here *before* running the task."
    )


@pytest.mark.parametrize(
    ("csv_path", "expected_lines"),
    [
        (Q1_FILE, EXPECTED_Q1_LINES),
        (Q2_FILE, EXPECTED_Q2_LINES),
    ],
)
def test_raw_csv_file_exists_and_matches_expected(csv_path: pathlib.Path, expected_lines):
    # 1. File existence
    assert csv_path.is_file(), (
        f"Required data file {csv_path} does not exist. "
        "It should be provided to the student verbatim."
    )

    # 2. Exact content check
    actual_lines = _read_csv_lines(csv_path)
    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of {csv_path} do not match the expected initial dataset.\n\n"
        f"Expected lines ({len(expected_lines)}):\n" + "\n".join(expected_lines) + "\n\n"
        f"Actual lines   ({len(actual_lines)}):\n" + "\n".join(actual_lines)
    )