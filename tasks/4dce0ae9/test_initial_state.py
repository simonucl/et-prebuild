# test_initial_state.py
#
# This pytest file validates the *initial* operating-system state
# before the student performs any action for the “incident log” task.
#
# REQUIRED INITIAL CONDITIONS (pre-exercise)
#   1. The directory /home/user/incident_logs MUST **NOT** exist.
#   2. Consequently, the file  /home/user/incident_logs/local_ping.log
#      MUST **NOT** exist either.
#
# If either the directory or the file is already present, the test
# will fail with a clear, actionable message.
#
# Only Python’s standard library and pytest are used in order to keep
# the test runner environment self-contained.

import os
from pathlib import Path
import pytest


INCIDENT_DIR = Path("/home/user/incident_logs")
LOG_FILE = INCIDENT_DIR / "local_ping.log"


def test_initial_filesystem_state():
    """
    Assert that no remnants of a previous run exist.

    The run-book instructs the student to create the directory and log
    file.  Therefore, neither should exist at the outset.
    """

    # 1. The incident directory must be absent.
    if INCIDENT_DIR.exists():
        pytest.fail(
            f"Pre-exercise clean-up required:\n"
            f"  The directory {INCIDENT_DIR} already exists, but it should "
            f"NOT be present before the exercise begins.\n"
            f"  Please remove or rename this directory and start over."
        )

    # 2. If the directory is absent, the specific log file cannot exist,
    #    but we assert explicitly for completeness and clarity.
    if LOG_FILE.exists():
        pytest.fail(
            f"Pre-exercise clean-up required:\n"
            f"  The file {LOG_FILE} already exists, but it should NOT be "
            f"present before the exercise begins.\n"
            f"  Please remove this file and start over."
        )