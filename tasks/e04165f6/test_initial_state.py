# test_initial_state.py
"""
Pytest suite that validates the initial operating-system / filesystem state
*before* the student performs any work for the “backup-testing” exercise.

What we assert here:
1. The required directories exist under /home/user/backup_testing/.
2. The two manifest CSV files exist with the exact, correct contents.
3. The manifest headers have the expected six comma-separated columns.

We deliberately do NOT test for the presence or absence of any output /
deliverable files (daily_cols.txt, combined_restore_report.tsv, etc.),
because those are expected to be created *after* the student completes
the task.

Only the Python standard library and pytest are used.
"""

import pathlib
import csv
import pytest

# ---------------------------------------------------------------------------
# Helper constants
# ---------------------------------------------------------------------------

HOME = pathlib.Path("/home/user")
BACKUP_DIR = HOME / "backup_testing"
MANIFEST_DIR = BACKUP_DIR / "manifests"

DAILY_MANIFEST = MANIFEST_DIR / "daily_restore_2023-01-15.csv"
WEEKLY_MANIFEST = MANIFEST_DIR / "weekly_restore_2023-01-15.csv"

EXPECTED_HEADER = ["ID", "FILE_PATH", "ORIGINAL_SIZE", "RESTORED_SIZE", "STATUS", "CRC32"]

EXPECTED_DAILY_ROWS = [
    ["1", "/data/db1.sql", "1048576", "1048576", "OK", "3A5F1D2C"],
    ["2", "/data/db2.sql", "2048000", "2048000", "OK", "B2C4E6F3"],
    ["3", "/data/db3.sql", "1048576", "1048572", "WARNING", "D3A7C9E4"],
]

EXPECTED_WEEKLY_ROWS = [
    ["1", "/backup/www.tar.gz", "4096000", "4096000", "OK", "9C1D2E3F"],
    ["2", "/backup/mail.tar.gz", "2097152", "2097152", "OK", "AA11BB22"],
    ["3", "/backup/home.tar.gz", "3145728", "3145720", "WARNING", "CC33DD44"],
    ["4", "/backup/configs.tar.gz", "512000", "512000", "OK", "EE44FF55"],
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_required_directories_exist():
    """Ensure /home/user/backup_testing and its manifests sub-directory exist."""
    assert BACKUP_DIR.is_dir(), f"Expected directory {BACKUP_DIR} to exist."
    assert MANIFEST_DIR.is_dir(), f"Expected directory {MANIFEST_DIR} to exist."


@pytest.mark.parametrize(
    "manifest_path", [DAILY_MANIFEST, WEEKLY_MANIFEST]
)
def test_manifest_files_exist(manifest_path):
    """Basic presence check for the two manifest CSV files."""
    assert manifest_path.is_file(), f"Expected file {manifest_path} to exist."


def _read_csv(path):
    """Read a CSV file using the csv.reader (comma delimiter)."""
    with path.open(newline="") as fh:
        reader = csv.reader(fh)
        return [row for row in reader]


@pytest.mark.parametrize(
    "path_, expected_rows",
    [
        (DAILY_MANIFEST, EXPECTED_DAILY_ROWS),
        (WEEKLY_MANIFEST, EXPECTED_WEEKLY_ROWS),
    ],
)
def test_manifest_content_exact(path_, expected_rows):
    """
    The content (header + data rows) of each manifest must match the
    reference truth exactly.
    """
    rows = _read_csv(path_)

    # --- Check header ---
    assert rows, f"{path_} appears to be empty."
    assert rows[0] == EXPECTED_HEADER, (
        f"Header in {path_} is incorrect.\n"
        f"Expected: {EXPECTED_HEADER}\n"
        f"Found:    {rows[0]}"
    )

    # --- Check data rows ---
    data_rows = rows[1:]  # skip header
    assert data_rows == expected_rows, (
        f"Data rows in {path_} are not as expected.\n"
        f"Expected ({len(expected_rows)} rows):\n{expected_rows}\n"
        f"Found ({len(data_rows)} rows):\n{data_rows}"
    )