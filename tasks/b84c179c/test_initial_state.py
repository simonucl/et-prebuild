# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student carries out the task described in the README.
# In short, nothing that the student is supposed to create should
# exist yet.  If any of the required artefacts are already present
# (especially with the final-expected contents), the test suite will
# fail with a clear, actionable message.
#
# Rules enforced here:
#   1. /home/user/logs/timezone_check.log must NOT exist.
#   2. If /home/user/logs exists already (that is allowed), it must be
#      an actual directory (not a file, symlink, etc.).
#
# NOTE:
# We do *not* forbid the existence of /home/user/logs itself because a
# shared environment might legitimately create such a directory for
# other purposes.  What we *do* forbid is the presence of the target
# log file that the student is expected to create.

import os
from pathlib import Path
import stat
import pytest

HOME_DIR = Path("/home/user")
LOGS_DIR = HOME_DIR / "logs"
TARGET_FILE = LOGS_DIR / "timezone_check.log"


def _is_directory_not_symlink(path: Path) -> bool:
    """
    Return True iff `path` exists, is a directory, and is NOT a symlink.
    """
    try:
        st = path.lstat()
    except FileNotFoundError:
        return False
    # Must be a directory and not a symlink
    return stat.S_ISDIR(st.st_mode) and not stat.S_ISLNK(st.st_mode)


def test_timezone_log_file_absent():
    """
    The target log file must NOT exist before the student runs their
    solution.  If it is already present, the exercise has effectively
    been completed ahead of time, which masks potential errors in the
    student's work.
    """
    assert not TARGET_FILE.exists(), (
        f"The file {TARGET_FILE} already exists. "
        "Please remove it so the student can create it as part of the task."
    )


def test_logs_dir_valid_if_present():
    """
    The /home/user/logs directory _may_ or _may not_ exist prior to the
    student's work.  If it **does** exist, ensure it is a bona-fide
    directory (not a file, FIFO, or symlink).  This guarantees that the
    student will be able to write inside it later.
    """
    if LOGS_DIR.exists():
        assert _is_directory_not_symlink(
            LOGS_DIR
        ), f"{LOGS_DIR} exists but is not a real directory."