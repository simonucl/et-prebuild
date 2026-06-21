# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state *before* the student performs any actions for the “quarterly_rollup”
# workflow exercise.
#
# The tests confirm that:
#   1.  The required source CSV files already exist and contain the exact
#      expected content (including final newlines).
#   2.  The target output directory and its artefacts do **not** exist yet.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Constant paths
# ---------------------------------------------------------------------------
HOME = Path("/home/user")

SOURCE_DIR = HOME / "source_data"
Q1_CSV = SOURCE_DIR / "sales_q1.csv"
Q2_CSV = SOURCE_DIR / "sales_q2.csv"

WORKFLOWS_DIR = HOME / "workflows"
OUTPUT_DIR = WORKFLOWS_DIR / "quarterly_rollup"
MERGED_CSV = OUTPUT_DIR / "merged_sales.csv"
PROCESS_LOG = OUTPUT_DIR / "process.log"


# ---------------------------------------------------------------------------
# Expected contents of the initial source CSV files
# (each line ends with a newline)
# ---------------------------------------------------------------------------
EXPECTED_Q1 = (
    "Date,Region,Product,Units,Revenue\n"
    "2024-01-10,North,Widget,120,2400\n"
    "2024-02-12,South,Gadget,85,1700\n"
    "2024-03-08,East,Thingamajig,60,1200\n"
)

EXPECTED_Q2 = (
    "Date,Region,Product,Units,Revenue\n"
    "2024-04-11,North,Widget,130,2600\n"
    "2024-05-15,South,Gadget,90,1800\n"
    "2024-06-18,East,Thingamabob,70,1400\n"
)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def read_text(path: Path) -> str:
    """Return the full text of a file, raising an explicit assertion
    if the file cannot be read for any reason."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Required file is missing: {path}")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_source_files_exist_with_correct_content():
    """Verify that the two source CSV files are present and exactly match
    the expected starter data."""
    # --- Q1 CSV checks ------------------------------------------------------
    assert Q1_CSV.is_file(), (
        f"Missing source file: {Q1_CSV}. "
        "The exercise requires this file to be present before you begin."
    )
    q1_text = read_text(Q1_CSV)
    assert (
        q1_text == EXPECTED_Q1
    ), f"Content mismatch in {Q1_CSV}. Expected:\n{EXPECTED_Q1!r}\nGot:\n{q1_text!r}"

    # --- Q2 CSV checks ------------------------------------------------------
    assert Q2_CSV.is_file(), (
        f"Missing source file: {Q2_CSV}. "
        "The exercise requires this file to be present before you begin."
    )
    q2_text = read_text(Q2_CSV)
    assert (
        q2_text == EXPECTED_Q2
    ), f"Content mismatch in {Q2_CSV}. Expected:\n{EXPECTED_Q2!r}\nGot:\n{q2_text!r}"


def test_output_directory_absent():
    """Ensure the workflow output directory and its artefacts are **not**
    present yet.  Students must create them as part of the exercise."""
    assert not OUTPUT_DIR.exists(), (
        f"The directory {OUTPUT_DIR} already exists, but it should not be "
        "present before you start the exercise."
    )

    # Even if the directory does not exist, double-check that individual
    # files do not exist (in case someone created them elsewhere).
    assert not MERGED_CSV.exists(), (
        f"The file {MERGED_CSV} already exists, but it should not be "
        "present before you start the exercise."
    )
    assert not PROCESS_LOG.exists(), (
        f"The file {PROCESS_LOG} already exists, but it should not be "
        "present before you start the exercise."
    )