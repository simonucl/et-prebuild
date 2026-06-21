# test_initial_state.py
#
# Pytest suite validating the *initial* operating-system state **before**
# the learner attempts the “network-diagnostic” task.
#
# What MUST be true *before* the task:
#   1. Directory /home/user/network_checks   – MUST NOT exist yet.
#   2. File      /home/user/network_checks/routes.log – MUST NOT exist yet.
#   3. The `ip` utility must be available in $PATH.
#   4. `ip route` must execute successfully and emit at least one non-empty
#      line whose first token is “default” (so the later grader’s assumptions
#      hold true).
#
# Any failure message should clearly indicate what is wrong with the
# provisioning host before the exercise starts.

import os
import shutil
import subprocess
import pytest

NETWORK_DIR = "/home/user/network_checks"
ROUTES_LOG = "/home/user/network_checks/routes.log"


def test_network_directory_absent_initially():
    """
    The working directory must NOT pre-exist. Its creation is part of
    the student’s task, so we ensure the sandbox starts clean.
    """
    assert not os.path.exists(
        NETWORK_DIR
    ), (
        f"The directory {NETWORK_DIR!r} already exists. The exercise "
        "expects a clean slate so the learner can create it."
    )


def test_routes_log_absent_initially():
    """
    No leftover log file should be present before the learner runs
    their one-liner.  An existing file could hide implementation errors.
    """
    assert not os.path.exists(
        ROUTES_LOG
    ), (
        f"The file {ROUTES_LOG!r} already exists. It must not exist "
        "prior to the learner's command."
    )


def test_ip_command_available():
    """
    The system needs the `ip` command (from iproute2) so the learner
    can run `ip route`.  Verify it is on PATH.
    """
    ip_path = shutil.which("ip")
    assert ip_path, (
        "The `ip` utility is not available on PATH. "
        "Install the iproute2 package so `ip route` can be executed."
    )


def test_ip_route_produces_expected_output():
    """
    Run `ip route` once to make sure:
      * it exits with return code 0,
      * it outputs at least one non-empty line,
      * the first token of the first line is the word ``default``.
    These conditions are prerequisites for the later grading rubric.
    """
    try:
        completed = subprocess.run(
            ["ip", "route"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        pytest.skip("`ip` command not found; handled in previous test.")
        return

    output = completed.stdout
    assert output, "`ip route` produced no output; the routing table appears empty."
    first_line = output.splitlines()[0]
    first_token = first_line.strip().split()[0] if first_line.strip() else ""
    assert (
        first_token == "default"
    ), (
        "The first line of `ip route` output must begin with 'default' "
        f"for the subsequent grader, but got: {first_line!r}"
    )