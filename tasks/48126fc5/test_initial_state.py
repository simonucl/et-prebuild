# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state before the student performs any actions for the “backup benchmark”
# assignment.  It asserts that the source data directory already exists
# (populated by the grader) and that no artefacts of the benchmark task
# are present yet.

import os
import pytest
from pathlib import Path

# Constants for the paths used in the assignment
HOME = Path("/home/user")
DATA_DIR = HOME / "data_to_backup"
BENCHMARK_DIR = HOME / "backup_benchmark"

@pytest.fixture(scope="session")
def data_dir_path() -> Path:
    """Return the Path object for /home/user/data_to_backup."""
    return DATA_DIR


def test_data_directory_exists_and_is_non_empty(data_dir_path):
    """
    The grader promises to create /home/user/data_to_backup **before** the
    student script runs.  Verify that:
      1. The path exists.
      2. It is a directory.
      3. The directory is not empty (contains at least one file or sub-dir).
    """
    assert data_dir_path.exists(), (
        f"Required source directory {data_dir_path} is missing. "
        "The benchmark has no data to work on."
    )
    assert data_dir_path.is_dir(), f"{data_dir_path} exists but is not a directory."
    # Check that the directory is non-empty
    try:
        next(data_dir_path.iterdir())
    except StopIteration:  # pragma: no cover
        pytest.fail(
            f"Directory {data_dir_path} is empty. "
            "It should contain ~8 MB of mixed text files supplied by the grader."
        )


def test_benchmark_directory_does_not_exist_yet():
    """
    The student has not started the task, therefore /home/user/backup_benchmark
    and all artefacts inside it must be absent at this point.
    """
    assert not BENCHMARK_DIR.exists(), (
        f"Directory {BENCHMARK_DIR} already exists before the benchmark runs. "
        "The workspace must be created by the student's solution, not pre-existing."
    )