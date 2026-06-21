# test_initial_state.py
#
# Pytest suite to verify the **initial** state of the system *before*
# the student executes any task‐related commands for the “root UID
# security-sanity check” exercise.
#
# What we assert here:
# 1. The canonical `root` account exists and has UID 0.
# 2. Neither the output directory nor the log file (which the student
#    is supposed to create) exist yet.
#
# A failing test provides a clear, descriptive error message so that
# any deviation from the expected baseline state is immediately
# obvious.

import os
import pwd
import pytest

# Constants for paths the student will eventually create
OUTPUT_DIR = "/home/user/scan_output"
LOG_FILE = os.path.join(OUTPUT_DIR, "root_uid_check.log")


def test_root_account_uid_is_zero():
    """
    The host must have a canonical 'root' account with UID 0.
    If this test fails, the exercise makes no sense because the
    student's single-line check would be meaningless.
    """
    try:
        root_pw_entry = pwd.getpwnam("root")
    except KeyError:  # pragma: no cover
        pytest.fail(
            "The system has no 'root' entry in /etc/passwd; "
            "cannot perform the intended UID check."
        )

    assert (
        root_pw_entry.pw_uid == 0
    ), f"'root' UID is {root_pw_entry.pw_uid}, expected 0."


def test_output_directory_does_not_exist_yet():
    """
    The /home/user/scan_output directory must NOT exist **before**
    the student runs their command.  Its presence would indicate that
    the task was already executed (or that the environment is dirty).
    """
    assert not os.path.exists(
        OUTPUT_DIR
    ), (
        f"Directory {OUTPUT_DIR!r} should not exist before the task is run; "
        "found it already present."
    )


def test_log_file_does_not_exist_yet():
    """
    Likewise, the specific log file must be absent prior to execution.
    """
    assert not os.path.exists(
        LOG_FILE
    ), (
        f"Log file {LOG_FILE!r} should not exist before the task is run; "
        "found it already present."
    )