# test_initial_state.py
"""
Pytest suite to verify the initial operating-system / filesystem state
before the student performs any action.

This file checks ONLY the pre-existing resources and does **not** touch or
test for the eventual output artefacts (e.g., /home/user/utils/checksums.log).
"""

import hashlib
import os
import stat
from pathlib import Path

# Absolute paths that will be used throughout the tests
UTILS_DIR = Path("/home/user/utils")
INPUT_FILE = UTILS_DIR / "input.txt"

EXPECTED_DIGEST = (
    "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
)
EXPECTED_CONTENT = b"hello"  # 5 bytes, no trailing newline


def test_utils_directory_exists_and_writable():
    """
    Ensure /home/user/utils:
    1. Exists.
    2. Is a directory.
    3. Is writable by the current user.
    """
    assert UTILS_DIR.exists(), (
        f"Required directory {UTILS_DIR} does not exist."
    )
    assert UTILS_DIR.is_dir(), (
        f"{UTILS_DIR} exists but is not a directory."
    )

    # Check write permission; we avoid side-effects by using os.access
    is_writable = os.access(UTILS_DIR, os.W_OK)
    assert is_writable, (
        f"Directory {UTILS_DIR} is not writable by the current user."
    )


def test_input_txt_exists_and_is_file():
    """
    Ensure /home/user/utils/input.txt exists and is a regular file.
    """
    assert INPUT_FILE.exists(), (
        f"Required file {INPUT_FILE} does not exist."
    )
    assert INPUT_FILE.is_file(), (
        f"{INPUT_FILE} exists but is not a regular file."
    )


def test_input_txt_content_exact():
    """
    Validate that input.txt contains exactly the 5 bytes 'hello'
    with NO trailing newline or additional characters.
    """
    data = INPUT_FILE.read_bytes()

    assert data == EXPECTED_CONTENT, (
        "input.txt content mismatch.\n"
        "Expected exact bytes: b'hello' (5 bytes, no newline)\n"
        f"Found            : {data!r}"
    )

    assert len(data) == 5, (
        f"input.txt should be exactly 5 bytes; found {len(data)} bytes."
    )


def test_input_txt_sha256_digest_matches():
    """
    Confirm that the SHA-256 digest of input.txt matches the expected value.
    """
    digest = hashlib.sha256(EXPECTED_CONTENT).hexdigest()
    assert digest == EXPECTED_DIGEST, (
        "SHA-256 digest mismatch for the expected content 'hello'.\n"
        f"Expected digest: {EXPECTED_DIGEST}\n"
        f"Computed digest: {digest}"
    )

    # As an additional safety check, compute directly from the file
    actual_digest_from_file = hashlib.sha256(INPUT_FILE.read_bytes()).hexdigest()
    assert actual_digest_from_file == EXPECTED_DIGEST, (
        "SHA-256 digest mismatch when reading directly from input.txt.\n"
        f"Expected digest: {EXPECTED_DIGEST}\n"
        f"File digest    : {actual_digest_from_file}"
    )


def test_input_txt_file_permissions_are_sensible():
    """
    Ensure input.txt is readable (0600-0644 typical range).  We do not
    require exact permissions, but it must be readable by the owner.
    """
    mode = INPUT_FILE.stat().st_mode
    is_readable = bool(mode & stat.S_IRUSR)
    assert is_readable, (
        f"{INPUT_FILE} is not readable by the file owner."
    )