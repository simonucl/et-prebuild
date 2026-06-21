# test_initial_state.py
#
# This test-suite validates the *initial* state of the OS / filesystem
# before the student carries out the task described in the instructions.
#
# The task requires the student to create:
#   1. /home/user/tech_writing/schedules/backup_cron.md
#   2. /home/user/tech_writing/schedules/task_log.txt
#
# At this point (i.e. before the task is done) **none** of those artefacts
# should exist.  These tests guarantee the workspace starts clean and give
# clear guidance if it is not.

import os
import pytest

BASE_DIR = "/home/user/tech_writing/schedules"
BACKUP_FILE = os.path.join(BASE_DIR, "backup_cron.md")
LOG_FILE = os.path.join(BASE_DIR, "task_log.txt")


@pytest.mark.parametrize(
    "path,kind",
    [
        (BACKUP_FILE, "file"),
        (LOG_FILE, "file"),
    ],
)
def test_expected_files_do_not_exist_yet(path, kind):
    """
    Confirm that the specific files the student is about to create
    are NOT present in the filesystem *before* they start.

    If any of these exist already, it means the environment is dirty
    and could mask implementation mistakes.
    """
    assert not os.path.exists(
        path
    ), (
        f"Initial state violation: The {kind!s} '{path}' is already present. "
        "The workspace must start clean so the exercise can be graded "
        "reliably."
    )


def test_base_directory_may_or_may_not_exist():
    """
    The parent directory may legitimately exist or not; both are acceptable
    for the starting point.  This test is included primarily to give a clear,
    explicit statement about that fact and to guard against the extremely
    unlikely situation that the path exists *as a file*.
    """
    if os.path.exists(BASE_DIR):
        assert os.path.isdir(
            BASE_DIR
        ), (
            f"Initial state violation: '{BASE_DIR}' exists but is not a "
            "directory.  Remove or rename this path so the student can "
            "create the required directory hierarchy."
        )


def test_no_unexpected_contents_previously_created(tmp_path_factory):
    """
    If the base directory happens to exist already, ensure that it does NOT
    contain artefacts that look like a previous run (e.g., files whose names
    end with 'backup_cron.md' or 'task_log.txt').

    This prevents stale files with atypical names from passing the later,
    post-task checks.
    """
    if not os.path.isdir(BASE_DIR):
        pytest.skip("Base directory does not exist yet; nothing further to check.")

    suspicious_files = [
        entry
        for entry in os.listdir(BASE_DIR)
        if entry.endswith(("backup_cron.md", "task_log.txt"))
        and entry not in {os.path.basename(BACKUP_FILE), os.path.basename(LOG_FILE)}
    ]

    assert not suspicious_files, (
        "Initial state violation: Unexpected pre-existing files found in "
        f"'{BASE_DIR}': {suspicious_files}.  Remove them so the exercise can "
        "start with a clean slate."
    )