# test_initial_state.py
"""
Pytest suite that verifies the initial operating-system / file-system state
*before* the student starts working on the task.

It checks that the staging backup directory exists and contains exactly the three
expected regular files with the prescribed placeholder contents.  Nothing about
the expected output artefacts (/home/user/backup_reports/…) is verified here.
"""

import hashlib
import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the required initial state
# --------------------------------------------------------------------------- #
BACKUP_DIR = Path("/home/user/backups/2023-10-03")

EXPECTED_FILES = {
    "config.zip": b"CONFIG ZIP PLACEHOLDER\n",
    "db_dump.sql.gz": b"SAMPLE DATABASE BACKUP 2023-10-03\n",
    "photos.tar": b"PHOTOS ARCHIVE PLACEHOLDER\n",
}

# Pre-compute expected sizes and SHA-256 sums
EXPECTED_META = {
    name: {
        "size": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }
    for name, content in EXPECTED_FILES.items()
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def sha256sum(path: Path) -> str:
    """Return the hex-digest SHA-256 of the file at *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_backup_directory_exists_and_is_dir():
    assert BACKUP_DIR.exists(), (
        f"Required directory {BACKUP_DIR} is missing. "
        "The pre-populated backup data must be present before starting the task."
    )
    assert BACKUP_DIR.is_dir(), f"{BACKUP_DIR} exists but is not a directory."


def test_backup_directory_contains_only_expected_files():
    present_files = sorted(p.name for p in BACKUP_DIR.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_FILES.keys())
    assert present_files == expected_files, (
        "The backup directory must contain exactly these files:\n"
        f"  {expected_files}\n"
        f"Currently found:\n"
        f"  {present_files}"
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_file_content_size_and_checksum(filename, expected_content):
    file_path = BACKUP_DIR / filename
    assert file_path.is_file(), f"Expected file {file_path} is missing or not a regular file."

    # Size check
    actual_size = file_path.stat().st_size
    expected_size = EXPECTED_META[filename]["size"]
    assert (
        actual_size == expected_size
    ), f"{filename}: expected size {expected_size} bytes, found {actual_size} bytes."

    # SHA-256 check
    actual_sha = sha256sum(file_path)
    expected_sha = EXPECTED_META[filename]["sha256"]
    assert (
        actual_sha == expected_sha
    ), f"{filename}: expected SHA-256 {expected_sha}, found {actual_sha}."

    # (Optional) sanity check that placeholder content matches exactly
    with file_path.open("rb") as fh:
        actual_content = fh.read()
    assert (
        actual_content == expected_content
    ), f"{filename}: file content does not match the required placeholder string."