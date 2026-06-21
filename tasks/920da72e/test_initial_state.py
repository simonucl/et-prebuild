# test_initial_state.py
#
# Pytest suite verifying the OS / filesystem **before** any student action.
# It asserts that the landing area starts exactly as described in the
# assignment specification.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")

DIRS = {
    "incoming": HOME / "data" / "incoming",
    "archive": HOME / "archive",
    "logs": HOME / "logs",
    "bin": HOME / "bin",
}

FILES = {
    "log1": {
        "path": DIRS["incoming"] / "log1.txt",
        "size": 2_048,
    },
    "old_report": {
        "path": DIRS["incoming"] / "old_report.tar",
        "size": 5_242_880,   # 5 MiB
    },
    "video": {
        "path": DIRS["incoming"] / "video.mp4",
        "size": 15_728_640,  # 15 MiB
    },
}


def _assert_mode_755(path: Path):
    """Assert that the filesystem object's mode bits equal 0o755."""
    mode = stat.S_IMODE(path.stat().st_mode)
    assert mode == 0o755, (
        f"Expected permissions 755 (-rwxr-xr-x or drwxr-xr-x) on {path}, "
        f"found {oct(mode)[2:]}"
    )


@pytest.mark.parametrize("key", DIRS.keys())
def test_directories_present_and_permissions(key):
    """
    All required directories must exist and have permission bits 755.
    """
    path = DIRS[key]
    assert path.exists(), f"Missing directory: {path}"
    assert path.is_dir(), f"Path is not a directory: {path}"
    _assert_mode_755(path)


@pytest.mark.parametrize("key", ["archive", "logs", "bin"])
def test_directories_start_empty(key):
    """
    /home/user/archive, /home/user/logs, and /home/user/bin must be empty
    at the outset.
    """
    path = DIRS[key]
    contents = list(path.iterdir())
    assert (
        len(contents) == 0
    ), f"Directory {path} is expected to be empty; found: {[p.name for p in contents]}"


@pytest.mark.parametrize("file_key", FILES.keys())
def test_files_present_with_exact_size(file_key):
    """
    Each expected file must exist in /home/user/data/incoming and have the
    exact byte size specified in the specification.
    """
    file_info = FILES[file_key]
    path = file_info["path"]
    expected_size = file_info["size"]

    assert path.exists(), f"Missing file: {path}"
    assert path.is_file(), f"Path is not a regular file: {path}"

    actual_size = path.stat().st_size
    assert (
        actual_size == expected_size
    ), f"{path} should be {expected_size} bytes, found {actual_size} bytes"


def test_no_cleanup_script_yet():
    """
    Before the student delivers their solution, /home/user/bin/disk_cleanup.sh
    should NOT exist. Its presence would indicate that the starting state is
    already modified.
    """
    script_path = DIRS["bin"] / "disk_cleanup.sh"
    assert (
        not script_path.exists()
    ), f"Found unexpected script at {script_path}; initial state should not contain the cleanup script."