# test_initial_state.py
#
# Pytest test-suite that verifies the *initial* filesystem state for the
# “artifact-manager” exercise **before** the student performs any action.
#
# It intentionally does *NOT* test for the presence of any output objects
# that the student is supposed to create later on (everything under
# /home/user/artifact_audit).  It focuses solely on what must already be
# on disk when the exercise starts.
#
# Only the Python standard-library and pytest are used.

import hashlib
import os
import time
from pathlib import Path

import pytest

HOME = Path("/home/user")
REPOS = HOME / "repositories"

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def file_size(path: Path) -> int:
    """Return file size in bytes."""
    return path.stat().st_size


def mtime(path: Path) -> float:
    """Return modification time in seconds since epoch."""
    return path.stat().st_mtime


def age_in_days(path: Path) -> float:
    """Return file age in days (positive -> older than now)."""
    return (time.time() - mtime(path)) / 86400.0


def sha256_hex(path: Path) -> str:
    """Return SHA-256 hex digest of a file (minus filename, same as `sha256sum`)."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
# Expected initial structure
# --------------------------------------------------------------------------- #
EXPECTED_DIRS = [
    REPOS,
    REPOS / "repoA",
    REPOS / "repoA" / "nested",
    REPOS / "repoB",
]

# path -> expected size (bytes)
EXPECTED_FILES = {
    REPOS / "repoA" / "oldlib-1.0.jar": 31,
    REPOS / "repoA" / "newlib-2.0.jar": 31,
    REPOS / "repoA" / "package-1.0.tar.gz": 38,
    REPOS / "repoA" / "empty.tmp": 0,
    REPOS / "repoA" / "nested" / "legacy-0.9.jar": 18,
    REPOS / "repoA" / "nested" / "sample-archive.tar.gz": 36,
    REPOS / "repoA" / "nested" / "zero.txt": 0,
    REPOS / "repoB" / "obsolete-2.3.jar": 28,
    REPOS / "repoB" / "data-1.1.tar.gz": 27,
    REPOS / "repoB" / "nothing.txt": 0,
}

AGED_JARS = {
    REPOS / "repoA" / "oldlib-1.0.jar",
    REPOS / "repoA" / "nested" / "legacy-0.9.jar",
    REPOS / "repoB" / "obsolete-2.3.jar",
}

FRESH_TARBALLS = {
    REPOS / "repoA" / "package-1.0.tar.gz",
    REPOS / "repoA" / "nested" / "sample-archive.tar.gz",
    REPOS / "repoB" / "data-1.1.tar.gz",
}

ZERO_BYTE_FILES = {
    REPOS / "repoA" / "empty.tmp",
    REPOS / "repoA" / "nested" / "zero.txt",
    REPOS / "repoB" / "nothing.txt",
}

# Age thresholds
DAYS_30 = 30
DAYS_90 = 90

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_directories_exist():
    """All required repository directories must exist."""
    missing = [str(p) for p in EXPECTED_DIRS if not p.is_dir()]
    assert not missing, f"Missing directories: {missing!r}"


def test_files_exist_and_sizes():
    """All expected files must exist with the correct sizes."""
    missing = [str(p) for p in EXPECTED_FILES if not p.is_file()]
    assert not missing, f"Missing files: {missing!r}"

    wrong_size = [
        f"{p} (expected {EXPECTED_FILES[p]} → found {file_size(p)})"
        for p in EXPECTED_FILES
        if p.is_file() and file_size(p) != EXPECTED_FILES[p]
    ]
    assert not wrong_size, (
        "Files with unexpected sizes:\n  " + "\n  ".join(wrong_size)
    )


def test_zero_byte_files_are_zero_bytes():
    """Ensure the zero-byte files really have size 0."""
    non_zero = [
        f"{p} (size {file_size(p)})" for p in ZERO_BYTE_FILES if file_size(p) != 0
    ]
    assert not non_zero, (
        "These files are expected to be *exactly* 0-bytes but are not:\n  "
        + "\n  ".join(non_zero)
    )


def test_aged_jars_are_older_than_90_days():
    """The ‘aged’ *.jar files must be older than 90 days."""
    too_new = [
        f"{p} (age {age_in_days(p):.2f} days)"
        for p in AGED_JARS
        if age_in_days(p) <= DAYS_90
    ]
    assert not too_new, (
        "The following *.jar files are expected to be older than "
        f"{DAYS_90} days but are not:\n  " + "\n  ".join(too_new)
    )


def test_fresh_tarballs_are_newer_than_30_days():
    """The ‘fresh’ *.tar.gz files must be newer than 30 days."""
    too_old = [
        f"{p} (age {age_in_days(p):.2f} days)"
        for p in FRESH_TARBALLS
        if age_in_days(p) >= DAYS_30
    ]
    assert not too_old, (
        "The following *.tar.gz files are expected to be *newer* than "
        f"{DAYS_30} days but appear older:\n  " + "\n  ".join(too_old)
    )


def test_no_artifact_audit_directory_yet():
    """The output directory should not exist *before* the student's actions."""
    audit_dir = HOME / "artifact_audit"
    assert not audit_dir.exists(), (
        f"{audit_dir} should NOT exist before the student runs their solution."
    )