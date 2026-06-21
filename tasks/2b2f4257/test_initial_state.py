# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem
# BEFORE the learner executes any actions for the “loopback latency
# check” exercise.
#
# We intentionally DO NOT check for the existence (or absence) of
# /home/user/loopback_ping_raw.log, because that is the required
# output artifact and the rubric forbids such tests at this stage.
#
# The goals here are to prove that the system is ready for the task:
# 1. The home directory exists and is a directory.
# 2. A usable `ping` binary is present somewhere on $PATH.
# 3. The loopback interface (127.0.0.1) responds successfully to
#    three ICMP echo-requests, indicating a healthy local network
#    stack.
#
# Only the Python standard library and pytest are used.

import os
import shutil
import subprocess
import sys
import textwrap

import pytest


HOME_DIR = "/home/user"


def _assert(condition: bool, msg: str):
    """
    Small helper that raises an assertion with the provided message
    *only* if the condition is False.  This keeps assertion messages
    consistently explicit.
    """
    if not condition:
        pytest.fail(msg, pytrace=False)


def test_home_directory_exists():
    """
    The canonical home directory for the learner MUST exist and be a
    directory.  Without this, the assignment cannot proceed because
    the output file must live in that location.
    """
    _assert(
        os.path.isdir(HOME_DIR),
        f"Expected home directory {HOME_DIR!r} to exist and be a directory, "
        "but it is missing or is not a directory.",
    )


def test_ping_binary_available_and_executable():
    """
    Validate that a `ping` binary is on the PATH and is executable.
    We rely on shutil.which() for portability rather than hard-coding
    a full path such as /bin/ping, /usr/bin/ping, etc.
    """
    ping_path = shutil.which("ping")
    _assert(
        ping_path is not None,
        "No `ping` executable found on PATH. "
        "Install the `iputils-ping` (or equivalent) package.",
    )
    _assert(
        os.access(ping_path, os.X_OK),
        f"`ping` was found at {ping_path!r} but is not executable.",
    )


@pytest.mark.timeout(15)
def test_loopback_ping_succeeds_for_three_packets():
    """
    Send exactly three ICMP echo-requests to 127.0.0.1 and verify that
    all packets are returned.  This confirms the local network stack
    is functional before the learner proceeds with the exercise.
    """
    ping_cmd = ["ping", "-c", "3", "127.0.0.1"]

    try:
        completed = subprocess.run(
            ping_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=10,
        )
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(
            "Attempted to execute `ping` but it could not be found. "
            "Ensure `ping` is installed and on PATH.",
            pytrace=False,
        )
    except subprocess.TimeoutExpired:  # pragma: no cover
        pytest.fail(
            "The `ping` command to 127.0.0.1 hung or took too long.",
            pytrace=False,
        )

    # Basic process exit status.
    _assert(
        completed.returncode == 0,
        textwrap.dedent(
            f"""
            Expected `ping -c 3 127.0.0.1` to exit with status 0, but
            got {completed.returncode}.  Stderr was:

            {completed.stderr.strip() or '<empty>'}
            """
        ),
    )

    # Parse stdout for packet statistics.
    # Example line:
    # "3 packets transmitted, 3 received, 0% packet loss, time 2040ms"
    stats_line = ""
    for line in completed.stdout.splitlines():
        if " packets transmitted" in line and " received" in line:
            stats_line = line.strip()
            break

    _assert(
        stats_line,
        "Could not find the packet statistics line in `ping` output:\n\n"
        f"{completed.stdout}",
    )

    try:
        transmitted = int(stats_line.split(" packets transmitted")[0])
        received_part = stats_line.split(",")[1].strip()
        received = int(received_part.split()[0])
    except (ValueError, IndexError):  # pragma: no cover
        pytest.fail(
            "Failed to parse the statistics line from `ping` output:\n\n"
            f"{stats_line}",
            pytrace=False,
        )

    _assert(
        transmitted == 3 and received == 3,
        f"Expected 3 packets transmitted and 3 received, but got "
        f"{transmitted} transmitted and {received} received.",
    )