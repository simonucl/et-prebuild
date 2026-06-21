# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state
# before the student performs any actions.  It checks only the
# pre-existing snapshots area and purposely avoids inspecting
# output paths such as /home/user/capacity_planner.

import os
import stat
import pytest

SNAPSHOT_ROOT = "/home/user/snapshots"
EXPECTED_DATES = ("2023-06-01", "2023-07-01")
RESOURCE_FILES = ("cpu.csv", "memory.csv")


def _is_regular_file(path: str) -> bool:
    """
    Return True only if `path` exists *and* is a regular file
    (i.e. not a directory, FIFO, device, or symlink).
    """
    try:
        st = os.lstat(path)  # lstat so we do NOT follow symlinks
    except FileNotFoundError:
        return False
    return stat.S_ISREG(st.st_mode)


def test_snapshot_root_directory_exists():
    assert os.path.isdir(
        SNAPSHOT_ROOT
    ), f"Required directory missing: {SNAPSHOT_ROOT}"


@pytest.mark.parametrize("date", EXPECTED_DATES)
def test_snapshot_date_directories_exist(date):
    dir_path = os.path.join(SNAPSHOT_ROOT, date)
    assert os.path.isdir(
        dir_path
    ), f"Required snapshot directory missing: {dir_path}"


@pytest.mark.parametrize("date", EXPECTED_DATES)
@pytest.mark.parametrize("filename", RESOURCE_FILES)
def test_resource_files_exist_and_are_regular(date, filename):
    file_path = os.path.join(SNAPSHOT_ROOT, date, filename)
    assert os.path.exists(
        file_path
    ), f"Expected file does not exist: {file_path}"

    assert _is_regular_file(
        file_path
    ), f"Path must be a regular file (not a symlink or directory): {file_path}"