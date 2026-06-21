# test_initial_state.py
#
# This test-suite validates the **initial** operating-system / filesystem
# state _before_ the student attempts the synchronisation task.  If any of
# these tests fail, the environment is not in the expected starting
# condition and the assignment cannot be graded reliably.
#
# The checks deliberately avoid touching **output** locations
# (/home/user/remote_backup, /home/user/sync_logs/last_sync.log, …) in
# accordance with the grading-framework rules.

import os
import stat
import pytest

HOME = "/home/user"
SRC_ROOT = os.path.join(HOME, "projects", "local_workspace")
SYNC_LOGS_DIR = os.path.join(HOME, "sync_logs")

EXPECTED_FILES = {
    os.path.join(SRC_ROOT, "file1.txt"): b"test",
    os.path.join(SRC_ROOT, "file2.txt"): b"hello",
    os.path.join(SRC_ROOT, "nested", "info.txt"): b"bye",
}


def _is_writable_dir(path: str) -> bool:
    """
    Return True iff 'path' exists, is a directory and is writable by the
    current user.
    """
    return os.path.isdir(path) and os.access(path, os.W_OK)


def test_source_directory_exists_and_is_directory():
    assert os.path.isdir(
        SRC_ROOT
    ), f"Expected source directory {SRC_ROOT!r} to exist and be a directory."


def test_source_contains_exactly_three_regular_files():
    """
    Verify that /home/user/projects/local_workspace contains **exactly**
    the three expected regular files (one of which is in a sub-directory)
    and nothing else.
    """
    found_regular_files = []
    for root, _, files in os.walk(SRC_ROOT):
        for name in files:
            full_path = os.path.join(root, name)
            # Guard against symlinks or other special files
            st_mode = os.lstat(full_path).st_mode
            if stat.S_ISREG(st_mode):
                found_regular_files.append(full_path)
            else:
                pytest.fail(
                    f"Unexpected non-regular file {full_path!r} found in source tree."
                )

    # Normalise lists for comparison
    expected_paths = sorted(EXPECTED_FILES.keys())
    found_regular_files_sorted = sorted(found_regular_files)

    assert (
        found_regular_files_sorted == expected_paths
    ), (
        "Source directory does not contain exactly the expected regular files.\n"
        f"Expected: {expected_paths}\n"
        f"Found   : {found_regular_files_sorted}"
    )


@pytest.mark.parametrize("filepath,expected_bytes", EXPECTED_FILES.items())
def test_each_file_has_expected_contents_and_size(filepath, expected_bytes):
    assert os.path.isfile(filepath), f"Missing expected file {filepath!r}."

    with open(filepath, "rb") as fh:
        data = fh.read()

    assert (
        data == expected_bytes
    ), f"File {filepath!r} contains unexpected data: {data!r}."

    expected_size = len(expected_bytes)
    actual_size = os.path.getsize(filepath)
    assert (
        actual_size == expected_size
    ), f"File {filepath!r} should be {expected_size} bytes, found {actual_size}."


def test_sync_logs_directory_exists_and_is_writable():
    assert os.path.isdir(
        SYNC_LOGS_DIR
    ), f"Directory {SYNC_LOGS_DIR!r} must exist before the sync begins."

    assert _is_writable_dir(
        SYNC_LOGS_DIR
    ), f"Directory {SYNC_LOGS_DIR!r} exists but is not writable by the current user."