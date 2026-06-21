# test_initial_state.py
#
# This test-suite verifies that a learner starts from a clean slate
# before running any of the commands described in the assignment.
#
# What **must NOT** exist yet:
#   • /home/user/iot_edge/                (directory)
#   • /home/user/iot_edge/iot_devices.db  (SQLite database file)
#   • /home/user/iot_edge/offline_devices.log (CSV log file)
#
# If any of these pre-exercise artefacts are already present the test
# will fail, because the learner’s commands should be responsible for
# creating them.

import os
import stat
import pytest

HOME = "/home/user"
IOT_DIR = os.path.join(HOME, "iot_edge")
DB_FILE = os.path.join(IOT_DIR, "iot_devices.db")
LOG_FILE = os.path.join(IOT_DIR, "offline_devices.log")


@pytest.mark.parametrize(
    "path,kind",
    [
        (IOT_DIR, "directory"),
        (DB_FILE, "file"),
        (LOG_FILE, "file"),
    ],
)
def test_artifacts_do_not_exist_yet(path: str, kind: str):
    """
    Ensure that the IoT directory, database, and log file are absent
    before the learner starts the task.
    """
    assert not os.path.exists(path), (
        f"The {kind} {path!r} already exists. "
        "Start with a clean state so the exercise can create it."
    )


def test_home_directory_exists_and_is_directory():
    """
    Sanity-check that /home/user itself is present and is a directory.
    """
    assert os.path.exists(HOME), (
        f"The expected home directory {HOME!r} does not exist. "
        "The test environment is misconfigured."
    )
    st = os.stat(HOME)
    assert stat.S_ISDIR(st.st_mode), (
        f"The path {HOME!r} exists but is not a directory."
    )