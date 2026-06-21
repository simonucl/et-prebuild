# test_initial_state.py
#
# This test-suite verifies that the operating-system / filesystem is in the
# expected **initial** state *before* the student performs any actions for the
# “UTC time-zone & en_US.UTF-8 locale compliance” task.  All artefacts the
# student will later create MUST be absent at this point.

import os
import pytest
import stat

HOME = "/home/user"
AUDIT_DIR = os.path.join(HOME, "compliance_audit")
SCRIPT_PATH = os.path.join(AUDIT_DIR, "enforce_time_locale.sh")
REPORT_PATH = os.path.join(AUDIT_DIR, "time_locale_report.txt")


def _exists(path: str) -> bool:
    """Return True if a path exists (file, dir, or symlink), False otherwise."""
    return os.path.exists(path)


def _is_executable(path: str) -> bool:
    """Return True if a file exists and any executable bit is set."""
    try:
        st_mode = os.stat(path).st_mode
    except FileNotFoundError:
        return False
    return bool(st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


def test_audit_directory_does_not_exist():
    """
    The audit directory /home/user/compliance_audit must NOT exist yet.
    """
    assert not _exists(
        AUDIT_DIR
    ), (
        f"Pre-condition failed: '{AUDIT_DIR}' already exists. "
        "The student task starts with a clean slate, so this directory "
        "should not be present."
    )


@pytest.mark.parametrize(
    "path, description",
    [
        (SCRIPT_PATH, "enforce_time_locale.sh script"),
        (REPORT_PATH, "time_locale_report.txt report file"),
    ],
)
def test_task_files_do_not_exist(path, description):
    """
    Neither the enforcement script nor the report file should exist
    before the student has begun the task.
    """
    assert not _exists(
        path
    ), (
        f"Pre-condition failed: the {description!s} at '{path}' already exists. "
        "The system must be in its initial state with no task artefacts present."
    )


def test_script_not_executable():
    """
    If, against expectations, the script does exist, it should at least not be
    executable yet.  This test adds a second guard so the suite still fails
    clearly if the directory was created and the script dropped in place
    prematurely with executable permissions.
    """
    assert not _is_executable(
        SCRIPT_PATH
    ), (
        f"Pre-condition failed: '{SCRIPT_PATH}' is already executable. "
        "The script should not exist—or at least not be executable—prior to "
        "the student's work."
    )