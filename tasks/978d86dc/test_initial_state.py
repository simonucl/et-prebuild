# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state
# before the student starts working on the “messy survey
# data” task.  It purposefully checks only the prerequisites
# and explicitly asserts that none of the deliverables
# created during the task exist yet.
#
# The tests rely solely on Python’s standard library + pytest.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
DATA_DIR = HOME / "data"

RAW_FILE      = DATA_DIR / "raw_survey.txt"
CLEAN_FILE    = DATA_DIR / "clean_survey.csv"
STATS_FILE    = DATA_DIR / "income_stats.txt"
PROCESS_LOG   = DATA_DIR / "process.log"

EXPECTED_RAW_LINES = [
    "Name | Age | Country | Income",
    "Alice   | 29 | usa | 70000",
    "Bob|34| Canada | 82000",
    "   Charlie | NA | UK | NA",
    "Diana| 42|usa|90000",
    "Eve |27|Germany| 65000",
    "Frank | 31 | USA | 72000",
    "Grace| 25|  Canada|68000",
    "Heidi|38|UK | NA",
    "Ivan | 45 | germany| 87000",
    "Judy|30|USA| 75000",
]

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def read_text_no_cr(path: pathlib.Path) -> str:
    """
    Read a file as text and assert that it contains *no* carriage returns,
    returning the raw contents for further inspection.
    """
    raw_bytes = path.read_bytes()
    assert b"\r" not in raw_bytes, (
        f"{path} must use Unix LF newlines only (no CR characters)."
    )
    return raw_bytes.decode("utf-8", errors="strict")

# ---------------------------------------------------------------------------
# Actual tests
# ---------------------------------------------------------------------------

def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} does not exist. "
        "It should be present because the raw survey file lives inside it."
    )

def test_raw_file_presence_and_contents():
    # ---------- presence ----------
    assert RAW_FILE.is_file(), (
        f"The raw survey file is expected at {RAW_FILE} but was not found."
    )

    # ---------- newline mode + basic sanity ----------
    content = read_text_no_cr(RAW_FILE)

    # ---------- exact line-by-line comparison ----------
    observed_lines = content.split("\n")
    # If the file ends with a newline, .split will add a trailing empty string;
    # strip it off for comparison purposes.
    if observed_lines and observed_lines[-1] == "":
        observed_lines.pop()

    assert observed_lines == EXPECTED_RAW_LINES, (
        "The contents of the raw survey file do not match the fixture that "
        "should be supplied to the student.  Any deviation here means the "
        "starting data are wrong.\n\n"
        "---- expected ----\n"
        + "\n".join(EXPECTED_RAW_LINES)
        + "\n---- observed ----\n"
        + "\n".join(observed_lines)
        + "\n------------------"
    )

    # ---------- basic counting assertions ----------
    # 1 header + 10 data rows = 11 total non-blank lines
    assert len(observed_lines) == 11, (
        f"The raw file should contain 11 non-blank lines (1 header + 10 "
        f"records) but contains {len(observed_lines)}."
    )

def test_output_files_do_not_exist_yet():
    """
    At the very start, none of the artefacts that the student must generate
    should be present.  Their presence would mean previous work polluted the
    environment.
    """
    for path in (CLEAN_FILE, STATS_FILE, PROCESS_LOG):
        assert not path.exists(), (
            f"Output artefact {path} already exists, but the initial state "
            "should be clean.  Remove the file before starting the task."
        )