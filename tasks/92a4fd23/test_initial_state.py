# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system / filesystem
# state before the learner performs any action for the “customers.csv”
# cleaning task.
#
# Rules enforced:
# 1. The raw CSV must already exist and contain the expected 4 data rows
#    plus header, exactly as specified.
# 2. No processed artefacts or even the processed directory may exist yet.
#
# Any deviation from these expectations will cause the tests to fail with a
# clear, actionable message.

import os
from pathlib import Path

RAW_FILE = Path("/home/user/data/raw/customers.csv")
PROCESSED_DIR = Path("/home/user/data/processed")
CLEAN_FILE = PROCESSED_DIR / "customers_clean.csv"
LOG_FILE = PROCESSED_DIR / "transform.log"


def test_raw_csv_exists():
    """The raw customers.csv must be present before any processing starts."""
    assert RAW_FILE.is_file(), (
        f"Expected raw input file {RAW_FILE} is missing.\n"
        "Make sure the initial dataset is placed exactly at that path."
    )


def test_raw_csv_content():
    """Verify the exact, line-by-line content of the raw input CSV."""
    expected_lines = [
        "id,name,age,country\n",
        "1,Alice,31,US\n",
        "2,Bob,25,CA\n",
        "3,Charlie,35,UK\n",
        "4,David,28,US\n",
    ]

    with RAW_FILE.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == expected_lines, (
        "The content of the raw CSV does not match the expected initial state.\n"
        "Expected:\n"
        + "".join(expected_lines)
        + "\nGot:\n"
        + "".join(actual_lines)
    )


def test_no_processed_directory_yet():
    """
    The processed directory (and therefore any output files) must NOT
    exist before the learner runs their solution.
    """
    assert not PROCESSED_DIR.exists(), (
        f"Directory {PROCESSED_DIR} should not exist yet. "
        "The learner's code is responsible for creating it."
    )


def test_no_output_files_present():
    """
    Ensure the final artefacts do not pre-exist. If the processed directory
    happens to exist for any reason, the specific output files must still
    be absent so the grader can detect newly generated results.
    """
    assert not CLEAN_FILE.exists(), f"Output file {CLEAN_FILE} already exists; it must be created by the learner."
    assert not LOG_FILE.exists(), f"Log file {LOG_FILE} already exists; it must be created by the learner."