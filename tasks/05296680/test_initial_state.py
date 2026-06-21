# test_initial_state.py
#
# Pytest suite to validate the **initial** operating-system / filesystem
# state for the “exoplanet re-organisation” exercise.
#
# This file makes sure that everything the student is supposed to start
# with is present **before** they run any commands and that nothing that
# the student is responsible for creating already exists.

import os
import stat
from pathlib import Path

import pytest

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------


def _assert_permissions(path: Path, expected_octal: int) -> None:
    """
    Assert that ``path`` has the exact permission bits ``expected_octal``.

    Parameters
    ----------
    path : pathlib.Path
        Path to the file or directory whose permissions we are checking.
    expected_octal : int
        E.g. 0o644 or 0o755.
    """
    actual = stat.S_IMODE(path.stat().st_mode)
    assert actual == expected_octal, (
        f"Permissions for {path} are {oct(actual)}, "
        f"but expected {oct(expected_octal)}."
    )


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

DATA_DIR = Path("/home/user/data")
CSV_FILE = DATA_DIR / "exoplanets.csv"
OUTPUT_DIR = Path("/home/user/output")


def test_data_directory_exists_and_permissions():
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} does not exist."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."
    _assert_permissions(DATA_DIR, 0o755)


def test_output_directory_exists_and_is_empty_with_permissions():
    assert OUTPUT_DIR.exists(), f"Required directory {OUTPUT_DIR} does not exist."
    assert OUTPUT_DIR.is_dir(), f"{OUTPUT_DIR} exists but is not a directory."
    _assert_permissions(OUTPUT_DIR, 0o755)

    extra_contents = list(OUTPUT_DIR.iterdir())
    assert (
        len(extra_contents) == 0
    ), f"{OUTPUT_DIR} should be empty initially, but contains: {extra_contents!r}"


def test_exoplanets_csv_exists_permissions_and_exact_content():
    # --- Existence & permissions ------------------------------------------------
    assert CSV_FILE.exists(), f"Required CSV file {CSV_FILE} does not exist."
    assert CSV_FILE.is_file(), f"{CSV_FILE} exists but is not a regular file."
    _assert_permissions(CSV_FILE, 0o644)

    # --- Exact file content -----------------------------------------------------
    expected_content = (
        "pl_name,hostname,disc_year,discoverymethod,pl_orbper\n"
        "\"Kepler-22 b\",\"Kepler-22\",2011,Transit,289.8623\n"
        "\"HD 209458 b\",\"HD 209458\",1999,Transit,3.5247\n"
        "\"51 Pegasi b\",\"51 Pegasi\",1995,Radial Velocity,4.2308\n"
        "\"Kepler-10 c\",\"Kepler-10\",2011,Transit,45.2943\n"
        "\"GJ 1214 b\",\"GJ 1214\",2009,Transit,1.5804\n"
    )

    with CSV_FILE.open("r", encoding="utf-8", newline="") as fh:
        actual_content = fh.read()

    assert (
        actual_content == expected_content
    ), "Content of exoplanets.csv does not match the expected initial dataset."


def test_number_of_transit_rows_is_exactly_four():
    """
    Sanity check: the CSV should contain exactly four rows whose
    discoverymethod column is 'Transit'.  This guards against the file
    being silently modified.
    """
    with CSV_FILE.open("r", encoding="utf-8", newline="") as fh:
        lines = fh.read().splitlines()

    # Skip header row
    data_rows = lines[1:]

    transit_rows = [
        row for row in data_rows if row.split(",")[3] == "Transit"
    ]

    assert len(transit_rows) == 4, (
        "The initial CSV should contain exactly 4 rows with "
        "discoverymethod == 'Transit', but found "
        f"{len(transit_rows)}."
    )