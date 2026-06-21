# test_initial_state.py
# Pytest suite that verifies the *initial* filesystem state required by the task.
# It purposely does NOT look for the output file the student is expected to create.
# Only stdlib and pytest are used.

import os
import pytest

DIR_PATH = "/home/user/storage_reports"
SOURCE_FILE = os.path.join(DIR_PATH, "current_usage.csv")

# The file must match this block exactly, including the final newline.
EXPECTED_CONTENT = (
    "filesystem,used_GB,available_GB\n"
    "/,12,38\n"
    "/home,40,60\n"
    "/var/log,4,6\n"
    "/tmp,1,9\n"
)


def test_storage_reports_directory_exists_and_writable():
    """
    The directory /home/user/storage_reports must exist and be writable.
    """
    assert os.path.isdir(DIR_PATH), (
        f"Required directory {DIR_PATH} does not exist.\n"
        "Create it before proceeding."
    )

    assert os.access(DIR_PATH, os.W_OK), (
        f"Directory {DIR_PATH} exists but is not writable by the current user.\n"
        "Adjust permissions so the task can create new files inside it."
    )


def test_current_usage_csv_exists_and_is_correct():
    """
    Verify that /home/user/storage_reports/current_usage.csv exists and that its
    contents match the exact specification in the task description.
    """
    assert os.path.isfile(SOURCE_FILE), (
        f"Required file {SOURCE_FILE} does not exist.\n"
        "Ensure it is present before attempting the task."
    )

    with open(SOURCE_FILE, "r", newline="") as fh:
        actual_content = fh.read()

    assert actual_content == EXPECTED_CONTENT, (
        f"The contents of {SOURCE_FILE} do not match the expected template.\n\n"
        "Expected (repr):\n"
        f"{EXPECTED_CONTENT!r}\n\n"
        "Actual (repr):\n"
        f"{actual_content!r}"
    )