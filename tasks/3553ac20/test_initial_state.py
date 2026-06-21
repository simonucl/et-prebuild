# test_initial_state.py
#
# This test-suite validates the **initial** state of the “freshly-provisioned”
# Linux host *before* the student starts working on the task described in the
# exercise.  Nothing that the student is supposed to create should be present
# yet, but the tools that the student will need (ip & ss) **must** already be
# available and runnable as an ordinary user.

import os
import subprocess
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# CONSTANTS                                                                   #
# --------------------------------------------------------------------------- #
HOME = Path("/home/user")
SNAPSHOT_DIR = HOME / "network_logs"
SNAPSHOT_FILE = SNAPSHOT_DIR / "network_diagnostics.log"

IP_CMD = ["ip", "-4", "addr", "show"]
ROUTE_CMD = ["ip", "route", "show"]
SS_CMD = ["ss", "-lntu"]


# --------------------------------------------------------------------------- #
# HELPER FUNCTIONS                                                            #
# --------------------------------------------------------------------------- #
def _run(cmd):
    """
    Run *cmd* and return the CompletedProcess instance.

    The call must:
      * Succeed (exit status 0).
      * Produce *some* stdout (not just a blank line).
    """
    proc = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        env=os.environ,
    )
    return proc


# --------------------------------------------------------------------------- #
# TESTS                                                                       #
# --------------------------------------------------------------------------- #
def test_home_directory_exists():
    assert HOME.exists(), f"The home directory {HOME} is missing."
    assert HOME.is_dir(), f"{HOME} exists but is not a directory."


def test_snapshot_directory_absent():
    """
    The directory /home/user/network_logs should NOT exist yet.  The
    student is responsible for creating it later.
    """
    assert not SNAPSHOT_DIR.exists(), (
        f"The directory {SNAPSHOT_DIR} already exists.  "
        "The host should be clean before the exercise starts."
    )


def test_snapshot_file_absent():
    """
    The file /home/user/network_logs/network_diagnostics.log should NOT
    exist yet.  The student will create it as part of the exercise.
    """
    assert not SNAPSHOT_FILE.exists(), (
        f"The file {SNAPSHOT_FILE} already exists.  "
        "The host should be clean before the exercise starts."
    )


@pytest.mark.parametrize(
    "cmd,cmd_name",
    [
        (IP_CMD, "ip -4 addr show"),
        (ROUTE_CMD, "ip route show"),
        (SS_CMD, "ss -lntu"),
    ],
)
def test_required_commands_available_and_runnable(cmd, cmd_name):
    """
    The commands that the student must capture (`ip` and `ss`) have to be
    present in the container image **and** executable by an unprivileged user.
    """
    proc = _run(cmd)

    # Does the executable exist?
    assert proc.returncode == 0, (
        f"Running `{cmd_name}` failed with return code {proc.returncode}.\n"
        f"stderr was:\n{proc.stderr}"
    )

    # We expect *some* output; an empty string or only whitespace would be odd.
    stdout_stripped = proc.stdout.strip()
    assert stdout_stripped, (
        f"`{cmd_name}` produced no output at all.  "
        "It should emit at least one line so the student has something to log."
    )