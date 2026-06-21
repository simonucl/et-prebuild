# test_initial_state.py
#
# Pytest suite to verify that the operating-system state is **clean**
# before the student begins work on:
# “Record the exact container-level hostname in
#  /home/user/container_info/hostname.txt”.
#
# Initial state expectations:
#   1. Directory /home/user/container_info must NOT exist.
#   2. Consequently, the file /home/user/container_info/hostname.txt
#      must also NOT exist.
#
# These pre-checks ensure the grading environment starts from a known,
# empty state and that any artefacts later found were created by the
# student.

import os
from pathlib import Path

CONTAINER_INFO_DIR = Path("/home/user/container_info")
HOSTNAME_FILE = CONTAINER_INFO_DIR / "hostname.txt"


def test_container_info_directory_absent():
    """
    The directory /home/user/container_info must not exist at the start.
    A pre-existing directory would indicate leftover artefacts from a
    previous run and would invalidate the cleanliness of the test
    environment.
    """
    assert not CONTAINER_INFO_DIR.exists(), (
        f"The directory {CONTAINER_INFO_DIR} already exists. "
        "Start with a clean state: remove it before beginning the task."
    )


def test_hostname_file_absent():
    """
    The hostname.txt file must not pre-exist.  Its presence would mean
    the task has already been attempted or completed, defeating the
    purpose of the exercise.
    """
    # If the parent directory is already absent, the file cannot exist,
    # but we check explicitly for clarity and robust failure messages.
    assert not HOSTNAME_FILE.exists(), (
        f"The file {HOSTNAME_FILE} already exists. "
        "Ensure the workspace is clean before performing the task."
    )


def test_parent_directory_is_home_user():
    """
    Sanity-check that the base path /home/user exists and is a directory.
    This guards against misconfigured containers where $HOME is missing
    or relocated.
    """
    home_path = Path("/home/user")
    assert home_path.exists(), "/home/user does not exist in this environment."
    assert home_path.is_dir(), "/home/user exists but is not a directory."