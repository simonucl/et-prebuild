# test_initial_state.py
#
# This PyTest suite validates the **initial** operating-system / filesystem
# state *before* the student performs any action.  It confirms that the
# existing configuration directory and the three configuration files are
# present, have the correct permissions, sizes, contents and SHA-256 digests.
#
# NOTE:  We intentionally **do not** test for the presence (or absence) of the
#        two *output* files the student is expected to create later
#        (manifest.sha256 and verification.log), in accordance with the
#        evaluation rules.

import hashlib
import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

CONFIG_DIR = Path("/home/user/configs")

EXPECTED_DIR_MODE = 0o755  # as per task description

# Expected file data: name -> (expected_bytes, expected_sha256)
EXPECTED_FILES = {
    "app.conf": (
        b"abc",
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    ),
    "db.conf": (
        b"",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    "web.conf": (
        b"The quick brown fox jumps over the lazy dog",
        "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
    ),
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def sha256_hex(data: bytes) -> str:
    """Return the SHA-256 hex digest of *data*."""
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_configs_directory_exists_and_has_correct_permissions():
    """
    The directory /home/user/configs must exist, be a directory,
    and have exactly 0o755 permissions.
    """
    assert CONFIG_DIR.exists(), f"Expected directory {CONFIG_DIR} to exist."
    assert CONFIG_DIR.is_dir(), f"{CONFIG_DIR} exists but is not a directory."

    # Mask with 0o777 to ignore file-type bits.
    actual_mode = CONFIG_DIR.stat().st_mode & 0o777
    assert (
        actual_mode == EXPECTED_DIR_MODE
    ), f"Directory {CONFIG_DIR} must have mode 755, found {oct(actual_mode)}."


@pytest.mark.parametrize("filename", sorted(EXPECTED_FILES.keys()))
def test_each_configuration_file(filename):
    """
    For every expected configuration file:
      • it must exist,
      • its size must match,
      • its content must be byte-for-byte correct (no stray newlines, etc.),
      • its SHA-256 digest must match the agreed reference value.
    """
    expected_bytes, expected_digest = EXPECTED_FILES[filename]
    file_path = CONFIG_DIR / filename

    # 1. Presence
    assert file_path.exists(), f"Expected file {file_path} to exist."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    # 2. Size check
    actual_size = file_path.stat().st_size
    expected_size = len(expected_bytes)
    assert (
        actual_size == expected_size
    ), f"Size mismatch for {file_path}: expected {expected_size} bytes, found {actual_size}."

    # 3. Content check
    actual_bytes = file_path.read_bytes()
    assert (
        actual_bytes == expected_bytes
    ), f"Content of {file_path} differs from expected bytes."

    # 4. SHA-256 digest check
    actual_digest = sha256_hex(actual_bytes)
    assert (
        actual_digest == expected_digest
    ), (
        f"SHA-256 digest mismatch for {file_path}.\n"
        f"  expected: {expected_digest}\n"
        f"    found: {actual_digest}"
    )