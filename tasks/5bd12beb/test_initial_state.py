# test_initial_state.py
#
# Pytest suite to validate the **initial** state of the operating system
# before the student carries out any actions for the “capacity-planning” task.
#
# The student is expected to CREATE the following as part of the exercise:
#   /home/user/capacity/
#   /home/user/capacity/.env
#   /home/user/capacity/logs/
#   /home/user/capacity/logs/memory_usage.log
#
# Therefore, none of the above should exist at the outset.  These tests
# assert their non-existence so that if anything is already present, the
# learner receives a clear, actionable failure message.

import os
import stat
import pytest

HOME = "/home/user"
CAPACITY_DIR = os.path.join(HOME, "capacity")
ENV_FILE = os.path.join(CAPACITY_DIR, ".env")
LOGS_DIR = os.path.join(CAPACITY_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, "memory_usage.log")


@pytest.mark.parametrize(
    "path,description",
    [
        (CAPACITY_DIR, "directory /home/user/capacity"),
        (ENV_FILE, "file /home/user/capacity/.env"),
        (LOGS_DIR, "directory /home/user/capacity/logs"),
        (LOG_FILE, "file /home/user/capacity/logs/memory_usage.log"),
    ],
)
def test_path_does_not_exist_yet(path, description):
    """
    Ensure none of the task-specific files or directories exist
    before the student performs the required steps.
    """
    assert not os.path.exists(path), (
        f"Unexpected pre-existing {description!s}. "
        "The working directory should be clean before you start the task."
    )


def test_no_partial_structures():
    """
    If /home/user/capacity happens to exist for unrelated reasons,
    ensure it is completely empty.  This guards against leftover
    artifacts that might give a false sense of completion.
    """
    if not os.path.exists(CAPACITY_DIR):
        pytest.skip(f"{CAPACITY_DIR} does not exist — nothing further to check.")

    # If it exists, confirm it's a directory.
    assert stat.S_ISDIR(os.stat(CAPACITY_DIR).st_mode), (
        f"{CAPACITY_DIR} exists but is not a directory."
    )

    # Directory must be empty at the start of the exercise.
    leftover = os.listdir(CAPACITY_DIR)
    assert leftover == [], (
        f"{CAPACITY_DIR} should be empty before starting, "
        f"but it already contains: {leftover}"
    )