# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the student starts working on the “netdiag” task.  We make sure
# that none of the artefacts the student is supposed to create are already
# present and that no leftover “ping 127.0.0.1” process is running.
#
# NOTE:  These checks purposefully assert the *absence* of the directories,
#        files and processes that will be produced by a correct solution.

import os
import subprocess
from pathlib import Path

NETDIAG_DIR = Path("/home/user/netdiag")
PING_LOG = NETDIAG_DIR / "ping.log"
PING_PID = NETDIAG_DIR / "ping.pid"
PROC_BEFORE = NETDIAG_DIR / "proc_before_kill.txt"
DIAG_REPORT = NETDIAG_DIR / "diag_report.log"

def _running_ping_localhost_pids():
    """
    Return a list of PIDs for any running `ping 127.0.0.1`
    processes owned by the current user.
    """
    try:
        # ps -eo pid,args      --> "  PID COMMAND_LINE"
        ps_output = subprocess.check_output(
            ["ps", "-eo", "pid,args"], text=True, encoding="utf-8"
        )
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"Failed to enumerate processes via ps: {exc}")

    pids = []
    for line in ps_output.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            pid_str, cmd = line.split(maxsplit=1)
        except ValueError:
            # Some implementations may print only the PID when the command
            # line is empty; ignore those.
            continue
        if "ping" in cmd and "127.0.0.1" in cmd:
            pids.append(int(pid_str))
    return pids

def test_netdiag_directory_should_not_exist():
    assert not NETDIAG_DIR.exists(), (
        f"Directory {NETDIAG_DIR} already exists. "
        "The environment must start clean."
    )

def test_no_residual_output_files():
    missing = []
    unexpected = []
    for fpath in (PING_LOG, PING_PID, PROC_BEFORE, DIAG_REPORT):
        if fpath.exists():
            unexpected.append(str(fpath))
        else:
            missing.append(str(fpath))  # Keep list to silence flake complaints
    assert not unexpected, (
        "The following files unexpectedly exist before the task starts: "
        + ", ".join(unexpected)
    )

def test_no_ping_localhost_process_running():
    pids = _running_ping_localhost_pids()
    assert not pids, (
        "One or more 'ping 127.0.0.1' processes are already running "
        f"({pids}).  The system must start without such processes."
    )