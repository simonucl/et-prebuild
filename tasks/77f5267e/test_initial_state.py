# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student performs any actions.  It checks only the objects that
# are guaranteed to exist at the start of the exercise and explicitly avoids
# testing for any of the items the student is asked to create.
#
# What must already be present:
#   1. /home/user/data/live                 – existing directory
#   2. /home/user/data/live/important.db    – existing regular file
#   3. /home/user/archives/snap_latest      – *broken* symbolic link that
#                                            points to /home/user/data/old_live
#
# Nothing else is verified here (per the grading-spec “DO NOT test for any of
# the output files or directories”).

import os
import stat
from pathlib import Path

DATA_DIR = Path("/home/user/data/live")
IMPORTANT_DB = DATA_DIR / "important.db"
SNAP_LATEST_LINK = Path("/home/user/archives/snap_latest")
BROKEN_TARGET = Path("/home/user/data/old_live")


def test_data_live_directory_exists():
    """
    /home/user/data/live must exist and be a directory.
    """
    assert DATA_DIR.exists(), (
        f"Expected directory {DATA_DIR} to exist, but it is missing."
    )
    assert DATA_DIR.is_dir(), (
        f"Expected {DATA_DIR} to be a directory, "
        f"but found a different file type."
    )


def test_important_db_file_exists():
    """
    /home/user/data/live/important.db must exist and be a regular file
    (not a symlink).
    """
    assert IMPORTANT_DB.exists(), (
        f"Expected file {IMPORTANT_DB} to exist, but it is missing."
    )

    st = IMPORTANT_DB.lstat()
    assert stat.S_ISREG(st.st_mode), (
        f"Expected {IMPORTANT_DB} to be a regular file, "
        f"but it is not."
    )


def test_snap_latest_is_broken_symlink():
    """
    /home/user/archives/snap_latest must exist, be a symlink pointing to
    /home/user/data/old_live, and the target directory must be absent
    (i.e. the link is broken).
    """
    assert SNAP_LATEST_LINK.exists() or SNAP_LATEST_LINK.is_symlink(), (
        f"Expected symlink {SNAP_LATEST_LINK} to exist, but it is missing."
    )
    assert SNAP_LATEST_LINK.is_symlink(), (
        f"Expected {SNAP_LATEST_LINK} to be a symbolic link, "
        f"but it is not."
    )

    link_target = SNAP_LATEST_LINK.readlink()
    assert link_target == BROKEN_TARGET, (
        f"Symlink {SNAP_LATEST_LINK} points to {link_target}, "
        f"but it should point to {BROKEN_TARGET}."
    )

    assert not BROKEN_TARGET.exists(), (
        f"The target of {SNAP_LATEST_LINK} ({BROKEN_TARGET}) unexpectedly exists; "
        f"it should be absent so the link is broken."
    )