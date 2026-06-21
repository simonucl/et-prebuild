# test_initial_state.py
#
# Pytest suite that validates the file-system state *before* the student
# performs any action for the “large, stale log files” exercise.
#
# The tests assert that the required directories and *.log files exist
# with the exact sizes and (minimum) modification ages described in the
# task statement.  Should anything be missing or have the wrong
# properties, the failure messages will clearly point out what is wrong.
#
# IMPORTANT:  These tests purposefully avoid touching any artefacts that
#             are expected to be produced *after* the student’s solution
#             runs (e.g. *.gz files, the report file, …) in order to
#             comply with the grading rules.

import os
import stat
import time
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_ROOT = HOME / "apps" / "logs"
OUTPUT_DIR = HOME / "output"


@pytest.mark.parametrize(
    "path",
    [
        LOG_ROOT,
        LOG_ROOT / "old",
        OUTPUT_DIR,
    ],
)
def test_required_directories_exist_and_are_accessible(path: Path):
    assert path.exists(), f"Required directory {path} is missing."
    assert path.is_dir(), f"Expected {path} to be a directory."
    # Must be readable; OUTPUT_DIR also needs to be writable.
    assert os.access(path, os.R_OK), f"Directory {path} is not readable."
    if path == OUTPUT_DIR:
        assert os.access(path, os.W_OK), (
            f"Directory {OUTPUT_DIR} must be writable for the upcoming report."
        )


@pytest.mark.parametrize(
    "path, expected_size_bytes, minimum_age_days",
    [
        (LOG_ROOT / "app1.log", 614_400, 2),
        (LOG_ROOT / "app2.log", 307_200, 2),
        (LOG_ROOT / "old" / "old.log", 819_200, 2),
    ],
)
def test_log_files_exist_with_correct_size_and_age(
    path: Path, expected_size_bytes: int, minimum_age_days: int
):
    assert path.exists(), f"Expected log file {path} to exist."
    assert path.is_file(), f"{path} should be a regular file."

    st = path.stat()

    # Verify that it is a *regular* file (not a symlink, fifo, etc.)
    assert stat.S_ISREG(st.st_mode), f"{path} must be a regular file."

    # Check size.
    assert (
        st.st_size == expected_size_bytes
    ), f"{path} has size {st.st_size} bytes, expected {expected_size_bytes}."

    # Check that the modification time is at least `minimum_age_days` old.
    age_seconds = time.time() - st.st_mtime
    required_seconds = minimum_age_days * 24 * 60 * 60
    assert (
        age_seconds >= required_seconds
    ), (
        f"{path} is only {age_seconds/86400:.2f} days old; "
        f"must be at least {minimum_age_days} days."
    )