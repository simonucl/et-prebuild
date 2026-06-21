# test_initial_state.py
"""
Pytest suite that validates the initial, pre-task state of the grading
environment for the “CPU snapshot” exercise.

Rules & checkpoints verified here:
1. /home/user exists and is a directory.
2. /home/user is writable by the current (non-root) user.

We intentionally **do not** check for /home/user/snapshots or the
cpu_top5_20240101.log file, because those are *output artifacts* that
should not be present before the student runs their solution.
"""

from pathlib import Path
import os
import tempfile
import pytest

HOME_DIR = Path("/home/user")


def test_home_directory_exists():
    """
    /home/user must already exist and be a directory so that the task can
    create the required snapshots subdirectory within it later.
    """
    assert HOME_DIR.exists(), (
        "Expected /home/user to exist, but it does not. The grading "
        "environment is mis-configured."
    )
    assert HOME_DIR.is_dir(), (
        f"Expected /home/user to be a directory, but found something else "
        f"({HOME_DIR.stat()} if it exists)."
    )


def test_home_directory_is_writable():
    """
    Verify that the current user can create and delete a temporary file in
    /home/user.  This ensures the student solution has the necessary write
    permissions to create /home/user/snapshots and the log file later.
    """
    try:
        with tempfile.NamedTemporaryFile(dir=HOME_DIR, delete=True) as tmp:
            # Attempt to write a single byte to guarantee write access.
            tmp.write(b"x")
            tmp.flush()
            assert os.path.exists(tmp.name), (
                "Could not create a temporary file inside /home/user. "
                "The directory is not writable."
            )
    except PermissionError as exc:
        pytest.fail(
            f"PermissionError: Unable to write to /home/user — {exc}. "
            "Ensure the directory is writable by the grading user."
        )