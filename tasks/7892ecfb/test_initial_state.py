# test_initial_state.py
# Pytest suite to verify the **initial** state of the operating system / filesystem
# before the student attempts the task described in the prompt.

import os
import pytest
import stat

HOME = "/home/user"
NET_DIAG_DIR = os.path.join(HOME, "net_diag")
TIME_CHECK_LOG = os.path.join(NET_DIAG_DIR, "time_check.log")


def _fail(msg: str):
    """
    Convenience helper to raise a pytest failure with a clear message.
    """
    pytest.fail(msg, pytrace=False)


def test_home_directory_exists_and_is_directory():
    """
    Ensure the base home directory exists and is a directory so that downstream
    tests referencing /home/user can rely on it.
    """
    if not os.path.exists(HOME):
        _fail(f"Expected home directory {HOME!r} to exist, but it does not.")
    if not os.path.isdir(HOME):
        _fail(f"Expected {HOME!r} to be a directory, but it is not.")


def test_net_diag_directory_does_not_exist_yet():
    """
    The assignment instructs the student to create /home/user/net_diag.
    Prior to their work, that directory must not already be present.
    """
    if os.path.exists(NET_DIAG_DIR):
        type_found = "directory" if os.path.isdir(NET_DIAG_DIR) else "file"
        _fail(
            f"Pre-condition failed: {NET_DIAG_DIR!r} already exists "
            f"as a {type_found}. The workspace must start clean."
        )


def test_time_check_log_does_not_exist_yet():
    """
    Likewise, the diagnostic file must not pre-exist.
    """
    if os.path.exists(TIME_CHECK_LOG):
        _fail(
            f"Pre-condition failed: unexpected file {TIME_CHECK_LOG!r} is already present."
        )


def test_parent_of_net_diag_is_not_symlink_or_file():
    """
    Validate that /home/user is a real directory—not a symlink or something else—
    so the student can create sub-directories safely.
    """
    st = os.lstat(HOME)
    if stat.S_ISLNK(st.st_mode):
        _fail(f"{HOME!r} is a symlink, expected a real directory.")
    if not stat.S_ISDIR(st.st_mode):
        _fail(f"{HOME!r} is not a directory (mode: {oct(st.st_mode)}).")