# test_initial_state.py
#
# Pytest suite that verifies the operating-system / filesystem *before*
# the student carries out the task described in the assignment.
#
# It asserts that none of the benchmark-related artefacts already exist
# so the student must create them from scratch.

import os
from pathlib import Path

import pytest

# Constants used throughout the checks
HOME = Path("/home/user")
MLOPS_DIR = HOME / "mlops"
BENCHMARKS_DIR = MLOPS_DIR / "benchmarks"
CSV_FILE = BENCHMARKS_DIR / "perf_20240101T120000Z.csv"
INDEX_FILE = MLOPS_DIR / "benchmark_index.txt"
CSV_FILENAME_STR = "perf_20240101T120000Z.csv"


def _read_last_line(path: Path) -> str | None:
    """
    Helper: return the last non-empty line of `path` if it exists,
    otherwise return None.
    """
    try:
        with path.open("r", encoding="utf-8") as f:
            lines = [ln.rstrip("\n") for ln in f if ln.rstrip("\n")]
            return lines[-1] if lines else ""
    except FileNotFoundError:
        return None


def test_benchmarks_directory_does_not_exist():
    """
    The directory /home/user/mlops/benchmarks must NOT exist yet.
    """
    assert not BENCHMARKS_DIR.exists(), (
        f"Pre-condition failed: {BENCHMARKS_DIR} already exists. "
        "The student task should create this directory."
    )


def test_csv_file_does_not_exist():
    """
    The target CSV file must NOT exist before the student creates it.
    """
    assert not CSV_FILE.exists(), (
        f"Pre-condition failed: {CSV_FILE} already exists. "
        "The student task should be responsible for creating this file."
    )


def test_index_file_absent_or_without_target_entry():
    """
    The index file can be absent or pre-existing, but if it exists its
    last non-empty line must NOT already list the target CSV filename.
    """
    last_line = _read_last_line(INDEX_FILE)
    assert last_line != CSV_FILENAME_STR, (
        f"Pre-condition failed: {INDEX_FILE} already lists "
        f"'{CSV_FILENAME_STR}' as its last line. The student task must "
        "append this entry; it should not be present beforehand."
    )


def test_parent_mlops_directory_state():
    """
    The parent directory /home/user/mlops may or may not exist; if it
    does, ensure it is a directory (not a file or symlink).
    """
    if MLOPS_DIR.exists():
        assert MLOPS_DIR.is_dir(), (
            f"Path {MLOPS_DIR} exists but is not a directory. "
            "The task expects this path to be a directory."
        )