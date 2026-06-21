# test_initial_state.py
#
# This pytest suite validates **baseline** assumptions about the execution
# environment *before* the student performs any task-related actions.
#
# NOTE:
#   • As required, we do *not* touch or test for the expected output paths
#     (/home/user/data, the quota report, etc.).  We only check that the
#     operating-system baseline is sane and ready for the student’s script.

import os
import stat
import sys
from pathlib import Path

HOME = Path("/home/user")
TMP  = Path("/tmp")
DEV_NULL = Path("/dev/null")
PROC = Path("/proc")
PROC_SELF = Path("/proc/self")


def _octal_permissions(path: Path) -> int:
    """
    Helper to return the permission bits (e.g. 0o755) of *path*.
    """
    return stat.S_IMODE(path.stat().st_mode)


def test_home_directory_exists_and_is_directory():
    """
    The 'user' home directory must exist so the student can create the
    required workspace beneath it.
    """
    assert HOME.exists(), f"Expected {HOME} to exist, but it does not."
    assert HOME.is_dir(), f"Expected {HOME} to be a directory."


def test_home_directory_is_writable_by_owner():
    """
    Verify that the owner of /home/user has write permission.  This is
    essential for creating the required sub-directories later.
    """
    perms = _octal_permissions(HOME)
    owner_write = perms & 0o200
    assert owner_write, (
        f"Owner write permission missing on {HOME!s}. "
        f"Current octal mode: {oct(perms)}"
    )


def test_tmp_exists_and_is_world_writable():
    """
    /tmp should exist and allow any process to create temporary files
    (permissions 0o777; the sticky bit may also be set → 0o1777).
    """
    assert TMP.exists(), "/tmp directory is missing."
    assert TMP.is_dir(), "/tmp exists but is not a directory."

    # Only look at rwx; ignore higher bits such as the sticky bit.
    perms = _octal_permissions(TMP) & 0o777
    assert perms == 0o777, (
        f"/tmp should be world-writable (777). "
        f"Current rwx bits: {oct(perms)}"
    )


def test_dev_null_character_device_exists():
    """
    /dev/null must be present and be a character special file so that
    scripts can safely discard unwanted output.
    """
    assert DEV_NULL.exists(), "/dev/null does not exist."
    st_mode = DEV_NULL.stat().st_mode
    assert stat.S_ISCHR(st_mode), "/dev/null exists but is not a character device."


def test_proc_filesystem_is_mounted():
    """
    The proc filesystem is commonly required for many utilities.
    """
    assert PROC.exists() and PROC.is_dir(), "/proc is not available."
    assert PROC_SELF.exists() and PROC_SELF.is_dir(), "/proc/self is missing."


def test_python_version_is_reasonable():
    """
    Ensure the Python interpreter version is at least 3.8, providing modern
    stdlib features the student might rely on.
    """
    assert sys.version_info >= (3, 8), (
        "Python >= 3.8 is required, "
        f"but current version is {sys.version_info.major}.{sys.version_info.minor}"
    )