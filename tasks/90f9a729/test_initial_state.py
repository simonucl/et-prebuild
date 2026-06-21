# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system
# environment _before_ the student starts working on the assignment.
#
# IMPORTANT:  The assignment will eventually ask the student to create
# artifacts under /home/user/capacity_planner/, but **these tests must not
# reference or assert anything about those future output paths** (per the
# test-writing rules).  Instead we only confirm that the baseline environment
# is sane and that the student has a writable $HOME in which to place their
# work.

import os
import stat
import tempfile
from pathlib import Path

import pytest

HOME = Path("/home/user")


def test_home_directory_exists_and_is_directory():
    """
    The baseline environment must provide the student with a /home/user
    directory.  It must be an actual directory, not a symlink or file.
    """
    assert HOME.exists(), f"Expected {HOME} to exist."
    assert HOME.is_dir(), f"Expected {HOME} to be a directory, but it is not."


def test_home_directory_is_writable():
    """
    The student must have write permissions inside /home/user so that they can
    create the resources required by the assignment.  This test creates (and
    immediately deletes) a temporary file to verify writability.
    """
    # os.access with W_OK does not always reflect the *effective* ability to
    # write (e.g., ACLs), so we perform an actual write attempt.
    with tempfile.NamedTemporaryFile(dir=HOME, prefix=".__pytest_write_test_", delete=True) as tmp:
        tmp.write(b"test")
        tmp.flush()
        assert Path(tmp.name).exists(), "Failed to write inside /home/user."


def test_home_directory_permissions_reasonable():
    """
    While exact mode bits can vary, the directory must at least have the owner's
    read, write and execute permissions so the student (owner) can work.
    """
    st: os.stat_result = os.stat(HOME)
    mode = st.st_mode
    # Owner permissions
    owner_can_read = bool(mode & stat.S_IRUSR)
    owner_can_write = bool(mode & stat.S_IWUSR)
    owner_can_exec = bool(mode & stat.S_IXUSR)
    assert owner_can_read and owner_can_write and owner_can_exec, (
        f"{HOME} must be readable, writable and executable by its owner. "
        f"Current mode: {oct(mode & 0o777)}"
    )