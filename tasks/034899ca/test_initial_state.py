# test_initial_state.py
#
# Pytest suite that validates the expected, pre-exercise filesystem
# state for the “SSN leak” assignment.  These tests make sure the
# reference CSV is present and well-formed *before* the student
# creates any new directories or files.
#
# IMPORTANT:  The instructions explicitly forbid checking for any
#             output artefacts, so this file **only** inspects
#             the original dataset shipped with the exercise.

import os
import re
from pathlib import Path

import pytest

# Absolute path to the canonical dataset that must already exist.
EMPLOYEES_CSV = Path("/home/user/datasets/employees.csv")

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

SSN_REGEX = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")


def _read_csv_lines():
    """Read the CSV file and return a list of stripped lines."""
    with EMPLOYEES_CSV.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_employees_csv_exists():
    """The employees.csv file must be present and be a regular file."""
    assert EMPLOYEES_CSV.is_file(), (
        f"Required dataset not found at '{EMPLOYEES_CSV}'. "
        "Verify that the file exists before starting the exercise."
    )


def test_employees_csv_not_empty():
    """The dataset must not be empty so that the scan is meaningful."""
    size = EMPLOYEES_CSV.stat().st_size
    assert size > 0, (
        f"Dataset '{EMPLOYEES_CSV}' is empty (0 bytes); "
        "cannot proceed with SSN scan."
    )


def test_employees_csv_header():
    """The header row must match the documented schema exactly."""
    lines = _read_csv_lines()
    assert lines, f"Dataset '{EMPLOYEES_CSV}' contains no lines."
    expected_header = "Name,Email,SSN,Phone,Salary"
    assert lines[0] == expected_header, (
        "CSV header mismatch.\n"
        f"Expected: '{expected_header}'\n"
        f"Found   : '{lines[0]}'"
    )


def test_employees_csv_contains_ssn_rows():
    """
    The input file should contain at least one SSN so that students
    have something to match against.
    """
    lines = _read_csv_lines()
    data_rows = lines[1:]  # skip header
    matches = [row for row in data_rows if SSN_REGEX.search(row)]
    assert matches, (
        f"No SSN pattern (###-##-####) found in '{EMPLOYEES_CSV}'. "
        "The sample must include at least one SSN to make the task viable."
    )