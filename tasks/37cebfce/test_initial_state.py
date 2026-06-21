# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state **before**
# the student has performed any actions for the “artifact manager” task.
#
# Expectations for a pristine container:
#   • The directory /home/user/artifactory exists.
#   • That directory is completely empty (no sub-directories, no files).
#   • None of the target paths that the exercise later asks the student
#     to create are present yet.
#
# If any of these conditions are violated, the student is starting from
# an unexpected environment and the remainder of the automated checker
# would produce misleading results.

from pathlib import Path
import os
import stat
import pytest

ARTIFACTORY_ROOT = Path("/home/user/artifactory")

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _full_paths_to_be_created():
    """
    All paths that the *student* will be asked to create later on.
    These MUST NOT exist in the pristine container.
    """
    return [
        ARTIFACTORY_ROOT / "config",
        ARTIFACTORY_ROOT / "config" / "users.csv",
        ARTIFACTORY_ROOT / "logs",
        ARTIFACTORY_ROOT / "logs" / "permission_changes_2023-01-15.log",
        ARTIFACTORY_ROOT / "repos",
        ARTIFACTORY_ROOT / "repos" / "lib-utils-binaries",
        ARTIFACTORY_ROOT / "repos" / "lib-utils-binaries" / "permissions.yml",
    ]

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_artifactory_root_exists_and_is_directory():
    assert ARTIFACTORY_ROOT.exists(), (
        f"Expected directory {ARTIFACTORY_ROOT} to be present, "
        "but it does not exist."
    )
    assert ARTIFACTORY_ROOT.is_dir(), (
        f"Expected {ARTIFACTORY_ROOT} to be a directory, "
        "but it is not."
    )

def test_artifactory_root_is_empty():
    contents = list(ARTIFACTORY_ROOT.iterdir())
    assert not contents, (
        f"Expected {ARTIFACTORY_ROOT} to be empty in the initial state, "
        f"but it contains: {[p.name for p in contents]}"
    )

@pytest.mark.parametrize("path", _full_paths_to_be_created())
def test_no_target_paths_exist_yet(path: Path):
    assert not path.exists(), (
        f"Path {path} already exists. The initial container should only "
        f"contain the empty directory {ARTIFACTORY_ROOT}. "
        "Please start from a clean environment."
    )

def test_artifactory_root_permissions_reasonable():
    """
    The directory should at least be accessible (owner read/write/execute).
    We don't enforce the exact mode (could be 755, 700, etc.), but we do
    verify that it is a directory and owner can r/w/x it; otherwise the
    student would be unable to continue.
    """
    mode = ARTIFACTORY_ROOT.stat().st_mode
    owner_perms = stat.S_IRWXU  # 0o700
    assert mode & owner_perms == owner_perms, (
        f"The owner does not have rwx permissions on {ARTIFACTORY_ROOT}. "
        "Please ensure the directory is usable by the current user."
    )