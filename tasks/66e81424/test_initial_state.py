# test_initial_state.py
#
# Pytest suite that validates the starting conditions *before* the learner
# carries out the “network-diagnostic heartbeat log” task.
#
# We purposely do NOT look for the target directory
# /home/user/network_diagnostics or the file
# /home/user/network_diagnostics/ping_localhost.log, because those are
# deliverables that should not exist yet.  Instead, we make sure the host is
# in a sane state and that the required tooling (“ping”) is available and
# functional.

import os
import shutil
import subprocess
import sys
import pytest
from pathlib import Path

HOME_DIR = Path("/home/user")


def test_home_directory_exists():
    """
    The baseline home directory for the learner must exist; otherwise the
    remainder of the exercise has no place to store output.
    """
    assert HOME_DIR.exists(), f"Expected home directory {HOME_DIR} to exist."
    assert HOME_DIR.is_dir(), f"{HOME_DIR} exists but is not a directory."


def test_ping_executable_is_available():
    """
    The exercise requires the standard `ping` utility.  Verify that it can be
    found in $PATH and is executable.
    """
    ping_path = shutil.which("ping")
    assert ping_path is not None, (
        "The `ping` command is not found in the system's PATH; "
        "the student will be unable to complete the task."
    )
    # On many Unix systems ping carries the SUID bit so non-root users can
    # send ICMP echo requests.  Regardless of permissions, it must at least be
    # executable by the current user.
    assert os.access(ping_path, os.X_OK), f"`ping` exists at {ping_path} but is not executable."


@pytest.mark.timeout(5)  # Fail fast if something is fundamentally broken
def test_ping_loopback_succeeds():
    """
    Confirm that the machine can ping its own loopback interface.  This
    double-checks that the networking stack and `ping` binary both work, and
    that the learner will receive the expected command output.
    """
    ping_cmd = ["ping", "-c", "1", "127.0.0.1"]
    try:
        completed = subprocess.run(
            ping_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=4,
        )
    except FileNotFoundError:
        pytest.fail("`ping` executable vanished between tests.")
    except subprocess.TimeoutExpired:
        pytest.fail("`ping` command timed out; loopback connectivity is broken.")

    assert completed.returncode == 0, (
        "Pinging 127.0.0.1 failed; return code "
        f"{completed.returncode}. stderr was:\n{completed.stderr}"
    )
    assert "127.0.0.1" in completed.stdout, (
        "The output of `ping 127.0.0.1` did not contain '127.0.0.1'. "
        "Unexpected ping implementation or output."
    )