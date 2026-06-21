# test_initial_state.py
#
# Pytest suite that validates the initial state of the filesystem
# BEFORE the learner performs any actions for the “FinOps analyst”
# task.  These tests must all pass **as-is** when the exercise
# starts.  If any of them fail, the starting environment is broken
# and the learner is not at fault.
#
# Checked items:
# 1. Three raw CSV files exist at the expected absolute paths.
# 2. Each raw file:
#    • is owned by the current user,
#    • has mode 0644,
#    • contains the single placeholder line.
# 3. The quarterly workspace directory does NOT exist yet.
# 4. The parent directory /home/user/cloud_costs exists and is a directory.
#
# NOTE: We intentionally do NOT check for any post-task artefacts
# (renamed files, new directory, log lines, etc.) because those are
# created by the learner’s solution.

import os
import pwd
import stat
from pathlib import Path

import pytest


HOME = Path("/home/user")
CLOUD_COSTS_DIR = HOME / "cloud_costs"

RAW_FILES = {
    "Jan": CLOUD_COSTS_DIR / "raw_costs_Jan.csv",
    "Feb": CLOUD_COSTS_DIR / "raw_costs_Feb.csv",
    "Mar": CLOUD_COSTS_DIR / "raw_costs_Mar.csv",
}

QUARTERLY_DIR = CLOUD_COSTS_DIR / "quarterly_2023_Q1"

EXPECTED_CONTENT = "cloud_costs_placeholder\n"
EXPECTED_MODE = 0o644  # rw-r--r--


def _get_file_mode(path: Path) -> int:
    """Return the permission bits (e.g., 0o644) of *path*."""
    return stat.S_IMODE(path.stat().st_mode)


def test_cloud_costs_directory_present_and_is_directory():
    assert CLOUD_COSTS_DIR.exists(), (
        f"Expected directory {CLOUD_COSTS_DIR} to exist, "
        "but it does not."
    )
    assert CLOUD_COSTS_DIR.is_dir(), (
        f"Expected {CLOUD_COSTS_DIR} to be a directory."
    )


@pytest.mark.parametrize("month,file_path", RAW_FILES.items())
def test_raw_files_exist(month, file_path: Path):
    assert file_path.exists(), (
        f"Raw cost file for {month} is missing: {file_path}"
    )
    assert file_path.is_file(), (
        f"{file_path} exists but is not a regular file."
    )


@pytest.mark.parametrize("month,file_path", RAW_FILES.items())
def test_raw_files_mode(month, file_path: Path):
    mode = _get_file_mode(file_path)
    assert mode == EXPECTED_MODE, (
        f"Incorrect mode for {file_path}. "
        f"Expected 0o{EXPECTED_MODE:03o}, got 0o{mode:03o}."
    )


@pytest.mark.parametrize("month,file_path", RAW_FILES.items())
def test_raw_files_owner(month, file_path: Path):
    file_uid = file_path.stat().st_uid
    current_uid = os.getuid()
    current_user = pwd.getpwuid(current_uid).pw_name
    assert file_uid == current_uid, (
        f"Owner UID mismatch for {file_path}. "
        f"Expected owner '{current_user}' (UID {current_uid}), "
        f"but file is owned by UID {file_uid}."
    )


@pytest.mark.parametrize("month,file_path", RAW_FILES.items())
def test_raw_files_content(month, file_path: Path):
    content = file_path.read_text()
    assert content == EXPECTED_CONTENT, (
        f"Unexpected content in {file_path!s}. "
        f"Expected one line {EXPECTED_CONTENT!r}."
    )


def test_quarterly_directory_not_yet_present():
    assert not QUARTERLY_DIR.exists(), (
        f"Directory {QUARTERLY_DIR} should NOT exist before the learner "
        "runs their solution."
    )