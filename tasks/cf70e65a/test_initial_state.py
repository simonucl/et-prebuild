# test_initial_state.py
#
# Pytest suite to verify the _initial_ state of the operating‐system
# environment, i.e. **before** the student begins the benchmark task.
# The checks deliberately confirm that no artefacts from the assignment
# are already present while also making sure required system utilities
# exist.
#
# Requirements being validated:
#
# 1.   The directory   /home/user/benchmark            must NOT exist yet.
# 2.   The CSV file    /home/user/benchmark/summary.csv must NOT exist yet.
# 3.   The POSIX timing utility /usr/bin/time must be present and executable
#      so that students can benchmark their commands.
#
# Any failure message should clearly point out what is wrong so that the
# environment can be fixed _before_ the actual assignment begins.

import os
import stat
import pytest
from pathlib import Path

BENCHMARK_DIR = Path("/home/user/benchmark")
SUMMARY_CSV   = BENCHMARK_DIR / "summary.csv"
TIME_BINARY   = Path("/usr/bin/time")


def _is_executable(file_path: Path) -> bool:
    """
    Helper to determine whether `file_path` is an existing, executable file.
    """
    return file_path.is_file() and os.access(str(file_path), os.X_OK)


def test_benchmark_directory_absent():
    """
    The benchmark directory must NOT yet exist.  Students should create it
    themselves.  If it is already present, the environment is ‘dirty’.
    """
    assert not BENCHMARK_DIR.exists(), (
        f"The directory {BENCHMARK_DIR} already exists. "
        "The initial state should be clean—remove it before students start."
    )


def test_summary_csv_absent():
    """
    The summary CSV file must NOT exist in the initial state; students are
    supposed to generate it during the assignment.
    """
    assert not SUMMARY_CSV.exists(), (
        f"The file {SUMMARY_CSV} already exists. "
        "Ensure the environment is clean before the task begins."
    )


def test_time_binary_present_and_executable():
    """
    The assignment requires the external utility `/usr/bin/time -p`.
    Verify that it exists and is executable so students can rely on it.
    """
    assert TIME_BINARY.exists(), (
        "/usr/bin/time is missing. Install ‘time’ package or fix the path."
    )

    assert TIME_BINARY.is_file(), (
        "/usr/bin/time exists but is not a regular file."
    )

    assert os.access(str(TIME_BINARY), os.X_OK), (
        "/usr/bin/time is present but not executable. "
        "Adjust its permissions (chmod +x) or reinstall the package."
    )