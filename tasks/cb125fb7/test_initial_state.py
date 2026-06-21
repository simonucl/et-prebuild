# test_initial_state.py
#
# This pytest suite verifies the PRE-TASK state of the operating system /
# filesystem for the “sales aggregation” exercise.  It checks that
#
#   • the three source CSV files exist at their absolute paths and contain the
#     exact expected text (including new-line characters),
#   • the output directory exists and is writable, and
#   • none of the files that the student is supposed to create later
#     (/home/user/output/aggregated_sales.csv and
#     /home/user/output/runtime_comparison.log) are present yet.
#
# Only Python’s stdlib and pytest are used.

from pathlib import Path
import os
import stat
import pytest

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
OUTPUT_DIR = HOME / "output"

Q1_PATH = DATA_DIR / "sales_q1.csv"
Q2_PATH = DATA_DIR / "sales_q2.csv"
Q3_PATH = DATA_DIR / "sales_q3.csv"

AGG_OUTPUT = OUTPUT_DIR / "aggregated_sales.csv"
LOG_OUTPUT = OUTPUT_DIR / "runtime_comparison.log"

# --------------------------------------------------------------------------- #
# Expected contents of the three pre-existing CSV files.
# Note the *trailing* newline on every single line, including the last one.

EXPECTED_Q1 = (
    "Region,Product,Units,UnitPrice\n"
    "North,Widget,10,20.5\n"
    "South,Gadget,5,15\n"
    "East,Widget,7,20.5\n"
    "North,Gadget,3,15\n"
)

EXPECTED_Q2 = (
    "Region,Product,Units,UnitPrice\n"
    "South,Widget,8,20.5\n"
    "East,Gadget,6,15\n"
    "West,Widget,4,20.5\n"
    "North,Widget,11,20.5\n"
)

EXPECTED_Q3 = (
    "Region,Product,Units,UnitPrice\n"
    "East,Widget,9,20.5\n"
    "South,Gadget,2,15\n"
    "West,Gadget,5,15\n"
    "North,Gadget,7,15\n"
)

@pytest.mark.parametrize(
    "path, expected",
    [
        (Q1_PATH, EXPECTED_Q1),
        (Q2_PATH, EXPECTED_Q2),
        (Q3_PATH, EXPECTED_Q3),
    ],
)
def test_source_csv_files_exist_and_match_expected_content(path: Path, expected: str):
    """
    Verify that each required source CSV exists and its byte-for-byte
    contents exactly match the specification.
    """
    assert path.is_file(), (
        f"Required data file is missing: {path}"
    )

    actual = path.read_text(encoding="utf-8")
    assert actual == expected, (
        f"Contents of {path} differ from the expected specification.\n"
        f"--- Expected (showing repr) ---\n{repr(expected)}\n"
        f"---   Actual (showing repr)  ---\n{repr(actual)}\n"
        "Make sure every line (including the final one) ends with a single LF."
    )


def test_output_directory_exists_and_is_writable():
    """
    The directory /home/user/output/ must already exist and be writable
    by the current user.
    """
    assert OUTPUT_DIR.exists(), "Output directory /home/user/output/ is missing."
    assert OUTPUT_DIR.is_dir(), "/home/user/output/ exists but is not a directory."

    # Check writability: user must have the write bit OR we can actually create a
    # file in a tmp path inside the directory.  The simpler permission check is
    # sufficient and does not leave any artefacts.
    mode = OUTPUT_DIR.stat().st_mode
    writable = bool(mode & stat.S_IWUSR)
    assert writable, "/home/user/output/ exists but is not writable by the current user."


@pytest.mark.parametrize("path", [AGG_OUTPUT, LOG_OUTPUT])
def test_output_files_do_not_exist_yet(path: Path):
    """
    Before the student starts, the two deliverable files must NOT exist.
    Their presence would indicate that the initial state is polluted.
    """
    assert not path.exists(), (
        f"Output file {path} already exists before the task has begun. "
        "The workspace must start without this file."
    )