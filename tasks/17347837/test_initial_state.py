# test_initial_state.py
"""
Pytest suite to validate the *initial* state of the filesystem **before**
the student starts working on the “artifact-manager” task.

This file only checks the pre-existing assets under
    /home/user/artifacts-source/
and deliberately ignores any target/output locations.

All assertions contain explicit, helpful error messages so that any
deviation from the expected starting conditions is immediately obvious.
"""

import os
import hashlib

SOURCE_DIR = "/home/user/artifacts-source"
ALPHA_PATH = os.path.join(SOURCE_DIR, "alpha.bin")
BETA_PATH = os.path.join(SOURCE_DIR, "beta.bin")


def test_source_directory_exists():
    assert os.path.isdir(
        SOURCE_DIR
    ), f"Required directory {SOURCE_DIR!r} is missing."


def _read_file_bytes(path: str) -> bytes:
    """Utility helper to read a file in binary mode."""
    with open(path, "rb") as fp:
        return fp.read()


def _assert_file(
    path: str,
    expected_content: bytes,
):
    """
    Generic checker for a single file:
      • must exist
      • must be a regular file
      • size and exact byte sequence must match the expectation
      • SHA-256 digest must be a valid 64-char hex string
    """
    assert os.path.isfile(path), f"Expected file {path!r} is missing or not a regular file."

    data = _read_file_bytes(path)
    assert (
        data == expected_content
    ), f"File {path!r} does not contain the expected byte sequence."

    # Size assertion
    expected_size = len(expected_content)
    actual_size = os.path.getsize(path)
    assert (
        actual_size == expected_size
    ), f"File {path!r} should be {expected_size} bytes, found {actual_size} bytes."

    # SHA-256 sanity check (length & hex characters)
    sha256_hex = hashlib.sha256(data).hexdigest()
    assert (
        len(sha256_hex) == 64 and all(c in "0123456789abcdef" for c in sha256_hex)
    ), f"Computed SHA-256 digest for {path!r} is invalid: {sha256_hex!r}"


def test_alpha_bin_present_and_correct():
    """alpha.bin must exist with exact content b'ALPHA\\n' (6 bytes)."""
    _assert_file(ALPHA_PATH, b"ALPHA\n")


def test_beta_bin_present_and_correct():
    """beta.bin must exist with exact content b'BETA\\n' (5 bytes)."""
    _assert_file(BETA_PATH, b"BETA\n")