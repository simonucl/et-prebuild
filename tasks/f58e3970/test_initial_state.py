# test_initial_state.py
#
# Pytest suite that validates the *initial* OS / filesystem state
# BEFORE the student performs the required actions for the rollout
# task.  If any of these tests fail, it means the environment is
# already “dirty” (e.g., someone has pre-created the venv or the
# setup.log file), which would invalidate the task assumptions.
#
# The tests intentionally confirm ABSENCE of the expected artefacts.
# Once the student completes the task, a separate test suite will
# check for their PRESENCE and correctness.

import os
import stat
import pytest

HOME = "/home/user"
ROLLOUT_DIR = os.path.join(HOME, "rollout")
VENV_PATH = os.path.join(ROLLOUT_DIR, "rollout-env")
LOG_PATH = os.path.join(ROLLOUT_DIR, "setup.log")


def _human_readable_mode(path: str) -> str:
    """
    Helper to provide a human-readable file-mode string in octal,
    e.g. '0o755'.  Returns '<missing>' if the path does not exist.
    """
    if not os.path.exists(path):
        return "<missing>"
    return oct(os.stat(path).st_mode & 0o777)


@pytest.mark.describe("Initial filesystem state is clean")
def test_venv_absent():
    """
    The virtual-environment directory MUST NOT exist yet.
    """
    assert not os.path.exists(VENV_PATH), (
        f"Expected no virtual-environment at {VENV_PATH!r}, but it already "
        f"exists with mode {_human_readable_mode(VENV_PATH)}.  Remove it so "
        "the student can create a fresh venv during the task."
    )


def test_setup_log_absent():
    """
    The setup.log file MUST NOT exist yet.
    """
    assert not os.path.exists(LOG_PATH), (
        f"Expected no setup log at {LOG_PATH!r}, but it already exists "
        f"with mode {_human_readable_mode(LOG_PATH)}.  Remove it so the "
        "student can generate a fresh, correctly formatted log."
    )


def test_parent_directory_state():
    """
    The parent directory /home/user/rollout is allowed to exist or not;
    however, if it DOES exist, it must be a *directory* and writable by
    the current user.  This ensures the student has a place to create
    the venv and log file.
    """
    if os.path.exists(ROLLOUT_DIR):
        assert os.path.isdir(ROLLOUT_DIR), (
            f"{ROLLOUT_DIR!r} exists but is not a directory."
        )
        # Check write permission for the current user
        mode = os.stat(ROLLOUT_DIR).st_mode
        is_writable = bool(mode & stat.S_IWUSR)
        assert is_writable, (
            f"{ROLLOUT_DIR!r} exists but is not writable by the current user "
            f"(mode {_human_readable_mode(ROLLOUT_DIR)})."
        )