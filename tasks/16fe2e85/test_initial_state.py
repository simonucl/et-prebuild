# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state **before** the
student starts working on the integrity-check task.

It asserts that:
1. Mandatory directories exist with permissions 0755.
2. Mandatory data files exist, are **empty** (0 bytes) and have permissions 0644.
3. The checksum manifest exists, has permissions 0644, contains the exact
   expected content, and every hash listed really matches the (empty) files.

Only stdlib + pytest are used and every failure message pinpoints what is
missing or wrong.
"""

import hashlib
import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the expected initial state
# --------------------------------------------------------------------------- #

HOME = Path("/home/user")
INCOMING = HOME / "incoming_batches"
VERIFICATION_LOGS = HOME / "verification_logs"

EXPECTED_DIRECTORIES = {
    INCOMING: 0o755,
    INCOMING / "batchA": 0o755,
    INCOMING / "batchB": 0o755,
    VERIFICATION_LOGS: 0o755,
}

# Data files (all must be empty)
EXPECTED_FILES = {
    INCOMING / "batchA" / "alpha.txt": 0o644,
    INCOMING / "batchA" / "bravo.txt": 0o644,
    INCOMING / "batchB" / "charlie.txt": 0o644,
    INCOMING / "batchB" / "delta.txt": 0o644,
}

MANIFEST_PATH = INCOMING / "expected_sha256.txt"

_EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)

_MANIFEST_LINES = [
    f"{_EMPTY_SHA256}  batchA/alpha.txt",
    f"{_EMPTY_SHA256}  batchA/bravo.txt",
    f"{_EMPTY_SHA256}  batchB/charlie.txt",
    f"{_EMPTY_SHA256}  batchB/delta.txt",
]
EXPECTED_MANIFEST_CONTENT = "\n".join(_MANIFEST_LINES) + "\n"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #


def _mode_without_special_bits(st_mode: int) -> int:
    """
    Return only the permission bits (e.g. 0o644, 0o755) from st_mode.
    """
    return st_mode & 0o777


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


def test_expected_directories_exist_with_correct_permissions():
    """
    Each required directory must exist and be a directory with mode 0755.
    """
    for directory, expected_mode in EXPECTED_DIRECTORIES.items():
        assert directory.exists(), f"Directory missing: {directory}"
        assert directory.is_dir(), f"Expected directory but found file: {directory}"
        actual_mode = _mode_without_special_bits(directory.stat().st_mode)
        assert (
            actual_mode == expected_mode
        ), f"Directory {directory} expected mode {oct(expected_mode)}, found {oct(actual_mode)}"


def test_expected_files_exist_empty_and_correct_permissions():
    """
    Each required data file must exist, be 0 bytes and have mode 0644.
    """
    for file_path, expected_mode in EXPECTED_FILES.items():
        assert file_path.exists(), f"Data file missing: {file_path}"
        assert file_path.is_file(), f"Expected regular file but found directory: {file_path}"
        size = file_path.stat().st_size
        assert size == 0, f"File {file_path} should be empty (0 bytes) but is {size} bytes"
        actual_mode = _mode_without_special_bits(file_path.stat().st_mode)
        assert (
            actual_mode == expected_mode
        ), f"File {file_path} expected mode {oct(expected_mode)}, found {oct(actual_mode)}"


def test_manifest_exists_mode_and_exact_content():
    """
    Manifest must exist, have correct mode and **exact** expected content.
    """
    assert MANIFEST_PATH.exists(), f"Checksum manifest missing: {MANIFEST_PATH}"
    assert MANIFEST_PATH.is_file(), f"Manifest path is not a regular file: {MANIFEST_PATH}"

    actual_mode = _mode_without_special_bits(MANIFEST_PATH.stat().st_mode)
    expected_mode = 0o644
    assert (
        actual_mode == expected_mode
    ), f"Manifest {MANIFEST_PATH} expected mode {oct(expected_mode)}, found {oct(actual_mode)}"

    content = MANIFEST_PATH.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_MANIFEST_CONTENT
    ), (
        "Manifest content is not exactly as expected.\n"
        "---- Expected ----\n"
        f"{EXPECTED_MANIFEST_CONTENT}"
        "---- Found ----\n"
        f"{content}"
    )


@pytest.mark.parametrize(
    "relative_path",
    [
        "batchA/alpha.txt",
        "batchA/bravo.txt",
        "batchB/charlie.txt",
        "batchB/delta.txt",
    ],
)
def test_manifest_hashes_match_actual_files(relative_path):
    """
    The sha256 checksum in the manifest must match the checksum of the actual
    file on disk.
    """
    file_path = INCOMING / relative_path
    assert file_path.exists(), f"File referenced in manifest does not exist: {file_path}"

    # Calculate sha256 of the file
    digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
    assert (
        digest == _EMPTY_SHA256
    ), f"Checksum mismatch for {file_path}: expected {_EMPTY_SHA256}, got {digest}"