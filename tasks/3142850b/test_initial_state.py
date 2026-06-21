# test_initial_state.py
#
# This pytest suite verifies the PRE-exercise state of the filesystem.
# It must be executed before the student runs any commands so that the
# subsequent grading script can rely on a clean, known layout.
#
# The checks below assert that:
#   • /home/user/finops_data exists and contains exactly the three
#     first-level sub-directories dev/, prod/, and staging/.
#   • Each of those sub-directories exists and is a real directory.
#   • One sample file is present in each environment directory and its
#     size in bytes matches the pre-populated fixture data.
#   • The output file /home/user/cloud_costs/disk_snapshot.log is NOT
#     present yet (the student must create it during the exercise).

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
FINOPS_DIR = HOME / "finops_data"
CLOUD_COSTS_DIR = HOME / "cloud_costs"
SNAPSHOT_FILE = CLOUD_COSTS_DIR / "disk_snapshot.log"

# Expected first-level sub-directories under /home/user/finops_data
EXPECTED_ENV_DIRS = {
    "dev": {"sample_file": "tmp.log", "size_bytes": 4321},
    "prod": {"sample_file": "data1.bin", "size_bytes": 12345},
    "staging": {"sample_file": "readme.txt", "size_bytes": 6789},
}


def test_finops_data_directory_exists_and_is_directory():
    assert FINOPS_DIR.exists(), f"Required directory {FINOPS_DIR} is missing."
    assert FINOPS_DIR.is_dir(), f"{FINOPS_DIR} exists but is not a directory."


def test_finops_data_contains_exactly_three_expected_subdirs():
    subdirs = [d for d in FINOPS_DIR.iterdir() if d.is_dir()]
    subdir_names = sorted(d.name for d in subdirs)

    expected_names_sorted = sorted(EXPECTED_ENV_DIRS.keys())
    assert (
        subdir_names == expected_names_sorted
    ), (
        f"{FINOPS_DIR} must contain EXACTLY the three directories "
        f"{expected_names_sorted}. Current directories found: {subdir_names}"
    )


@pytest.mark.parametrize("env_name,meta", EXPECTED_ENV_DIRS.items())
def test_each_environment_directory_and_sample_file(env_name, meta):
    env_path = FINOPS_DIR / env_name
    sample_file_path = env_path / meta["sample_file"]

    # Directory checks
    assert env_path.exists(), f"Expected directory {env_path} is missing."
    assert env_path.is_dir(), f"{env_path} exists but is not a directory."

    # Sample file checks
    assert sample_file_path.exists(), (
        f"Expected sample file {sample_file_path} is missing."
    )
    assert sample_file_path.is_file(), (
        f"{sample_file_path} exists but is not a regular file."
    )

    actual_size = sample_file_path.stat().st_size
    expected_size = meta["size_bytes"]
    assert (
        actual_size == expected_size
    ), f"{sample_file_path} size is {actual_size} bytes, expected {expected_size} bytes."


def test_snapshot_file_not_yet_present():
    """
    The exercise requires the student to create /home/user/cloud_costs/disk_snapshot.log.
    Before the student starts, this file MUST NOT exist to avoid false positives.
    The parent directory may or may not exist, but the file itself must be absent.
    """
    assert not SNAPSHOT_FILE.exists(), (
        f"Pre-exercise snapshot file {SNAPSHOT_FILE} already exists. "
        "It should be created by the student during the task, not beforehand."
    )