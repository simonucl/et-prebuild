# test_initial_state.py
#
# Pytest suite that verifies the filesystem **before** the student runs
# their one-liner.  It asserts that the deployment tree is set up exactly
# as described in the task statement, i.e. the “current” symlink still
# points to v1.2.2 and all required directories / files are present.
#
# Any failure message is written so that the student immediately knows
# what prerequisite element is missing or incorrect.

import os
from pathlib import Path
import pytest

# Base paths used throughout the assertions
BASE_DIR = Path("/home/user/releases")
V122_DIR = BASE_DIR / "v1.2.2"
V123_DIR = BASE_DIR / "v1.2.3"
CURRENT_LINK = BASE_DIR / "current"


def _assert_is_dir(p: Path):
    """Utility: assert that path exists and is a directory."""
    assert p.exists(), f"Expected directory {p} is missing."
    assert p.is_dir(), f"Expected directory {p} exists but is not a directory."


def _assert_is_file(p: Path):
    """Utility: assert that path exists and is a regular file."""
    assert p.exists(), f"Expected file {p} is missing."
    assert p.is_file(), f"Expected file {p} exists but is not a regular file."


def test_releases_directory_exists():
    """/home/user/releases must exist and be a directory."""
    _assert_is_dir(BASE_DIR)


@pytest.mark.parametrize("build_dir", [V122_DIR, V123_DIR])
def test_version_directories_exist(build_dir: Path):
    """Both v1.2.2 and v1.2.3 directories must exist."""
    _assert_is_dir(build_dir)


@pytest.mark.parametrize(
    "app_path",
    [
        V122_DIR / "app.jar",
        V123_DIR / "app.jar",
    ],
)
def test_app_jars_exist(app_path: Path):
    """Each build directory must contain an app.jar file."""
    _assert_is_file(app_path)


def test_current_symlink_points_to_v122():
    """
    The pre-existing “current” symlink must exist and resolve to v1.2.2.
    This is the state BEFORE the student changes it.
    """
    # Does the symlink itself exist?
    assert CURRENT_LINK.exists(), f"Symbolic link {CURRENT_LINK} is missing."
    # Is it actually a symlink (not a dir / file)?
    assert CURRENT_LINK.is_symlink(), f"{CURRENT_LINK} exists but is not a symbolic link."

    # Resolve the symlink target to its canonical path
    resolved = CURRENT_LINK.resolve()  # follows symlinks

    assert (
        resolved == V122_DIR
    ), f"{CURRENT_LINK} should resolve to {V122_DIR} before the task starts, but it resolves to {resolved}."