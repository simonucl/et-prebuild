# test_initial_state.py
#
# This pytest file asserts that none of the artefacts the student is
# supposed to create for the “network-diagnostic log” task are present
# **before** they start working.  If any of these files/directories
# already exist, the test fails with a clear, actionable message.

import os
import pytest
import stat

HOME = "/home/user"
PROJECT_DIR = os.path.join(HOME, "project")
NET_DIAG_DIR = os.path.join(PROJECT_DIR, "net_diag")
LOG_FILE = os.path.join(NET_DIAG_DIR, "diag.log")


def _exists(path: str) -> bool:
    """Return True if *path* exists in the filesystem."""
    return os.path.lexists(path)


def test_home_directory_must_exist():
    """
    Sanity-check: /home/user should exist on the test runner.  If it
    doesn’t, there is something fundamentally wrong with the environment
    and the rest of the tests become meaningless.
    """
    assert os.path.isdir(HOME), (
        f"Expected base home directory {HOME!r} to exist for the exercise, "
        "but it does not.  The test environment is mis-configured."
    )


@pytest.mark.parametrize(
    "path, what",
    [
        (PROJECT_DIR, "directory /home/user/project"),
        (NET_DIAG_DIR, "directory /home/user/project/net_diag"),
        (LOG_FILE, "file   /home/user/project/net_diag/diag.log"),
    ],
)
def test_workspace_is_pristine(path: str, what: str):
    """
    None of the paths the student is tasked with creating should exist
    yet.  We deliberately *do not* care about permission bits here –
    mere non-existence is sufficient.
    """
    assert not _exists(path), (
        f"{what} already exists before the student has begun.  "
        "The workspace must start from a clean slate."
    )


def test_no_stale_net_diag_processes():
    """
    Optional sanity check: ensure no lingering `ping`/`traceroute`/`nslookup`
    processes from previous runs are hanging around.  This isn’t strictly
    required by the task, but catching stale processes early avoids test
    flakiness in constrained CI environments.
    """
    # We can only use the stdlib, so we look in /proc for PIDs (Linux CI
    # assumption).  If /proc isn’t available we silently skip.
    proc_root = "/proc"
    if not os.path.isdir(proc_root):
        pytest.skip("/proc is not present; cannot inspect running processes")

    suspicious = {"ping", "traceroute", "nslookup", "dig", "ip"}
    found = []

    for pid in os.listdir(proc_root):
        if not pid.isdigit():
            continue
        cmd_path = os.path.join(proc_root, pid, "comm")
        try:
            with open(cmd_path, "rt", encoding="utf-8") as fh:
                cmd = fh.read().strip()
            if cmd in suspicious:
                found.append((pid, cmd))
        except (FileNotFoundError, PermissionError):
            continue  # The process exited or we lack permission.

    assert not found, (
        "Stale network-diagnostic processes detected:\n"
        + "\n".join(f"PID {pid}: {cmd}" for pid, cmd in found)
        + "\nPlease start the exercise with a clean process table."
    )