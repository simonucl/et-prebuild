# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student writes or runs `setup_test_env.sh`.
#
# These tests purposefully avoid checking for any artefacts that the student
# is expected to create (the shell script itself, log files, environment
# directories, etc.).  Instead, they make sure that the prerequisites
# documented in the task description are satisfied so that the student
# can complete the assignment without environment-related surprises.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
SCRIPTS_DIR = HOME / "scripts"
TEST_ENVS_DIR = HOME / "test_envs"


def _is_writable(path: Path) -> bool:
    """
    Helper: return True if the current user can create files within `path`.
    """
    return os.access(str(path), os.W_OK)


def _is_executable(path: Path) -> bool:
    """
    Helper: return True if the current user can traverse / execute `path`.
    Directory "execute" permission == ability to traverse.
    """
    return os.access(str(path), os.X_OK)


def test_scripts_directory_exists_and_is_writable():
    """
    The assignment guarantees that `/home/user/scripts` exists
    and is writable by the current user.  The forthcoming shell
    script will be placed there.
    """
    assert SCRIPTS_DIR.exists(), (
        f"Required directory {SCRIPTS_DIR} is missing. "
        "Please create it so the student can place their script."
    )
    assert SCRIPTS_DIR.is_dir(), (
        f"{SCRIPTS_DIR} exists but is not a directory."
    )

    assert _is_writable(SCRIPTS_DIR) and _is_executable(SCRIPTS_DIR), (
        f"Current user lacks write/execute permissions on {SCRIPTS_DIR}. "
        "Ensure the directory is writable and traversable."
    )


@pytest.mark.parametrize(
    "dir_path, description",
    [
        (HOME, "home directory"),
        (SCRIPTS_DIR, "scripts directory"),
        (TEST_ENVS_DIR.parent, "parent of test_envs directory"),  # i.e. /home/user
    ],
)
def test_expected_directories_are_traversable(dir_path: Path, description: str):
    """
    Sanity-check that fundamental directories are traversable (execute bit set).
    This avoids odd failures when the student attempts to create sub-directories.
    """
    assert _is_executable(dir_path), (
        f"Cannot traverse {description} ({dir_path}). "
        "Check directory permissions."
    )


def test_test_envs_directory_state_and_permissions():
    """
    `/home/user/test_envs` *may or may not* exist initially.
    If it does exist, it must be a writable directory so the
    student's script can create new environment folders and the
    central log file.  If it does not exist, the parent directory
    must be writable so that it can be created later.
    """
    if TEST_ENVS_DIR.exists():
        assert TEST_ENVS_DIR.is_dir(), (
            f"{TEST_ENVS_DIR} exists but is not a directory."
        )
        assert _is_writable(TEST_ENVS_DIR), (
            f"Directory {TEST_ENVS_DIR} exists but is not writable. "
            "Ensure the student can write to it."
        )
    else:
        # Directory absent: make sure we *could* create it.
        assert _is_writable(TEST_ENVS_DIR.parent), (
            f"{TEST_ENVS_DIR} does not exist and its parent directory "
            f"{TEST_ENVS_DIR.parent} is not writable. The student will be "
            "unable to create the required directory."
        )