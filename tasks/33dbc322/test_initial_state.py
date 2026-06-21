# test_initial_state.py
#
# This pytest suite validates that the operating-system state is **clean**
# before the student starts work on the “dummy restore” task.
#
# – /home/user/restore_test        MUST NOT exist yet
# – /home/user/restore_test/restore_status.log  MUST NOT exist yet
# – There MUST be **no** running “sleep 300” process owned by the current user
#
# If any of these pre-conditions fail, the environment is not in the
# expected initial state and the student would get misleading feedback.

import os
import subprocess
import pwd
import stat
import pytest
from pathlib import Path


HOME_DIR = Path("/home/user")
RESTORE_DIR = HOME_DIR / "restore_test"
LOG_FILE = RESTORE_DIR / "restore_status.log"


def _current_username() -> str:
    """Return the current user's login name."""
    return pwd.getpwuid(os.getuid()).pw_name


def _running_sleep_300_pids_owned_by_user(username: str):
    """
    Return a set of PIDs for processes owned by `username`
    whose command line is exactly 'sleep 300'.
    """
    try:
        # '-u username' restricts to processes owned by the user.
        # `pid=` and `args=` emit PID and CMD without headers or extra spacing.
        ps_output = subprocess.check_output(
            ["ps", "-u", username, "-o", "pid=", "-o", "args="],
            text=True,
        )
    except subprocess.CalledProcessError as exc:  # pragma: no cover
        pytest.fail(f"Could not run ps to inspect processes: {exc}")

    pids = set()
    for line in ps_output.strip().splitlines():
        if not line.strip():
            continue
        # The first field (PID) may have leading spaces; split once.
        pid_str, cmdline = line.strip().split(maxsplit=1)
        if cmdline == "sleep 300":
            try:
                pids.add(int(pid_str))
            except ValueError:  # pragma: no cover
                continue
    return pids


def test_restore_directory_does_not_exist():
    assert not RESTORE_DIR.exists(), (
        f"Pre-condition failed: Directory '{RESTORE_DIR}' already exists. "
        "The task expects it to be created by the student's solution, "
        "so it must be absent before they start."
    )


def test_log_file_does_not_exist():
    assert not LOG_FILE.exists(), (
        f"Pre-condition failed: Log file '{LOG_FILE}' already exists. "
        "The task requires the student to create this file; "
        "it must not be present at the outset."
    )


def test_no_sleep_300_process_running_for_user():
    username = _current_username()
    pids = _running_sleep_300_pids_owned_by_user(username)
    assert not pids, (
        "Pre-condition failed: The following 'sleep 300' processes are already "
        f"running and owned by user '{username}': {sorted(pids)}. "
        "There must be no such processes before the student launches their "
        "single dummy restore job."
    )