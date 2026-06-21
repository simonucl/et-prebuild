# test_initial_state.py
#
# This test-suite validates that the container starts in the expected,
# pristine state **before** the student executes any commands.
#
# IMPORTANT:
# * Do NOT add tests that look for any files that the student is
#   expected to create (e.g. optimization.log).
# * We purposefully only assert on the *input* area
#   (/home/user/db/queries/…) and its contents.

import os
import time
from datetime import datetime, timedelta

import pytest

BASE_DIR = "/home/user/db"
QUERIES_DIR = os.path.join(BASE_DIR, "queries")

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def read_lines(path):
    """Return a list of lines stripped from their trailing newline."""
    with open(path, "r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


# ----------------------------------------------------------------------
# Data that represents the canonical, pristine state.
# ----------------------------------------------------------------------

EXPECTED_FILES = {
    os.path.join(QUERIES_DIR, "daily", "report.sql"): [
        "/* daily report */",
        "SELECT * FROM sales;",
        "LIMIT 100;",
    ],
    os.path.join(QUERIES_DIR, "archive", "old_report.sql"): [
        "/* archived report */",
        "SELECT * FROM sales;",
    ],
    os.path.join(QUERIES_DIR, "maintenance", "cleanup.sql"): [
        "/* maintenance task */",
        "DELETE FROM logs WHERE date < NOW() - INTERVAL '30 days';",
    ],
}

# Only the daily report should be considered "recent"
RECENT_PATH = os.path.join(QUERIES_DIR, "daily", "report.sql")
DAYS_7_AGO = time.time() - 7 * 24 * 60 * 60  # seconds


# ----------------------------------------------------------------------
# Actual tests
# ----------------------------------------------------------------------


def test_directory_structure_exists():
    """Verify that the base directories exist."""
    assert os.path.isdir(BASE_DIR), f"Expected directory {BASE_DIR} to exist."
    assert os.path.isdir(
        QUERIES_DIR
    ), f"Expected directory {QUERIES_DIR} to exist."


@pytest.mark.parametrize("path,expected_lines", list(EXPECTED_FILES.items()))
def test_file_exists_with_correct_content(path, expected_lines):
    """Every expected .sql file must exist with the exact initial content."""
    assert os.path.isfile(path), f"Expected file {path} to exist."

    lines = read_lines(path)
    assert (
        lines == expected_lines
    ), f"File {path} has unexpected content.\nExpected: {expected_lines!r}\nFound:    {lines!r}"


def test_only_expected_sql_files_present():
    """
    There must be exactly the three known .sql files under /home/user/db/queries.
    This guards against extra pre-existing files that could interfere with the
    grading logic.
    """
    discovered_sql_files = []
    for root, _, files in os.walk(QUERIES_DIR):
        for fname in files:
            if fname.endswith(".sql"):
                discovered_sql_files.append(os.path.join(root, fname))

    missing = set(EXPECTED_FILES) - set(discovered_sql_files)
    extra = set(discovered_sql_files) - set(EXPECTED_FILES)

    assert (
        not missing
    ), f"The following expected .sql files are missing: {', '.join(sorted(missing))}"
    assert (
        not extra
    ), f"Unexpected .sql files found before the task starts: {', '.join(sorted(extra))}"


def test_file_timestamps():
    """
    Exactly one file — the daily report — must be 'recent' (mtime within 7 days),
    while the others must be older.  This precondition is essential because the
    grading logic relies on modification dates.
    """
    for path in EXPECTED_FILES:
        mtime = os.path.getmtime(path)
        is_recent = mtime >= DAYS_7_AGO
        if path == RECENT_PATH:
            assert (
                is_recent
            ), f"Expected {path} to have a modification time within the last 7 days."
        else:
            assert (
                not is_recent
            ), f"Expected {path} to be older than 7 days (mtime={datetime.fromtimestamp(mtime)!s})."