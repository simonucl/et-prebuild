# test_initial_state.py
#
# Pytest suite that verifies the *initial* filesystem state expected for the
# “database backup benchmark” exercise.  These tests **must** pass **before**
# the student attempts the task.  If any test fails, the starting conditions
# are not as specified and the assignment cannot be graded reliably.
#
# Requirements checked
# --------------------
# 1. /home/user/sample_db_data  :
#       • exists and is a directory
#       • contains exactly three CSV files:
#           - customers.csv  (50 lines, header: "id,name")
#           - orders.csv     (100 lines, header: "id,customer_id,total")
#           - products.csv   (30  lines, header: "id,name,price")
#
# 2. /home/user/backup_benchmark :
#       • must *not* exist yet (nothing should have been produced)
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import pytest

SAMPLE_DB_DIR = Path("/home/user/sample_db_data").resolve()
BACKUP_BENCHMARK_DIR = Path("/home/user/backup_benchmark").resolve()

EXPECTED_FILES = {
    "customers.csv": {
        "lines": 50,
        "header": "id,name",
    },
    "orders.csv": {
        "lines": 100,
        "header": "id,customer_id,total",
    },
    "products.csv": {
        "lines": 30,
        "header": "id,name,price",
    },
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _read_lines(path: Path):
    """Read the file as text using UTF-8 and return list of lines without
    trailing newline characters."""
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines()]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_sample_db_directory_exists_and_is_correct():
    # 1. Directory existence & type
    assert SAMPLE_DB_DIR.exists(), (
        f"Required directory {SAMPLE_DB_DIR} does not exist. "
        "The exercise expects this directory to be provided."
    )
    assert SAMPLE_DB_DIR.is_dir(), f"{SAMPLE_DB_DIR} is expected to be a directory."

    # 2. Exact file list
    existing_files = sorted(p.name for p in SAMPLE_DB_DIR.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_FILES.keys())
    assert existing_files == expected_files, (
        f"{SAMPLE_DB_DIR} must contain exactly the files "
        f"{expected_files}, but found {existing_files}. "
        "Ensure no extra or missing files are present."
    )


@pytest.mark.parametrize("filename,meta", EXPECTED_FILES.items())
def test_each_csv_file_has_correct_header_and_linecount(filename, meta):
    file_path = SAMPLE_DB_DIR / filename
    assert file_path.exists(), f"Expected file {file_path} not found."

    lines = _read_lines(file_path)
    # Non-empty file
    assert lines, f"{file_path} is empty; expected {meta['lines']} lines."

    # Header check
    expected_header = meta["header"]
    assert (
        lines[0] == expected_header
    ), f"Header mismatch in {file_path}: expected '{expected_header}', got '{lines[0]}'."

    # Line-count check
    expected_count = meta["lines"]
    actual_count = len(lines)
    assert (
        actual_count == expected_count
    ), f"{file_path} should have {expected_count} lines, found {actual_count}."


def test_backup_benchmark_directory_not_yet_present():
    assert not BACKUP_BENCHMARK_DIR.exists(), (
        f"Directory {BACKUP_BENCHMARK_DIR} already exists before the benchmark "
        "has been run. The student task should create this directory; "
        "please ensure the initial environment is clean."
    )