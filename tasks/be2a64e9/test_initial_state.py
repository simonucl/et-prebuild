# test_initial_state.py
#
# This pytest suite asserts that the system is **still** in its initial state
# BEFORE the student creates the required diagnostics snapshot.
#
# Expected state *before* the task begins:
#   1. The directory /home/user/diagnostics may or may not exist.
#   2. The file   /home/user/diagnostics/sys_snapshot.log MUST **NOT** exist.
#
# If the directory does happen to exist already (perfectly legal, because the
# instructions say “create it if it does not already exist”), the tests also
# verify that it is indeed a directory and that the regular user can write to
# it.  This prevents misleading situations where an unexpected file or a
# read-only directory would block the student’s work.
#
# NOTE: These tests deliberately do *not* look for any of the output-files or
#       headers that will be produced **after** the task is completed; they
#       only make sure the workspace is clean right now.

import os
import stat
import pwd
import pytest

HOME = "/home/user"
DIAG_DIR = os.path.join(HOME, "diagnostics")
SNAPSHOT_FILE = os.path.join(DIAG_DIR, "sys_snapshot.log")


def test_snapshot_file_does_not_exist():
    """
    The main deliverable must NOT be present yet.  If the file already exists
    the student would be prevented from creating it cleanly, or worse, would
    work on stale data.
    """
    assert not os.path.exists(
        SNAPSHOT_FILE
    ), (
        f"The file {SNAPSHOT_FILE!r} already exists, but it should not be present "
        "before the task starts. Please remove it so that a fresh snapshot can "
        "be created."
    )


@pytest.mark.parametrize("path", [DIAG_DIR])
def test_diagnostics_directory_if_it_exists(path):
    """
    The directory may or may not exist initially.  If it *does* exist,
    make sure:
      • It is actually a directory (not a regular file, symlink, etc.).
      • It is writable by the regular user, otherwise the student will not
        be able to place the snapshot inside it.
    """
    if not os.path.exists(path):
        pytest.skip(f"{path!r} does not exist yet, which is acceptable.")
    # It exists: make sure it is a directory
    assert os.path.isdir(
        path
    ), f"{path!r} exists but is not a directory. Please remove or rename it."
    # Check writability for the current (regular) user
    user_uid = os.getuid()
    st: os.stat_result = os.stat(path)

    is_owner = st.st_uid == user_uid
    is_group = st.st_gid == os.getgid()

    mode = st.st_mode
    owner_w = bool(mode & stat.S_IWUSR)
    group_w = bool(mode & stat.S_IWGRP)
    other_w = bool(mode & stat.S_IWOTH)

    writable = (is_owner and owner_w) or (is_group and group_w) or other_w
    assert writable, (
        f"The directory {path!r} exists but is not writable by the current user. "
        "Please adjust its permissions or ownership."
    )