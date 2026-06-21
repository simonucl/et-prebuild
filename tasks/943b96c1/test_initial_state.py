# test_initial_state.py
#
# This pytest suite validates the initial state of the filesystem
# before the student’s solution is applied.

import os
import stat
import pytest

STATUS_DIR = "/home/user/status"
UPTIME_LOG = "/home/user/status/uptime.log"


def test_status_directory_exists_and_is_directory():
    """
    The directory /home/user/status must exist and be a directory.
    """
    assert os.path.exists(STATUS_DIR), (
        f"Required directory '{STATUS_DIR}' is missing."
    )
    assert os.path.isdir(STATUS_DIR), (
        f"'{STATUS_DIR}' exists but is not a directory."
    )

    # Optional: basic permission sanity (directory should be readable by the user)
    mode = os.stat(STATUS_DIR).st_mode
    assert bool(mode & stat.S_IRUSR), (
        f"Directory '{STATUS_DIR}' is not readable by the owner."
    )


def test_uptime_log_exists_and_is_empty():
    """
    The file /home/user/status/uptime.log must exist,
    be a regular file, and have zero bytes.
    """
    assert os.path.exists(UPTIME_LOG), (
        f"Required file '{UPTIME_LOG}' is missing."
    )
    assert os.path.isfile(UPTIME_LOG), (
        f"'{UPTIME_LOG}' exists but is not a regular file."
    )
    size = os.path.getsize(UPTIME_LOG)
    assert size == 0, (
        f"'{UPTIME_LOG}' should be 0 bytes but is {size} bytes."
    )