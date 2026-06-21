# test_initial_state.py
#
# Pytest suite that verifies the **initial** filesystem state
# before the student’s backup script is ever executed.
# Only stdlib modules + pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")
BACKUP_DIR = os.path.join(HOME, "backup")

EXPECTED_DATA_FILES = {
    "report.txt": "Quarterly report Q3 2023\n",
    "config.cfg": "max_connections=100\n",
}


def _read_file(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def data_dir_listing():
    """Return the list of entries in /home/user/data."""
    if not os.path.isdir(DATA_DIR):
        pytest.fail(f"Required directory {DATA_DIR!r} is missing")
    return os.listdir(DATA_DIR)


def test_data_directory_contains_expected_files_only(data_dir_listing):
    missing = [name for name in EXPECTED_DATA_FILES if name not in data_dir_listing]
    unexpected = [name for name in data_dir_listing if name not in EXPECTED_DATA_FILES]

    assert not missing, (
        "The following required file(s) are missing from "
        f"{DATA_DIR}: {', '.join(missing)}"
    )
    assert not unexpected, (
        "Found unexpected file(s)/directory(ies) in "
        f"{DATA_DIR}: {', '.join(unexpected)}"
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_DATA_FILES.items())
def test_data_file_contents(filename, expected_content):
    file_path = os.path.join(DATA_DIR, filename)

    assert os.path.isfile(file_path), f"Expected regular file {file_path} to exist"

    content = _read_file(file_path)
    assert (
        content == expected_content
    ), f"Contents of {file_path} do not match expected text"


def test_backup_directory_exists_and_is_writable_and_empty():
    assert os.path.isdir(
        BACKUP_DIR
    ), f"Required directory {BACKUP_DIR} is missing or not a directory"

    # Check write permission for current user
    assert os.access(
        BACKUP_DIR, os.W_OK
    ), f"Directory {BACKUP_DIR} is not writable by the current user"

    # Ensure directory is empty **before** the backup script runs
    entries = os.listdir(BACKUP_DIR)
    assert (
        len(entries) == 0
    ), f"Directory {BACKUP_DIR} should be empty before running the backup script, found: {entries}"