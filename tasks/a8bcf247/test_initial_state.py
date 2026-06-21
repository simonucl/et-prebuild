# test_initial_state.py
#
# Pytest suite that validates the pristine filesystem layout *before* the
# student runs any command.  These tests assert that the exercise is set up
# exactly as the specification describes.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
ARTIFACTS_DIR = HOME / "artifacts"

# ---------------------------------------------------------------------------
# Expected layout according to the exercise description
# ---------------------------------------------------------------------------

EXPECTED_TMP_FILES = {
    ARTIFACTS_DIR / "repoA" / "releases" / "staging.tmp",
    ARTIFACTS_DIR / "repoA" / "releases" / "unused.tmp",
    ARTIFACTS_DIR / "repoB" / "snapshots" / "cache.tmp",
}

EXPECTED_KEEP_FILES = {
    ARTIFACTS_DIR / "repoA" / "releases" / "libfoo-1.0.jar",
    ARTIFACTS_DIR / "repoB" / "snapshots" / "libbar-2.3.jar",
    ARTIFACTS_DIR / "readme.md",
}


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def collect_files_with_suffix(root: Path, suffix: str):
    """Return a set of Paths for every file under *root* that ends with *suffix*."""
    return {p for p in root.rglob(f"*{suffix}") if p.is_file()}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_artifacts_directory_exists():
    """The root artifacts directory must be present and be a directory."""
    assert ARTIFACTS_DIR.exists(), f"Expected directory {ARTIFACTS_DIR} to exist."
    assert ARTIFACTS_DIR.is_dir(), f"{ARTIFACTS_DIR} exists but is not a directory."


@pytest.mark.parametrize("path", sorted(EXPECTED_TMP_FILES))
def test_each_tmp_file_exists(path: Path):
    """Every .tmp placeholder file the student must delete later should exist now."""
    assert path.exists(), f"Expected .tmp file {path} to exist before cleanup."
    assert path.is_file(), f"Expected .tmp path {path} to be a regular file."


def test_no_extra_tmp_files_present():
    """
    Exactly three *.tmp files should be present anywhere under /home/user/artifacts.
    This guards against accidental fixture drift.
    """
    found_tmp_files = collect_files_with_suffix(ARTIFACTS_DIR, ".tmp")
    assert found_tmp_files == EXPECTED_TMP_FILES, (
        "Unexpected difference in *.tmp placeholder files.\n"
        f"Expected exactly: {sorted(EXPECTED_TMP_FILES)}\n"
        f"Found:            {sorted(found_tmp_files)}"
    )


@pytest.mark.parametrize("path", sorted(EXPECTED_KEEP_FILES))
def test_files_that_should_remain_are_present(path: Path):
    """Verify that all files which must *not* be touched are in place."""
    assert path.exists(), f"Required keep-file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."


def test_purge_directory_not_yet_created():
    """
    The audit directory (/home/user/purge) shouldn't exist before the student
    runs their solution. Its presence would indicate a prior, possibly
    contaminating, execution.
    """
    purge_dir = HOME / "purge"
    assert not purge_dir.exists(), (
        f"Directory {purge_dir} should not exist before the cleanup command runs."
    )