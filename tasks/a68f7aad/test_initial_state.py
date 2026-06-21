# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system state
for the “disk-usage analysis” workflow **before** the student runs
any commands.

Only the pre-existing fixture (/home/user/disk_demo and its
contents) is checked.  No assertions are made about the future
output directory or log file.

The expected fixture:

/home/user/disk_demo
├── file1.txt   5,120  bytes  (ASCII “A”)
└── file2.bin  20,480  bytes  (random data)

Total directory size: 25,600 bytes
"""

import os
import stat
import pytest

DISK_DEMO_DIR = "/home/user/disk_demo"
FILE1 = os.path.join(DISK_DEMO_DIR, "file1.txt")
FILE2 = os.path.join(DISK_DEMO_DIR, "file2.bin")

# Expected byte sizes as specified in the task description.
EXPECTED_SIZE_FILE1 = 5_120
EXPECTED_SIZE_FILE2 = 20_480
EXPECTED_TOTAL_SIZE = 25_600


def _file_mode(path):
    """Return the permission bits of a filesystem entry as an integer."""
    return stat.S_IMODE(os.lstat(path).st_mode)


@pytest.mark.parametrize(
    "path,kind",
    [
        (DISK_DEMO_DIR, "directory"),
        (FILE1, "file"),
        (FILE2, "file"),
    ],
)
def test_paths_exist(path, kind):
    """
    Ensure that the disk_demo directory and its expected files exist
    and are of the correct filesystem type.
    """
    assert os.path.exists(path), f"Expected {kind} at '{path}' is missing."

    if kind == "directory":
        assert os.path.isdir(
            path
        ), f"Expected '{path}' to be a directory, but it is not."
    else:
        assert os.path.isfile(
            path
        ), f"Expected '{path}' to be a regular file, but it is not."


@pytest.mark.parametrize(
    "path,expected_size",
    [
        (FILE1, EXPECTED_SIZE_FILE1),
        (FILE2, EXPECTED_SIZE_FILE2),
    ],
)
def test_individual_file_sizes(path, expected_size):
    """
    Verify that each file in /home/user/disk_demo has the exact byte size
    specified by the fixture description.
    """
    actual_size = os.path.getsize(path)
    assert (
        actual_size == expected_size
    ), f"Size mismatch for '{path}': expected {expected_size} bytes, found {actual_size} bytes."


def test_total_directory_size():
    """
    Confirm that the total size in bytes of /home/user/disk_demo equals 25,600,
    matching the combination of the two known files.
    """
    total = 0
    for root, _dirs, files in os.walk(DISK_DEMO_DIR):
        for fn in files:
            total += os.path.getsize(os.path.join(root, fn))

    assert (
        total == EXPECTED_TOTAL_SIZE
    ), f"Total size of '{DISK_DEMO_DIR}' should be {EXPECTED_TOTAL_SIZE} bytes, found {total} bytes."