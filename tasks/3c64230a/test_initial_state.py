# test_initial_state.py
#
# This pytest suite validates that the *starting* filesystem and tooling
# are in the correct shape *before* the student begins any work.  It
# checks only the artefacts that must already exist or be available.
#
# IMPORTANT:
#   • We explicitly do **not** test for any of the output files or
#     directories that the student is expected to create.
#   • Only stdlib and pytest are used.

import csv
import shutil
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
HOME = Path("/home/user")
RAW_CSV = HOME / "data" / "raw_reviews.csv"
EXPECTED_HEADER = ["review_id", "product_id", "sentiment", "review_text"]
EXPECTED_ROW_COUNT = 6


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def _read_csv_rows(path: Path):
    """Read the CSV and return header list + list of rows (as dicts)."""
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        rows = list(reader)
    return header, rows


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_raw_reviews_csv_exists():
    """The starting CSV file must be present at the exact path given."""
    assert RAW_CSV.is_file(), (
        f"Expected source CSV not found at {RAW_CSV}. "
        "Ensure the file exists before you begin."
    )


@pytest.mark.skipif(not RAW_CSV.is_file(), reason="Source CSV is missing")
def test_raw_reviews_csv_content():
    """
    Validate the structure and size of the starting CSV.

    • It must have the correct header columns in the correct order.
    • It must contain exactly the expected number of data rows.
    """
    header, rows = _read_csv_rows(RAW_CSV)

    # Header validation
    assert header == EXPECTED_HEADER, (
        "CSV header mismatch.\n"
        f"Expected: {EXPECTED_HEADER}\n"
        f"Found   : {header}"
    )

    # Row-count validation
    assert len(rows) == EXPECTED_ROW_COUNT, (
        f"CSV does not contain the expected number of rows "
        f"(expected {EXPECTED_ROW_COUNT}, found {len(rows)})."
    )

    # Basic sanity check: ensure each review_id is unique and 1-based ints
    ids = [int(r["review_id"]) for r in rows]
    assert sorted(ids) == list(range(1, EXPECTED_ROW_COUNT + 1)), (
        "review_id column should contain unique consecutive integers "
        "starting at 1."
    )


def test_sqlite3_cli_is_installed():
    """
    The `sqlite3` CLI must be available on the PATH so the student can
    perform all subsequent tasks purely from the shell.
    """
    sqlite_path = shutil.which("sqlite3")
    assert sqlite_path is not None, (
        "The `sqlite3` command-line tool is not installed or not on PATH. "
        "Install it (or fix the PATH) before proceeding."
    )