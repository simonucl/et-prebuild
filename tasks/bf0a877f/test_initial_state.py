# test_initial_state.py
#
# This pytest suite verifies that the execution environment
# starts in a **clean** state, i.e. _before_ the student’s
# script performs any action.
#
# The tests assert that:
#   1.  /home/user/test_environment/pids  does **not** exist.
#   2.  /home/user/test_environment/pids/daemon.pid  does **not** exist.
#   3.  There is **no** running process whose command line is exactly
#       `tail -f /dev/null`.
#
# If any of these assumptions fail, the exercise may produce false-positive
# or false-negative results, so we stop early with clear error messages.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path
import pytest

# Constants for paths
ROOT_DIR = Path("/home/user/test_environment")
PIDS_DIR = ROOT_DIR / "pids"
PID_FILE = PIDS_DIR / "daemon.pid"


def _iter_proc_cmdlines():
    """
    Yields tuples of (pid: int, argv: list[str]) for every process
    the current (unprivileged) user can inspect.
    Reading /proc/<pid>/cmdline returns a NUL-separated byte string.
    """
    proc_root = Path("/proc")
    for entry in proc_root.iterdir():
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        cmdline_path = entry / "cmdline"
        try:
            raw = cmdline_path.read_bytes()
        except (FileNotFoundError, PermissionError):
            # Process may have exited or we lack permission – skip it.
            continue
        if not raw:
            # Kernel threads show up with an empty cmdline.
            continue
        argv = raw.rstrip(b"\x00").split(b"\x00")
        # Decode bytes -> str using system default (UTF-8 on most distros).
        argv = [arg.decode() for arg in argv]
        yield pid, argv


def _count_tail_devnull_processes():
    """
    Returns the number of processes whose argv is exactly:
        ['tail', '-f', '/dev/null']
    """
    return sum(
        1
        for _pid, argv in _iter_proc_cmdlines()
        if argv == ["tail", "-f", "/dev/null"]
    )


def test_pids_directory_absent():
    """
    The directory /home/user/test_environment/pids must NOT exist
    before the student's script runs. Its presence would indicate
    contamination from a previous attempt.
    """
    assert not PIDS_DIR.exists(), (
        f"The directory '{PIDS_DIR}' already exists before execution. "
        "The initial environment must be clean."
    )


def test_pid_file_absent():
    """
    The file /home/user/test_environment/pids/daemon.pid must NOT exist
    at the beginning.
    """
    assert not PID_FILE.exists(), (
        f"The file '{PID_FILE}' already exists. "
        "It should be created only by the student's solution."
    )


def test_no_lingering_tail_devnull_process():
    """
    There must be **zero** `tail -f /dev/null` processes running
    prior to the student's code. Otherwise we cannot reliably
    determine which process was started by the student.
    """
    count = _count_tail_devnull_processes()
    assert count == 0, (
        "Found an existing 'tail -f /dev/null' process before the exercise "
        f"started (count={count}). The environment must be free of such "
        "processes."
    )