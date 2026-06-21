# test_initial_state.py
#
# This pytest suite validates the *starting* filesystem state **before**
# the learner begins the clean-up/migration task for “alpha_app”.
#
# It intentionally checks ONLY the pre-existing materials and stays away
# from every path that the learner is expected to create later.  If any
# of these tests fail, the learner is not starting from the prescribed
# baseline.

import os
import stat
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DOWNLOADS_DIR = Path("/home/user/downloads/alpha_assets")
DEV_DIR = Path("/home/user/dev")

EXPECTED_FILES = {
    "app.py",
    "helpers.py",
    "test_app.py",
    "test_helpers.py",
    "overview.md",
    "CHANGELOG.md",
    "Dockerfile",
    "LICENSE",
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _assert_is_regular_file(p: Path):
    """Assert that *p* exists and is a regular file (not dir, not symlink)."""
    assert p.exists(), f"Expected file {p} is missing."
    st_mode = p.stat().st_mode
    assert stat.S_ISREG(st_mode), f"{p} exists but is not a regular file."


def _dir_listing_without_dotfiles(directory: Path):
    """List non-hidden entries in *directory*."""
    return {entry.name for entry in directory.iterdir() if not entry.name.startswith(".")}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_downloads_directory_exists_and_is_directory():
    assert DOWNLOADS_DIR.exists(), f"{DOWNLOADS_DIR} does not exist."
    assert DOWNLOADS_DIR.is_dir(), f"{DOWNLOADS_DIR} exists but is not a directory."


def test_downloads_directory_contains_exact_expected_files():
    actual_files = _dir_listing_without_dotfiles(DOWNLOADS_DIR)
    assert actual_files == EXPECTED_FILES, (
        "The contents of the downloads directory do not match the expected set.\n"
        f"Expected: {sorted(EXPECTED_FILES)}\n"
        f"Actual  : {sorted(actual_files)}"
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_FILES))
def test_each_expected_downloads_file_is_regular_file(filename):
    path = DOWNLOADS_DIR / filename
    _assert_is_regular_file(path)


def test_no_subdirectories_or_symlinks_inside_downloads_dir():
    for entry in DOWNLOADS_DIR.iterdir():
        if entry.name.startswith("."):
            # Hidden files/directories are not expected; flag them.
            pytest.fail(f"Unexpected hidden entry found in downloads dir: {entry}")
        assert entry.is_file(), (
            f"Unexpected non-file entry found in downloads dir: {entry} "
            "(should contain only regular files)."
        )
        assert not entry.is_symlink(), f"Unexpected symlink found in downloads dir: {entry}"


def test_dev_directory_exists_and_is_writable(tmp_path):
    # Basic sanity check that /home/user/dev is ready to receive new content.
    assert DEV_DIR.exists(), f"{DEV_DIR} does not exist."
    assert DEV_DIR.is_dir(), f"{DEV_DIR} exists but is not a directory."
    # Attempt to create & remove a temporary file to ensure write permission.
    temp_file = DEV_DIR / ".__write_test__"
    try:
        temp_file.write_text("ok")
        assert temp_file.exists(), (
            f"Unable to create files inside {DEV_DIR}; "
            "directory must be writable by the learner."
        )
    finally:
        temp_file.unlink(missing_ok=True)