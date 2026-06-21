# test_initial_state.py
#
# This test-suite validates the *initial* operating-system / filesystem
# state before the student performs any actions for the “deployment
# package” task.  If any of these tests fail it means the environment
# is **already** in the final (or a polluted) state and therefore the
# exercise would be meaningless to run.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")

EDGE_CONFIGS_DIR = HOME / "edge_configs"
EDGE_DEVICE_FILE = EDGE_CONFIGS_DIR / "edge_device_list.txt"

DEPLOY_PKG_DIR = HOME / "deploy_package"
DEVICES_TO_PUSH_FILE = DEPLOY_PKG_DIR / "devices_to_push.list"
DEPLOY_LOG_FILE = DEPLOY_PKG_DIR / "deploy.log"


@pytest.mark.parametrize(
    "path_obj, should_exist",
    [
        (EDGE_CONFIGS_DIR, False),
        (EDGE_DEVICE_FILE, False),
        (DEPLOY_PKG_DIR, False),
        (DEVICES_TO_PUSH_FILE, False),
        (DEPLOY_LOG_FILE, False),
    ],
)
def test_objects_do_not_exist_yet(path_obj: Path, should_exist: bool):
    """
    None of the directories or files that the student is supposed to create
    should exist *before* the exercise starts.
    """
    exists = path_obj.exists()
    assert exists is should_exist, (
        f"Expected {'no ' if not should_exist else ''}{path_obj} to exist "
        f"before the student begins, but it {'does' if exists else 'does NOT'}."
    )


def test_home_directory_present():
    """
    Sanity-check: /home/user itself must be present, writable,
    and a directory.  This ensures the test environment is sensible.
    """
    assert HOME.exists(), "/home/user is missing on the test runner."
    assert HOME.is_dir(), "/home/user exists but is not a directory."
    # We cannot guarantee write permissions in every CI system,
    # but we can at least check that the path is not a file.