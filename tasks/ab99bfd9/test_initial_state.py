# test_initial_state.py
#
# This suite validates that the machine is still in a **clean** state
# before the student starts the task.  None of the capacity-planning
# artefacts should exist yet.  If any do, the environment is considered
# “dirty” and the tests will fail with an explanatory message.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
WS_DIR = HOME / "capacity_planning"
SNAPSHOT_FILE = WS_DIR / "snapshot_001.log"
VERIFICATION_FILE = WS_DIR / "verification.log"


def _assert_absent(path: pathlib.Path):
    """
    Helper that asserts the given path does NOT exist on the filesystem.
    Produces a clear, human-friendly failure message if the assertion fails.
    """
    assert not path.exists(), (
        f"The path {path} already exists. The starting environment must be "
        f"clean so the student can create it during the exercise."
    )


def test_capacity_planning_directory_absent():
    """
    The directory /home/user/capacity_planning must NOT exist yet.
    """
    _assert_absent(WS_DIR)


def test_snapshot_file_absent():
    """
    The snapshot log file must NOT exist before the student runs the commands.
    """
    _assert_absent(SNAPSHOT_FILE)


def test_verification_file_absent():
    """
    The verification log file must NOT exist before the student runs the commands.
    """
    _assert_absent(VERIFICATION_FILE)