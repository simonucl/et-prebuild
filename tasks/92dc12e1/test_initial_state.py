# test_initial_state.py
#
# This pytest suite verifies that the workspace starts **clean** before the
# student performs any actions required by the “dotenv” task.  In other words,
# the directory /home/user/observability/env/ and the two files that must be
# created later (.env and env_load.log) must NOT exist at this point.
#
# If any of these artefacts are already present, the tests will fail with a
# clear, actionable message so the learner knows the environment is not in the
# expected initial state.

import os
import pytest

BASE_DIR = "/home/user/observability/env"
ENV_FILE = os.path.join(BASE_DIR, ".env")
LOG_FILE = os.path.join(BASE_DIR, "env_load.log")


def _pretty(path: str) -> str:  # helper for consistent error messages
    return f"`{path}`"


@pytest.mark.order(1)
def test_env_file_absent():
    """
    The canonical dotenv file must *not* exist before the student creates it.
    """
    assert not os.path.exists(ENV_FILE), (
        f"{_pretty(ENV_FILE)} already exists. "
        "Start from a clean slate by removing or renaming this file."
    )


@pytest.mark.order(2)
def test_log_file_absent():
    """
    The one-shot log proving the variables were exported must *not* exist yet.
    """
    assert not os.path.exists(LOG_FILE), (
        f"{_pretty(LOG_FILE)} already exists. "
        "It will be generated after you source the .env file—please remove it first."
    )


@pytest.mark.order(3)
def test_directory_state():
    """
    The target directory should either be completely absent or, if it does
    exist, it must *not* contain the final artefacts.
    """
    if not os.path.exists(BASE_DIR):
        # Ideal: the directory hierarchy has not been created yet.
        return

    # The directory exists: ensure it does not already contain the required files.
    assert os.path.isdir(BASE_DIR), (
        f"{_pretty(BASE_DIR)} exists but is not a directory—please remove or rename it."
    )

    unexpected_entries = [name for name in os.listdir(BASE_DIR)
                          if name in {".env", "env_load.log"}]

    assert not unexpected_entries, (
        f"{_pretty(BASE_DIR)} should not already contain {', '.join(unexpected_entries)}. "
        "Remove these files before starting the task."
    )