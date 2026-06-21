# test_initial_state.py
#
# Pytest suite verifying that the system is in a “clean” state *before*
# the student starts the workflow described in the assignment.
#
# What we assert **must NOT exist or be running yet**:
#
#   1. /home/user/ml_project/preprocessing/nice_history.log
#   2. /home/user/ml_project/preprocessing/pipeline.pid
#   3. Any “sleep 600” process owned by the current user.
#
# These checks guarantee that the student’s forthcoming commands are the
# only things that create the required files and background process.

import os
import subprocess
import pwd
import pytest
from pathlib import Path

# Constants
HOME = Path("/home/user")
PROJECT_DIR = HOME / "ml_project" / "preprocessing"
NICE_LOG = PROJECT_DIR / "nice_history.log"
PID_FILE = PROJECT_DIR / "pipeline.pid"


def _sleep_600_pids():
    """
    Return a list of PIDs (integers) for any processes **owned by the current
    user** whose command line is exactly `sleep 600` (with or without a leading
    path component, e.g. '/bin/sleep 600').
    """
    user_name = pwd.getpwuid(os.getuid()).pw_name
    try:
        ps_output = subprocess.check_output(
            ["ps", "-u", user_name, "-o", "pid=,args="],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        # If ps fails for some reason, treat as “no such process” so the test
        # will still succeed (and fail later if needed).
        return []

    pids = []
    for line in ps_output.splitlines():
        pid_str, _, cmd = line.strip().partition(" ")
        cmd = cmd.strip()
        # Accept any leading path component, but the final argv[0] must be
        # 'sleep' followed by arg '600'.
        if cmd.endswith("sleep 600"):
            try:
                pids.append(int(pid_str))
            except ValueError:
                # Ignore malformed PID entries.
                continue
    return pids


def test_nice_history_log_absent():
    """
    The nice-history log must NOT exist before the student starts.
    """
    assert not NICE_LOG.exists(), (
        f"Found unexpected file {NICE_LOG}. "
        "Please remove it before beginning the exercise."
    )


def test_pipeline_pid_file_absent():
    """
    The PID file must NOT exist before the student starts.
    """
    assert not PID_FILE.exists(), (
        f"Found unexpected file {PID_FILE}. "
        "Please remove it before beginning the exercise."
    )


def test_no_sleep_600_running():
    """
    Confirm that no stray `sleep 600` process is already running for this user.
    """
    pids = _sleep_600_pids()
    assert not pids, (
        "One or more `sleep 600` processes are already running: "
        f"{', '.join(map(str, pids))}. "
        "Terminate them before starting the assignment."
    )