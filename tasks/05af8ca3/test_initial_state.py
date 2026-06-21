# test_initial_state.py
#
# Pytest suite that verifies the filesystem **before** the student performs
# any actions.  It checks only the resources that must already exist and does
# NOT look for any artefacts the student is expected to create.

import os
import stat
import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")
BACKUP_DIR = os.path.join(HOME, "backup")
FILE1 = os.path.join(DATA_DIR, "file1.txt")
FILE2 = os.path.join(DATA_DIR, "file2.txt")


def _assert_is_regular_file(path: str):
    """Helper that asserts `path` exists and is a regular file (not dir/symlink)."""
    if not os.path.exists(path):
        pytest.fail(f"Required file {path!r} is missing.")
    if not stat.S_ISREG(os.stat(path, follow_symlinks=False).st_mode):
        pytest.fail(f"{path!r} exists but is not a regular file.")


def _assert_is_directory(path: str):
    """Helper that asserts `path` exists and is a directory (not symlink)."""
    if not os.path.exists(path):
        pytest.fail(f"Required directory {path!r} is missing.")
    if not stat.S_ISDIR(os.stat(path, follow_symlinks=False).st_mode):
        pytest.fail(f"{path!r} exists but is not a directory.")


def test_data_directory_exists():
    """The source directory /home/user/data must already exist."""
    _assert_is_directory(DATA_DIR)


def test_expected_files_exist_with_correct_contents():
    """file1.txt and file2.txt must exist with exact expected contents."""
    expected_contents = {
        FILE1: "alpha\n",
        FILE2: "beta\n",
    }

    for path, expected in expected_contents.items():
        _assert_is_regular_file(path)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                actual = fh.read()
        except Exception as exc:
            pytest.fail(f"Could not read {path!r}: {exc}")

        assert actual == expected, (
            f"File {path!r} does not contain the expected contents.\n"
            f"Expected: {expected!r}\nActual:   {actual!r}"
        )


def test_backup_directory_exists_and_is_empty():
    """
    The destination directory /home/user/backup must exist and be empty
    before the student starts.  Being empty guarantees the student does not
    rely on pre-existing artefacts.
    """
    _assert_is_directory(BACKUP_DIR)

    unwanted_items = os.listdir(BACKUP_DIR)
    assert (
        len(unwanted_items) == 0
    ), f"{BACKUP_DIR!r} is expected to be empty, but found: {unwanted_items}"