# test_initial_state.py
"""
Pytest suite that verifies the EXPECTED *initial* state of the filesystem
before the student writes the Makefile or runs `make`.

The checks intentionally fail fast with explicit error messages so that a
student immediately knows what prerequisite is missing or has been modified.

The reference directory is:
    /home/user/data_science_project
"""
import os
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/data_science_project")
RAW_DIR = BASE_DIR / "raw_data"
CLEANED_DIR = BASE_DIR / "cleaned_data"
STATS_DIR = BASE_DIR / "stats"
MAKEFILE = BASE_DIR / "Makefile"
RUN_LOG = BASE_DIR / "run.log"

# --------------------------------------------------------------------------- #
# Expected *exact* contents of the two raw CSV files supplied at start-up.
# --------------------------------------------------------------------------- #
Q1_EXPECTED = (
    "id,product,units\n"
    "1,Widget,10\n"
    "2,Gadget,\n"
    "3,Thingamajig,5\n"
)

Q2_EXPECTED = (
    "id,product,units\n"
    "4,Widget,7\n"
    "5,Gadget,3\n"
    "6,Thingamajig,\n"
)


# -----------------------------  Helper utils  ------------------------------ #
def _read_text(path: Path) -> str:
    """
    Read a text file exactly as-is (no newline conversions).  Fail with a clear
    message if the file is missing.
    """
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Expected file not found: {path}")


# ---------------------------  Individual tests  ---------------------------- #
def test_base_directory_exists():
    assert BASE_DIR.is_dir(), f"Base directory is missing: {BASE_DIR}"


def test_raw_data_directory_and_files_exist():
    assert RAW_DIR.is_dir(), f"Missing directory: {RAW_DIR}"

    q1 = RAW_DIR / "sales_q1.csv"
    q2 = RAW_DIR / "sales_q2.csv"
    for path in (q1, q2):
        assert path.is_file(), f"Missing raw CSV file: {path}"

    # Exact content verification (needed so that later tests can rely on it).
    assert _read_text(q1) == Q1_EXPECTED, (
        f"Contents of {q1} do not match the expected initial data."
    )
    assert _read_text(q2) == Q2_EXPECTED, (
        f"Contents of {q2} do not match the expected initial data."
    )


def test_makefile_not_yet_present():
    assert not MAKEFILE.exists(), (
        f"{MAKEFILE} should NOT exist before the task is attempted."
    )


def test_cleaned_and_stats_directories_absent():
    for dir_path in (CLEANED_DIR, STATS_DIR):
        assert not dir_path.exists(), (
            f"{dir_path} should NOT exist in the initial state."
        )


def test_run_log_absent():
    assert not RUN_LOG.exists(), (
        f"{RUN_LOG} should NOT exist before any Makefile target is run."
    )