# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / file-system
# state for the “East-region product sales summary” exercise.
#
# The tests make sure that:
#   • The required directories exist (/home/user/data and /home/user/output).
#   • The data directory contains **exactly** the two expected CSV files.
#   • Each CSV file’s contents match the specification (line-for-line, LF endings).
#   • The output directory exists, is writable, and is completely empty.
#
# No tests are written for any output artefacts, because those should not exist
# before the student runs their solution.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
OUTPUT_DIR = HOME / "output"

# --------------------------------------------------------------------------- #
# Helpers & fixtures
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="module")
def expected_q1_content():
    """
    Exact content expected for /home/user/data/sales_q1.csv (including LF
    line endings and the trailing newline after the final row).
    """
    return (
        "Region,Product,Sales\n"
        "East,Gadget,1200\n"
        "West,Widget,800\n"
        "East,Widget,950\n"
        "North,Gadget,620\n"
        "East,Doohickey,300\n"
    )


@pytest.fixture(scope="module")
def expected_q2_content():
    """
    Exact content expected for /home/user/data/sales_q2.csv (including LF
    line endings and the trailing newline after the final row).
    """
    return (
        "Region,Product,Sales\n"
        "South,Gadget,730\n"
        "East,Gadget,660\n"
        "West,Doohickey,410\n"
        "East,Widget,540\n"
        "East,Doohickey,200\n"
    )


# --------------------------------------------------------------------------- #
# Directory structure tests
# --------------------------------------------------------------------------- #

def test_data_directory_exists():
    assert DATA_DIR.exists() and DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} is missing or is not a directory."
    )


def test_output_directory_exists_and_writable():
    assert OUTPUT_DIR.exists() and OUTPUT_DIR.is_dir(), (
        f"Required directory {OUTPUT_DIR} is missing or is not a directory."
    )

    is_writable = os.access(OUTPUT_DIR, os.W_OK)
    assert is_writable, f"Directory {OUTPUT_DIR} exists but is not writable."


def test_output_directory_is_empty():
    leftover_items = [p for p in OUTPUT_DIR.iterdir()]
    assert not leftover_items, (
        f"Directory {OUTPUT_DIR} must be empty at the start, "
        f"but found: {', '.join(str(p) for p in leftover_items)}"
    )


# --------------------------------------------------------------------------- #
# File presence tests
# --------------------------------------------------------------------------- #

def test_data_directory_contains_only_expected_csv_files():
    expected_files = {
        DATA_DIR / "sales_q1.csv",
        DATA_DIR / "sales_q2.csv",
    }
    actual_files = {p for p in DATA_DIR.iterdir() if p.is_file()}

    assert actual_files == expected_files, (
        "The /home/user/data directory must contain exactly the two CSV files:\n"
        f"  {', '.join(str(p) for p in sorted(expected_files))}\n"
        f"Found instead:\n"
        f"  {', '.join(str(p) for p in sorted(actual_files))}"
    )


# --------------------------------------------------------------------------- #
# File content tests
# --------------------------------------------------------------------------- #

def _assert_file_content(path: Path, expected: str):
    assert path.is_file(), f"Expected file {path} is missing."

    actual_content = path.read_text(encoding="utf-8")
    assert actual_content == expected, (
        f"Contents of {path} do not match the specification.\n"
        "---- Expected ----\n"
        f"{expected}\n"
        "---- Actual ----\n"
        f"{actual_content}"
    )


def test_sales_q1_content(expected_q1_content):
    q1_path = DATA_DIR / "sales_q1.csv"
    _assert_file_content(q1_path, expected_q1_content)


def test_sales_q2_content(expected_q2_content):
    q2_path = DATA_DIR / "sales_q2.csv"
    _assert_file_content(q2_path, expected_q2_content)