# test_initial_state.py
#
# This pytest suite validates the _initial_ operating-system / filesystem state
# expected **before** the student carries out any actions described in the
# assignment.  Specifically, it checks that two CSV data files already exist in
# /home/user/data and that their line-counts match the specification.
#
# IMPORTANT:  Per the meta-rules, we intentionally do **not** look for the
# benchmark output directory or log file that the student will create later.

import os
from pathlib import Path

import pytest

# Absolute paths that must be present beforehand.
DATA_DIR = Path("/home/user/data")
Q1_FILE = DATA_DIR / "sales_q1.csv"
Q2_FILE = DATA_DIR / "sales_q2.csv"


@pytest.mark.parametrize(
    "pathobj, is_dir",
    [
        (DATA_DIR, True),
        (Q1_FILE, False),
        (Q2_FILE, False),
    ],
)
def test_paths_exist(pathobj: Path, is_dir: bool):
    """
    Ensure that the expected directory and files exist with the correct type.
    """
    assert pathobj.exists(), f"Required path {pathobj} is missing."
    if is_dir:
        assert pathobj.is_dir(), f"Expected {pathobj} to be a directory."
    else:
        assert pathobj.is_file(), f"Expected {pathobj} to be a regular file."


@pytest.mark.parametrize(
    "file_path, expected_lines",
    [
        (Q1_FILE, 11),
        (Q2_FILE, 8),
    ],
)
def test_line_counts(file_path: Path, expected_lines: int):
    """
    Verify that each CSV file has exactly the expected number of lines.
    The count **includes** the header row.
    """
    with file_path.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    actual = len(lines)
    assert (
        actual == expected_lines
    ), f"{file_path} should have {expected_lines} lines, but has {actual}."


def test_header_row():
    """
    Confirm that both CSV files start with the correct header row.
    """
    expected_header = "id,region,sales,week\n"
    for file_path in (Q1_FILE, Q2_FILE):
        with file_path.open("r", encoding="utf-8") as fh:
            first_line = fh.readline()
        assert (
            first_line == expected_header
        ), f"{file_path} header mismatch: expected '{expected_header.strip()}', got '{first_line.strip()}'."