# test_initial_state.py
#
# Pytest suite that validates the initial, pre-remediation state of the
# on-disk evidence set located under /home/user/data/.  These tests must all
# pass *before* the student performs any actions.  If any test fails, the
# failure message pinpoints exactly what is missing or incorrect.
#
# NOTE:  Per instructions, this file intentionally does *not* test for the
#        presence or contents of any output / compliance artefacts.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Static paths used throughout the suite
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
ORIGINAL_DIR = DATA_DIR / "original"
ARCHIVE_DIR = DATA_DIR / "archive"
LINKS_DIR = DATA_DIR / "links"

# Files
DOC1_TXT = ORIGINAL_DIR / "doc1.txt"
DOC2_TXT = ORIGINAL_DIR / "doc2.txt"
DOC1_BAK = ARCHIVE_DIR / "doc1_backup.txt"
DOC2_BAK = ARCHIVE_DIR / "doc2_backup.txt"

# Symlinks
DOC1_LINK = LINKS_DIR / "doc1_link"
DOC2_LINK = LINKS_DIR / "doc2_link"
ARCHIVE_LINK = LINKS_DIR / "archive_link"
OLD_LINK = LINKS_DIR / "old_link"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def assert_is_file_with_content(path: Path, expected: str):
    """
    Assert that *path* exists, is a regular file, and its entire contents
    match *expected* exactly (byte-for-byte, including newlines).
    """
    assert path.exists(), f"Missing expected file: {path}"
    assert path.is_file(), f"Expected regular file at {path}, but found something else."
    data = path.read_text(encoding="utf-8")
    assert data == expected, (
        f"Unexpected contents in {path!s}.\n"
        f"Expected ({len(expected)} bytes): {repr(expected)}\n"
        f"Found    ({len(data)} bytes): {repr(data)}"
    )


def assert_symlink_points_to(path: Path, expected_target: str, target_must_exist: bool):
    """
    Assert that *path* is a symlink that points to *expected_target* (exact
    string match as stored in the symlink).  Additionally, verify whether the
    target should (or should not) exist on disk via *target_must_exist*.
    """
    assert path.exists() or path.is_symlink(), f"Expected symlink at {path} is missing."
    assert path.is_symlink(), f"{path} exists but is not a symbolic link."

    actual_target = os.readlink(path)
    assert actual_target == expected_target, (
        f"{path} points to '{actual_target}', expected '{expected_target}'."
    )

    # Absolute path to the resolved target for existence checks
    resolved = (path.parent / actual_target).resolve()
    if target_must_exist:
        assert resolved.exists(), (
            f"Symlink {path} is expected to be valid but its target {resolved} "
            "does not exist."
        )
    else:
        assert not resolved.exists(), (
            f"Symlink {path} is expected to be broken, but its target "
            f"{resolved} unexpectedly exists."
        )


# ---------------------------------------------------------------------------
# Directory structure tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "directory",
    [
        DATA_DIR,
        ORIGINAL_DIR,
        ARCHIVE_DIR,
        LINKS_DIR,
    ],
)
def test_required_directories_exist(directory: Path):
    assert directory.exists(), f"Required directory {directory} is missing."
    assert directory.is_dir(), f"{directory} exists but is not a directory."


# ---------------------------------------------------------------------------
# File presence & content tests
# ---------------------------------------------------------------------------

def test_original_documents():
    assert_is_file_with_content(DOC1_TXT, "Compliance Document 1\n")
    assert_is_file_with_content(DOC2_TXT, "Compliance Document 2\n")


def test_archive_documents():
    assert_is_file_with_content(DOC1_BAK, "Backup 1\n")
    assert_is_file_with_content(DOC2_BAK, "Backup 2\n")


# ---------------------------------------------------------------------------
# Symlink tests
# ---------------------------------------------------------------------------

def test_doc1_link_valid():
    assert_symlink_points_to(DOC1_LINK, "../original/doc1.txt", target_must_exist=True)


def test_doc2_link_broken():
    assert_symlink_points_to(DOC2_LINK, "../original/nonexistent.txt", target_must_exist=False)


def test_archive_link_valid():
    # Target must be a directory and exist
    assert_symlink_points_to(ARCHIVE_LINK, "../archive", target_must_exist=True)
    resolved = (ARCHIVE_LINK.parent / os.readlink(ARCHIVE_LINK)).resolve()
    assert resolved.is_dir(), (
        f"Target of {ARCHIVE_LINK} ({resolved}) is expected to be a directory."
    )


def test_old_link_broken():
    assert_symlink_points_to(OLD_LINK, "../old", target_must_exist=False)


def test_no_extra_symlinks_under_links_dir():
    """
    Sanity check: exactly the four expected symlinks should be present under
    /home/user/data/links/ at this stage.
    """
    expected = {DOC1_LINK, DOC2_LINK, ARCHIVE_LINK, OLD_LINK}
    actual = {p for p in LINKS_DIR.iterdir() if p.is_symlink()}
    assert actual == expected, (
        "Mismatch in the set of symlinks under /home/user/data/links/.\n"
        f"Expected: {[str(p) for p in sorted(expected)]}\n"
        f"Found   : {[str(p) for p in sorted(actual)]}"
    )