# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must
# be present before the student begins working on the task.  It checks
# only the pre-existing artefacts that the instructions guarantee.
#
# IMPORTANT:  We deliberately do *not* test for any files or directories
# that the student is expected to create (e.g. /home/user/output,
# /home/user/network, /home/user/logs), because they must not exist yet.

import os
from pathlib import Path
import csv
import pytest

DATA_DIR = Path("/home/user/data")
Q1_FILE = DATA_DIR / "sales_q1.csv"
Q2_FILE = DATA_DIR / "sales_q2.csv"

# Ground-truth contents -----------------------------------------------
Q1_EXPECTED_LINES = [
    "date,product,units_sold,unit_price",
    "2023-01-05,Widget,10,25.00",
    "2023-02-10,Gadget,5,15.00",
    "2023-03-15,Widget,20,25.00",
    "2023-03-18,Doodad,7,12.50",
]

Q2_EXPECTED_LINES = [
    "date,product,units_sold,unit_price",
    "2023-04-02,Gadget,8,15.00",
    "2023-04-10,Widget,15,25.00",
    "2023-05-12,Doodad,10,12.50",
    "2023-06-22,Widget,5,25.00",
]


# Utility --------------------------------------------------------------

def read_csv_lines(path: Path):
    """
    Return a list of lines (without trailing newlines) from the CSV file.
    """
    with path.open("r", encoding="utf-8") as fh:
        # Strip only the final newline character(s) from each line
        return [line.rstrip("\r\n") for line in fh.readlines()]


# Tests ----------------------------------------------------------------

def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} is missing. "
        "The test environment must provide the CSV source files here."
    )


@pytest.mark.parametrize(
    "csv_file, expected_lines",
    [
        (Q1_FILE, Q1_EXPECTED_LINES),
        (Q2_FILE, Q2_EXPECTED_LINES),
    ],
)
def test_csv_file_exists(csv_file, expected_lines):
    assert csv_file.is_file(), (
        f"Expected CSV file {csv_file} is missing."
    )
    # Basic sanity: file must not be empty
    assert csv_file.stat().st_size > 0, (
        f"CSV file {csv_file} is empty."
    )

    lines = read_csv_lines(csv_file)

    # Check the exact number of lines
    assert len(lines) == len(expected_lines), (
        f"{csv_file} should have {len(expected_lines)} lines "
        f"(header plus data) but has {len(lines)}."
    )

    # Check each line exactly
    for idx, (got, exp) in enumerate(zip(lines, expected_lines), start=1):
        assert got == exp, (
            f"Line {idx} in {csv_file} differs from expected.\n"
            f"  Expected: {exp!r}\n"
            f"  Found:    {got!r}"
        )

    # Structural validation: each line must have exactly 4 comma-separated columns
    for idx, row in enumerate(lines, start=1):
        cols = row.split(",")
        assert len(cols) == 4, (
            f"Line {idx} in {csv_file} should have 4 comma-separated values "
            f"but has {len(cols)}: {row!r}"
        )


def test_no_unexpected_output_directories():
    """
    Ensure that directories intended to be created *by the student* do NOT
    already exist. Their prior existence would invalidate the initial state.
    """
    forbidden_dirs = [
        Path("/home/user/output"),
        Path("/home/user/network"),
        Path("/home/user/logs"),
    ]
    preexisting = [str(p) for p in forbidden_dirs if p.exists()]
    assert not preexisting, (
        "The following directories already exist but should not be present "
        "before the task starts:\n  " + "\n  ".join(preexisting)
    )