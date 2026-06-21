# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state *before* the learner
creates any symbolic links or log files.

The initial state must satisfy all of the following:

1. Directory /home/user/data/original/ exists.
2. Directory /home/user/data/working/ exists.
3. Regular file /home/user/data/original/train_set.csv exists (must not be a
   symlink or directory).
4. Regular file /home/user/data/original/test_set.csv exists (must not be a
   symlink or directory).

This test purposefully **does not** check for the presence or absence of any
future output artifacts (e.g., train.csv, test.csv, or
/home/user/data/symlink_verification.log) in order to comply with the grading
rules.
"""

from pathlib import Path
import os
import pytest

ORIGINAL_DIR = Path("/home/user/data/original")
WORKING_DIR = Path("/home/user/data/working")
TRAIN_FILE = ORIGINAL_DIR / "train_set.csv"
TEST_FILE = ORIGINAL_DIR / "test_set.csv"


def _assert_is_regular_file(path: Path):
    """
    Helper that asserts the given path is a regular file (not a symlink,
    directory, or anything else).
    """
    assert path.exists(), f"Expected file {path} to exist, but it does not."
    assert path.is_file(), f"Expected {path} to be a regular file, but it is not."
    # pathlib considers symlinks to files as 'is_file()' == True; ensure it's not a symlink.
    assert not path.is_symlink(), f"Expected {path} to be a regular file, but it is a symlink."


def test_original_directory_exists():
    assert ORIGINAL_DIR.exists(), (
        f"Required directory {ORIGINAL_DIR} is missing. "
        "The dataset directory structure is not present."
    )
    assert ORIGINAL_DIR.is_dir(), (
        f"Expected {ORIGINAL_DIR} to be a directory, but it is not."
    )


def test_working_directory_exists():
    assert WORKING_DIR.exists(), (
        f"Required working directory {WORKING_DIR} is missing."
    )
    assert WORKING_DIR.is_dir(), (
        f"Expected {WORKING_DIR} to be a directory, but it is not."
    )


@pytest.mark.parametrize(
    "csv_path",
    [TRAIN_FILE, TEST_FILE],
    ids=["train_set.csv", "test_set.csv"],
)
def test_original_csv_files_exist(csv_path: Path):
    _assert_is_regular_file(csv_path)