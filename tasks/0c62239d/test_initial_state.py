# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present **before** the student performs any cut-over actions.  It asserts
# that only the legacy v0.9 release exists, that the “current” symlink still
# points to it, and that none of the artefacts required for the new v1.0.0
# release have been created yet.

import os
import stat
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helper constants
# ---------------------------------------------------------------------------
HOME = Path("/home/user")
REPO_ROOT = HOME / "repos" / "ci-cd-scripts"
RELEASES_DIR = REPO_ROOT / "releases"
LEGACY_RELEASE_DIR = RELEASES_DIR / "v0.9"
NEW_RELEASE_DIR = RELEASES_DIR / "v1.0.0"
CURRENT_SYMLINK = REPO_ROOT / "current"
SHARED_DIR = REPO_ROOT / "shared"
LOG_FILE = HOME / "ci_cd_symlink_update.log"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def assert_is_symlink(path: Path):
    assert path.exists(), f"Expected symlink at {path} to exist."
    assert path.is_symlink(), f"Expected {path} to be a symlink."


def assert_is_dir(path: Path):
    assert path.exists(), f"Expected directory {path} to exist."
    assert path.is_dir(), f"Expected {path} to be a directory."


def assert_not_exists(path: Path):
    assert not path.exists(), f"{path} should NOT exist at this stage."


# ---------------------------------------------------------------------------
# Tests for initial state
# ---------------------------------------------------------------------------
def test_repo_root_exists():
    """Verify that the repository root and basic skeleton exist."""
    assert_is_dir(REPO_ROOT)
    assert_is_dir(RELEASES_DIR)


def test_legacy_release_present_with_deploy_script():
    """The legacy v0.9 release directory and its deploy.sh must exist."""
    assert_is_dir(LEGACY_RELEASE_DIR)

    deploy_sh = LEGACY_RELEASE_DIR / "deploy.sh"
    assert deploy_sh.exists(), f"Expected legacy deploy script at {deploy_sh}."
    assert deploy_sh.is_file(), f"{deploy_sh} should be a regular file."

    # Optionally confirm it is executable for good measure.
    st_mode = deploy_sh.stat().st_mode
    assert (
        st_mode & stat.S_IXUSR
    ), f"{deploy_sh} should be executable by the owner (legacy invariant)."


def test_current_symlink_points_to_legacy_release():
    """
    The 'current' symlink must exist and resolve (after realpath) to the
    legacy v0.9 directory.
    """
    assert_is_symlink(CURRENT_SYMLINK)

    resolved_path = CURRENT_SYMLINK.resolve()
    expected = LEGACY_RELEASE_DIR.resolve()
    assert (
        resolved_path == expected
    ), f"'current' symlink should resolve to {expected}, but resolves to {resolved_path}."


def test_shared_directory_absent():
    """No shared/ directory should be present yet."""
    assert_not_exists(SHARED_DIR)


def test_log_file_absent():
    """The cut-over log must *not* be present before the procedure."""
    assert_not_exists(LOG_FILE)


def test_new_release_not_yet_created():
    """The new v1.0.0 release directory and its artefacts must not exist yet."""
    assert_not_exists(NEW_RELEASE_DIR)
    assert_not_exists(REPO_ROOT / "releases" / "v1.0.0" / "deploy.sh")
    assert_not_exists(REPO_ROOT / "releases" / "v1.0.0" / "config.yml")