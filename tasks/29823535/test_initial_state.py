# test_initial_state.py
"""
Pytest suite to validate that the operating-system prerequisites for the
“loop-back diagnostics” exercise are in place *before* the student performs
any actions.  These checks deliberately avoid the final artefact
(/home/user/network_diag.txt) per the specification.

The tests assert that:
1. The student’s home directory exists.
2. Standard networking tools (`ping` and `ip`) are available in the PATH.
3. The loop-back network interface (`lo`) is present in the sysfs tree.

If any of these fail, the student will receive a clear, actionable error
message.
"""
from pathlib import Path
import shutil
import os
import stat
import pytest


HOME_DIR = Path("/home/user")
LO_SYSFS_PATH = Path("/sys/class/net/lo")


def test_home_directory_exists_and_is_directory():
    """
    Ensure the expected home directory (/home/user) is present and really
    is a directory.  Without it the student cannot place the report file.
    """
    assert HOME_DIR.exists(), (
        f"Expected home directory {HOME_DIR} is missing. "
        "Create it or correct the base path before proceeding."
    )
    assert HOME_DIR.is_dir(), (
        f"Expected {HOME_DIR} to be a directory, but it is not. "
        "Check the filesystem layout."
    )


@pytest.mark.parametrize("tool", ["ping", "ip"])
def test_required_network_tools_are_in_path(tool):
    """
    Confirm that the essential networking tools (`ping` and `ip`) can be
    located via $PATH.  Students need these to run the diagnostics.
    """
    path = shutil.which(tool)
    assert path is not None, (
        f"Required tool '{tool}' is not available in PATH. "
        "Install it or adjust PATH before starting the exercise."
    )
    # Double-check execute permission
    st_mode = os.stat(path).st_mode
    assert st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH), (
        f"Tool '{tool}' found at {path} but it is not executable."
    )


def test_loopback_interface_exists_in_sysfs():
    """
    Validate that the loop-back interface ('lo') is present in /sys.  The
    student will query its MTU and IP information.
    """
    assert LO_SYSFS_PATH.exists(), (
        "Loop-back interface not found under /sys/class/net/lo. "
        "Ensure the system's networking stack is functioning."
    )