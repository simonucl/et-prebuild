# test_initial_state.py
#
# This test-suite validates that the *starting* filesystem state is exactly
# what the exercise description promises.  It deliberately does **not** check
# for any artefacts that the student is supposed to create later on
# (/home/user/data/final, *.tar.gz, processing_report.log, …).
#
# Failing tests will tell the student which prerequisite files / directories
# are missing or wrong **before** they begin the task.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
STAGING_DIR = DATA_DIR / "staging"
NESTED_DIR = STAGING_DIR / "nested"

# --------------------------------------------------------------------------- #
# Ground-truth: files that *must* exist at the start of the assignment
# --------------------------------------------------------------------------- #

TMP_FILES = {
    STAGING_DIR / "readme.tmp": b"temporary readme\n",
    STAGING_DIR / "notes.tmp": b"some notes\n",
    STAGING_DIR / "empty.tmp": b"",
    NESTED_DIR / "old.tmp": b"old tmp\n",
    NESTED_DIR / "blank.tmp": b"",
}

TXT_FILES = {
    STAGING_DIR / "sample1.txt": b"sample1-data\n",
    STAGING_DIR / "sample2.txt": b"sample2-data\n",
    NESTED_DIR / "data.txt": b"nested-sample\n",
}

LOG_FILE = STAGING_DIR / "ignore.log"
LOG_CONTENT = b"keep me\n"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #


def walk_files(root: Path, suffix: str):
    """Return a set of Path objects for *all* files under <root> with given suffix."""
    return {
        p for p in root.rglob("*") if p.is_file() and p.name.endswith(suffix)
    }


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("file_path,expected_content", list(TMP_FILES.items()))
def test_tmp_files_present_with_correct_content(file_path: Path, expected_content: bytes):
    """Every *.tmp file must be present with the exact expected content."""
    assert file_path.exists(), f"Required .tmp file missing: {file_path}"
    assert file_path.is_file(), f"Expected a regular file but got something else: {file_path}"
    actual = file_path.read_bytes()
    assert (
        actual == expected_content
    ), f"Content mismatch in {file_path!s}. Expected {expected_content!r}, got {actual!r}"


def test_exactly_five_tmp_files_under_staging():
    """There should be exactly five *.tmp files in the entire staging tree."""
    found = walk_files(STAGING_DIR, ".tmp")
    assert len(found) == 5, (
        "The starting situation must contain exactly 5 '.tmp' files under "
        f"{STAGING_DIR}. Found {len(found)}: {sorted(map(str, found))}"
    )


@pytest.mark.parametrize("file_path,expected_content", list(TXT_FILES.items()))
def test_txt_files_present_with_correct_content(file_path: Path, expected_content: bytes):
    """Every *.txt file must be present with the exact expected content."""
    assert file_path.exists(), f"Required .txt file missing: {file_path}"
    assert file_path.is_file(), f"Expected a regular file but got something else: {file_path}"
    actual = file_path.read_bytes()
    assert (
        actual == expected_content
    ), f"Content mismatch in {file_path!s}. Expected {expected_content!r}, got {actual!r}"


def test_exactly_three_txt_files_under_staging():
    """There should be exactly three *.txt files in the entire staging tree."""
    found = walk_files(STAGING_DIR, ".txt")
    assert len(found) == 3, (
        "The starting situation must contain exactly 3 '.txt' files under "
        f"{STAGING_DIR}. Found {len(found)}: {sorted(map(str, found))}"
    )


def test_ignore_log_file_present_and_unchanged():
    """ignore.log must exist with the original content."""
    assert LOG_FILE.exists(), f"Log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} should be a regular file."
    actual = LOG_FILE.read_bytes()
    assert (
        actual == LOG_CONTENT
    ), f"Content mismatch in {LOG_FILE}. Expected {LOG_CONTENT!r}, got {actual!r}"


def test_no_tmp_or_txt_files_outside_expected_locations():
    """
    Sanity-check: ensure we did not miss any '*.tmp' or '*.txt' files that are
    *not* in the ground-truth lists.
    """
    expected_tmp = set(TMP_FILES.keys())
    expected_txt = set(TXT_FILES.keys())

    found_tmp = walk_files(STAGING_DIR, ".tmp")
    found_txt = walk_files(STAGING_DIR, ".txt")

    unexpected_tmp = found_tmp - expected_tmp
    unexpected_txt = found_txt - expected_txt

    assert (
        not unexpected_tmp
    ), f"Unexpected '.tmp' files found: {sorted(map(str, unexpected_tmp))}"
    assert (
        not unexpected_txt
    ), f"Unexpected '.txt' files found: {sorted(map(str, unexpected_txt))}"