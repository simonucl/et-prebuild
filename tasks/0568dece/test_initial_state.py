# test_initial_state.py
#
# Pytest suite to verify the *initial* operating-system / filesystem state
# before the student begins working on ticket #9901.  These tests make sure
# the necessary tools and baseline environment exist so that the student can
# complete the assignment, yet they deliberately avoid checking for any of
# the files or directories the student is expected to create (per project
# rules).
#
# Only the Python standard library and pytest are used.

import os
import stat
import sys
import pytest
from pathlib import Path


PING_CANDIDATES = [
    "/bin/ping",
    "/usr/bin/ping",
    "/sbin/ping",
    "/usr/sbin/ping",
]


@pytest.fixture(scope="session")
def ping_path():
    """
    Locate the system's `ping` binary in one of a handful of common locations.
    Returns the first path found or raises pytest.Skip if none can be located.
    """
    for path in PING_CANDIDATES:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    # If we get here, we could not find an executable ping utility.
    pytest.skip(
        "Cannot locate an executable `ping` command in expected locations "
        f"({', '.join(PING_CANDIDATES)}).  The student cannot continue without it."
    )


def test_ping_command_is_executable(ping_path):
    """
    Verify that the `ping` binary is present and has execute permissions.
    """
    st = os.stat(ping_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, (
        f"`ping` exists at {ping_path!s} but is not executable. "
        "Ensure it has the proper execute bits set (e.g. 0755)."
    )


def test_loopback_interface_present():
    """
    Ensure the loopback network interface (lo) is present in /proc/net/dev.
    This is a fundamental requirement for being able to ping 127.0.0.1.
    """
    proc_net_dev = Path("/proc/net/dev")
    assert proc_net_dev.is_file(), "/proc/net/dev is missing; cannot verify interfaces."

    with proc_net_dev.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Extract interface names before the ':' delimiter.
    interfaces = {line.split(":")[0].strip() for line in lines if ":" in line}

    assert "lo" in interfaces, (
        "The loopback interface 'lo' is not present in /proc/net/dev. "
        "Without it the student cannot demonstrate local connectivity."
    )


def test_home_user_directory_exists():
    """
    Confirm that the expected home directory /home/user exists and is a directory.
    """
    home = Path("/home/user")
    assert home.is_dir(), (
        "/home/user does not exist or is not a directory. "
        "The assignment instructions assume this path is available."
    )