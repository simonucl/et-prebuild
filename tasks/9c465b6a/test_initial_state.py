# test_initial_state.py
#
# This test-suite validates the **initial** operating-system / filesystem
# state before the student performs any action.
#
# It checks only the *pre-existing* raw data; it **does not** touch or
# reference any of the expected output files or directories.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RAW_DIR = Path("/home/user/data/raw")
RAW_FILE = RAW_DIR / "user_events.tsv"

EXPECTED_LINES = [
    "user_id\tevent_type\ttimestamp",
    "u01\tclick\t2023-05-01T10:00:00Z",
    "u02\tview\t2023-05-01T10:02:00Z",
    "u01\tclick\t2023-05-01T10:00:00Z",
    "u03\tpurchase\t2023-05-01T10:05:00Z",
    "u02\tview\t2023-05-01T10:02:00Z",
    "u04\tclick\t2023-05-01T10:10:00Z",
    "u02\tclick\t2023-05-01T10:12:00Z",
    "u03\tview\t2023-05-01T10:15:00Z",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_tsv_lines(path: Path):
    """Return the file content as a list of stripped lines (no newline char)."""
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_raw_directory_exists():
    """Verify that /home/user/data/raw exists and is a directory."""
    assert RAW_DIR.exists(), f"Required directory {RAW_DIR} is missing."
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."


def test_raw_file_exists():
    """Verify that /home/user/data/raw/user_events.tsv exists."""
    assert RAW_FILE.exists(), f"Required file {RAW_FILE} is missing."
    assert RAW_FILE.is_file(), f"{RAW_FILE} exists but is not a regular file."


def test_raw_file_content_exact_match():
    """
    Verify that the raw file has exactly the expected 9 lines (header + 8 data)
    and that each line matches the truth provided in the task description.
    """
    lines = _read_tsv_lines(RAW_FILE)
    assert len(lines) == 9, (
        f"{RAW_FILE} should contain 9 lines (1 header + 8 data), "
        f"but {len(lines)} lines were found."
    )
    assert lines == EXPECTED_LINES, (
        f"Content of {RAW_FILE} does not match the expected truth.\n"
        "First mismatch (if any) will be shown below:\n"
        f"Expected: {EXPECTED_LINES}\n"
        f"Found   : {lines}"
    )


def test_raw_file_is_tab_separated_and_has_three_columns():
    """Ensure each line in the TSV file contains exactly three tab-separated fields."""
    lines = _read_tsv_lines(RAW_FILE)
    for idx, line in enumerate(lines, start=1):
        cols = line.split("\t")
        assert len(cols) == 3, (
            f"Line {idx} in {RAW_FILE} should have exactly 3 tab-separated columns, "
            f"but it has {len(cols)}. Line content: {line!r}"
        )