# test_initial_state.py
#
# This pytest file validates the *initial* state of the operating-system
# filesystem **before** the student performs any actions for the
# “archive-utils” assignment.  It purposefully verifies only the items that
# must already exist and also confirms that none of the artefacts the
# student is supposed to create (archives directory, .tar.gz files, log
# file, etc.) are present yet.

import io
import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/projects/archive-utils")
SUBDIRS = {
    "alpha": (
        ("file1.txt", "Alpha file 1\n"),
        ("file2.txt", "Alpha file 2\n"),
    ),
    "beta": (
        ("file1.txt", "Beta file 1\n"),
        ("file2.txt", "Beta file 2\n"),
    ),
    "gamma": (
        ("file1.txt", "Gamma file 1\n"),
        ("file2.txt", "Gamma file 2\n"),
    ),
}

ARCHIVES_DIR = BASE_DIR / "archives"
LOG_FILE = BASE_DIR / "archive_activity.log"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _read_text(path: Path) -> str:
    """
    Read a text file using UTF-8, returning its full contents.
    """
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_base_directory_exists():
    """The main project directory must exist and be a directory."""
    assert BASE_DIR.exists(), f"Expected directory {BASE_DIR} to exist."
    assert BASE_DIR.is_dir(), f"Expected {BASE_DIR} to be a directory."


def test_only_expected_subdirectories_present():
    """
    The base directory must contain exactly the three expected sub-directories
    (alpha, beta, gamma) and *no* other files or directories.
    """
    dir_entries = {p.name for p in BASE_DIR.iterdir() if p.is_dir()}
    file_entries = {p.name for p in BASE_DIR.iterdir() if p.is_file()}

    expected_dirs = set(SUBDIRS.keys())

    # Directories ------------------------------------------------------------
    assert dir_entries == expected_dirs, (
        f"Expected sub-directories {sorted(expected_dirs)} inside {BASE_DIR}, "
        f"found {sorted(dir_entries)}."
    )

    # Files ------------------------------------------------------------------
    assert file_entries == set(), (
        f"Did not expect any files in {BASE_DIR} yet, but found: "
        f"{sorted(file_entries)}"
    )


@pytest.mark.parametrize("subdir, files", SUBDIRS.items())
def test_subdirectory_contents(subdir: str, files):
    """
    Each sub-directory must contain exactly two text files with the expected
    names and contents—nothing more, nothing less.
    """
    path = BASE_DIR / subdir
    assert path.exists(), f"Expected directory {path} to exist."
    assert path.is_dir(), f"Expected {path} to be a directory."

    dir_files = {p.name for p in path.iterdir() if p.is_file()}
    expected_filenames = {fname for fname, _ in files}

    # File names -------------------------------------------------------------
    assert dir_files == expected_filenames, (
        f"In {path} expected files {sorted(expected_filenames)}, "
        f"found {sorted(dir_files)}."
    )

    # File contents ----------------------------------------------------------
    for fname, expected_contents in files:
        file_path = path / fname
        actual_contents = _read_text(file_path)
        assert actual_contents == expected_contents, (
            f"File {file_path} has unexpected contents.\n"
            f"Expected: {repr(expected_contents)}\n"
            f"Actual:   {repr(actual_contents)}"
        )

    # Extra directories? -----------------------------------------------------
    extra_dirs = [p.name for p in path.iterdir() if p.is_dir()]
    assert not extra_dirs, (
        f"Did not expect any sub-directories inside {path}, "
        f"but found: {sorted(extra_dirs)}"
    )


def test_archives_directory_absent():
    """The student has not yet created /archives, so it must be absent."""
    assert not ARCHIVES_DIR.exists(), (
        f"Directory {ARCHIVES_DIR} should NOT exist before the task starts."
    )


def test_log_file_absent():
    """The activity log must *not* exist before the student begins."""
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} should NOT exist before the task starts."
    )