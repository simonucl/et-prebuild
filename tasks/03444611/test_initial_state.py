# test_initial_state.py
#
# This pytest file validates the *initial* operating-system / filesystem
# state before the student begins working on the task.  It makes sure that
# only the starter CSV file is present and that none of the final output
# artefacts have been created yet.
#
# Requirements verified:
#   • /home/user/project            → directory exists
#   • /home/user/project/raw_sales.csv
#       - file exists
#       - contains exactly the 11 expected lines
#       - every line contains **exactly 6 commas** (7 columns)
#   • None of the target output files are present yet
#
# The tests rely on stdlib only.

import os
import pathlib
import pytest

PROJECT_DIR = pathlib.Path("/home/user/project").resolve()
RAW_CSV      = PROJECT_DIR / "raw_sales.csv"

OUTPUT_FILES = [
    PROJECT_DIR / "salesdata.json",
    PROJECT_DIR / "sales_schema.json",
    PROJECT_DIR / "sales_validation.log",
    PROJECT_DIR / "high_value_sales.json",
    PROJECT_DIR / "sales_summary.log",
]

# --------------------------------------------------------------------------- #
# Helper data                                                                 #
# --------------------------------------------------------------------------- #

EXPECTED_CSV_LINES = [
    "Date,Region,Rep,Item,Units,Unit Cost,Total",
    "2023-07-01,East,Jones,Pencil,95,1.99,189.05",
    "2023-07-02,West,Kivell,Binder,50,19.99,999.50",
    "2023-07-03,East,Jardine,Pencil,36,4.99,179.64",
    "2023-07-04,East,Gill,Pen,27,19.99,539.73",
    "2023-07-05,Central,Sorvino,Pencil,56,2.99,167.44",
    "2023-07-06,East,Jones,Binder,60,4.99,299.40",
    "2023-07-07,West,Andrews,Pencil,75,1.99,149.25",
    "2023-07-08,Central,Jardine,Pen Set,90,15.99,1439.10",
    "2023-07-09,Central,Thompson,Binder,32,4.99,159.68",
    "2023-07-10,East,Jones,Pencil,65,4.99,324.35",
]

# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), (
        f"Expected directory {PROJECT_DIR} to exist, "
        "but it was not found. Make sure the project directory is present."
    )

def test_raw_sales_csv_exists():
    assert RAW_CSV.is_file(), (
        f"Starter CSV file not found at {RAW_CSV}. "
        "The exercise requires this file to be supplied before any work begins."
    )

def test_raw_sales_csv_contents():
    """Check exact line content and structure of raw_sales.csv."""
    with RAW_CSV.open("r", encoding="utf-8") as fh:
        lines = [line.rstrip("\n\r") for line in fh]

    assert lines == EXPECTED_CSV_LINES, (
        "The contents of raw_sales.csv do not match the expected starter data.\n"
        "Differences:\n"
        f"Expected ({len(EXPECTED_CSV_LINES)} lines):\n"
        + "\n".join(EXPECTED_CSV_LINES) + "\n\n"
        f"Found ({len(lines)} lines):\n"
        + "\n".join(lines)
    )

    # Additional structural check: each line must have exactly 6 commas (7 fields).
    bad_lines = [
        (idx + 1, l) for idx, l in enumerate(lines) if l.count(",") != 6
    ]
    assert not bad_lines, (
        "All lines in raw_sales.csv must contain exactly 6 commas "
        "(7 comma-separated fields). Offending lines:\n"
        + "\n".join(f"Line {ln}: '{text}'" for ln, text in bad_lines)
    )

@pytest.mark.parametrize("path", OUTPUT_FILES)
def test_no_output_files_yet(path):
    assert not path.exists(), (
        f"Output file {path} already exists, but the student has not yet "
        "performed the task. The workspace should only contain raw_sales.csv "
        "at this point."
    )