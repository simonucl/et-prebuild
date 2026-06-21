# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student begins the assignment.  It verifies that:
#   • the three required source files exist with the expected contents;
#   • the /home/user/data directory is present;
#   • the /home/user/output directory either does not yet exist or, if it
#     already exists, that it does NOT yet contain the files the student
#     must create.
#
# No third-party libraries are used—only the Python stdlib and pytest.

import os
from pathlib import Path

import pytest


# ---------- Constants --------------------------------------------------------

DATA_DIR = Path("/home/user/data")
OUTPUT_DIR = Path("/home/user/output")

PEOPLE_FILE = DATA_DIR / "people.txt"
SALARIES_FILE = DATA_DIR / "salaries.txt"
ADDRESSES_FILE = DATA_DIR / "addresses.txt"

EMPLOYEE_REPORT_FILE = OUTPUT_DIR / "employee_report_2023.csv"
LOG_FILE = OUTPUT_DIR / "employee_report.log"

EXPECTED_PEOPLE = (
    "1,John,Doe,Engineering\n"
    "2,Jane,Smith,Marketing\n"
    "3,Bob,Johnson,Sales\n"
    "4,Alice,Williams,Engineering\n"
    "5,Mike,Brown,Support\n"
)

EXPECTED_SALARIES = (
    "1,90000,5000,2023\n"
    "2,80000,4000,2023\n"
    "3,75000,3000,2023\n"
    "4,95000,6000,2023\n"
    "5,60000,2000,2023\n"
)

EXPECTED_ADDRESSES = (
    "1,Seattle,WA,98101\n"
    "2,Portland,OR,97201\n"
    "3,San Francisco,CA,94105\n"
    "4,Boston,MA,02108\n"
    "5,Austin,TX,73301\n"
)


# ---------- Helper utilities -------------------------------------------------


def _read_file(path: Path) -> str:
    """Read a text file using UTF-8 and return its contents."""
    with path.open(encoding="utf-8") as fh:
        return fh.read()


# ---------- Tests ------------------------------------------------------------


def test_data_directory_exists():
    """Verify that /home/user/data exists and is a directory."""
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."


@pytest.mark.parametrize(
    "path_, expected_content",
    [
        (PEOPLE_FILE, EXPECTED_PEOPLE),
        (SALARIES_FILE, EXPECTED_SALARIES),
        (ADDRESSES_FILE, EXPECTED_ADDRESSES),
    ],
)
def test_source_files_exist_and_match_expected(path_: Path, expected_content: str):
    """Each source file must exist and contain exactly the expected lines."""
    assert path_.exists(), f"Source file {path_} is missing."
    assert path_.is_file(), f"{path_} exists but is not a regular file."

    actual = _read_file(path_)
    # We strip trailing newlines on both sides to avoid false negatives
    # if the file ends with or without a single trailing newline.
    assert actual.strip() == expected_content.strip(), (
        f"Contents of {path_} do not match expected data.\n"
        "Make sure no lines are missing, extra, or reordered."
    )


def test_output_files_do_not_yet_exist():
    """
    Before the student runs their solution, the output directory should *either*
    be absent or, if it already exists, it MUST NOT contain the target files.
    """
    if not OUTPUT_DIR.exists():
        # Directory does not exist yet: fine.
        return

    # If the directory exists, confirm it is a directory.
    assert OUTPUT_DIR.is_dir(), f"{OUTPUT_DIR} exists but is not a directory."

    # Neither the CSV report nor the log file should exist yet.
    assert not EMPLOYEE_REPORT_FILE.exists(), (
        f"{EMPLOYEE_REPORT_FILE} already exists—initial state must be clean."
    )
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists—initial state must be clean."
    )