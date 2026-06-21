# test_initial_state.py
"""
Pytest suite to validate the initial, pre-task filesystem state.

The student task will later:
    • Compute the SHA-256 of /home/user/experiments/run_42/model.bin
    • Append it to   /home/user/experiments/checksums.log

Per grading rules, this pre-task test must **not** look at, create, or
assert anything about the eventual output file (/home/user/experiments/checksums.log).
It must only confirm that the prerequisite inputs exist and are intact.
"""

import hashlib
import os
from pathlib import Path

import pytest

# ----- Constants -------------------------------------------------------------

MODEL_PATH = Path("/home/user/experiments/run_42/model.bin")
EXPECTED_BYTES = b"hello"  # 5 bytes, no trailing newline
EXPECTED_SHA256 = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


# ----- Helper ----------------------------------------------------------------


def sha256_of(path: Path) -> str:
    """
    Compute the hexadecimal SHA-256 digest of a file.

    Parameters
    ----------
    path : pathlib.Path
        Full path to the file.

    Returns
    -------
    str
        64-character, lower-case hexadecimal digest.
    """
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ----- Tests -----------------------------------------------------------------


def test_model_file_exists_and_is_regular():
    """The artifact file must exist and be a regular file."""
    assert MODEL_PATH.exists(), (
        f"Required file not found: {MODEL_PATH}. "
        "The task cannot proceed without this input model artifact."
    )
    assert MODEL_PATH.is_file(), f"{MODEL_PATH} exists but is not a regular file."


def test_model_file_contents_are_exact():
    """The model.bin file must contain exactly the expected 5 bytes: b'hello'."""
    actual_bytes = MODEL_PATH.read_bytes()
    assert actual_bytes == EXPECTED_BYTES, (
        f"{MODEL_PATH} has unexpected contents.\n"
        f"Expected (hex): {EXPECTED_BYTES.hex()}\n"
        f"Actual   (hex): {actual_bytes.hex()}"
    )


def test_model_file_sha256_matches_expected():
    """Verify the SHA-256 digest equals the pre-computed truth value."""
    actual_digest = sha256_of(MODEL_PATH)
    assert actual_digest == EXPECTED_SHA256, (
        f"SHA-256 mismatch for {MODEL_PATH}.\n"
        f"Expected: {EXPECTED_SHA256}\n"
        f"Actual  : {actual_digest}"
    )