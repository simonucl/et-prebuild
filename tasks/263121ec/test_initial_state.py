# test_initial_state.py
#
# This test-suite validates the *initial* operating-system / filesystem
# state **before** the student performs any action for the assignment
# “Node.js process snapshot”.
#
# It verifies that
#   1. No file already exists at the required output path
#      /home/user/webdev/logs/node_process_summary.log
#   2. There is currently no running Node.js process
#
# NOTE: The directory /home/user/webdev/logs is *allowed* to exist
#       beforehand (the task says “create if it does not yet exist”),
#       therefore the tests do NOT assert its absence—only that the
#       specific output file is not present.

import os
import subprocess
import sys
from pathlib import Path

import pytest

OUTPUT_FILE = Path("/home/user/webdev/logs/node_process_summary.log")


def _list_running_commands() -> list[str]:
    """
    Return the list of command names (basename of argv[0] a.k.a COMM column)
    for all running processes that the current user can see.
    """
    try:
        ps = subprocess.run(
            ["ps", "-eo", "comm"],
            text=True,
            capture_output=True,
            check=True,
        )
    except FileNotFoundError:  # Extremely unlikely in POSIX-like container
        pytest.skip("`ps` command not available on this system")
    # The first line of `ps` output is the header "COMMAND" (or similar);
    # ignore it.
    return [line.strip() for line in ps.stdout.splitlines()[1:] if line.strip()]


def test_output_file_does_not_exist_yet():
    """
    The report file must NOT exist *before* the student runs their command.
    """
    assert not OUTPUT_FILE.exists(), (
        f"The file {OUTPUT_FILE} already exists, "
        "but it should be created by the student's one-liner. "
        "Remove the file and re-run the tests."
    )


def test_no_node_process_is_running_initially():
    """
    The evaluation container is guaranteed to start with *zero* Node.js
    processes.  Confirm that guarantee so that later tests can rely on it.
    """
    running_cmds = _list_running_commands()

    # We test for exact command names 'node' and 'nodejs' only; this avoids
    # accidental matches like 'notifyd', 'anode', etc.
    offending = [cmd for cmd in running_cmds if cmd in {"node", "nodejs"}]

    assert not offending, (
        "Unexpected Node.js processes are already running:\n"
        + "\n".join(offending)
        + "\nThe initial state must have no such processes."
    )