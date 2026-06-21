# test_initial_state.py
"""
Pytest suite that validates the **initial** operating-system / filesystem state
*before* the student attempts the task described in the assignment.

What is verified:
1. The artefact /home/user/builds/webapp_2023-09-15.tar.gz
   • exists,
   • is a regular file,
   • contains exactly the 5 bytes corresponding to ASCII “hello”,
   • has the expected SHA-256 digest.

2. No checksum side-car file is present yet; i.e.
   /home/user/checksums/webapp_2023-09-15.sha256 must **not** exist.

These assertions guarantee that the environment starts in the known good state
expected by the downstream grading logic.
"""
import hashlib
import os
from pathlib import Path

import pytest

# --- Constants used throughout the tests ------------------------------------

ARTEFACT_PATH = Path("/home/user/builds/webapp_2023-09-15.tar.gz")
CHECKSUM_DIR = Path("/home/user/checksums")
SIDECAR_PATH = CHECKSUM_DIR / "webapp_2023-09-15.sha256"

EXPECTED_ARTEFACT_BYTES = b"hello"  # exactly 5 bytes, no trailing newline
EXPECTED_SHA256 = (
    "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
)


# --- Helper ------------------------------------------------------------------


def sha256_of_file(path: Path) -> str:
    """Return the hex-encoded SHA-256 digest (lower-case) of *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --- Tests -------------------------------------------------------------------


def test_artefact_exists_and_is_regular_file():
    """The artefact must exist and be a regular file."""
    assert ARTEFACT_PATH.exists(), (
        f"Expected artefact {ARTEFACT_PATH} does not exist. "
        "The build step should have downloaded it."
    )
    assert ARTEFACT_PATH.is_file(), (
        f"{ARTEFACT_PATH} exists but is not a regular file."
    )


def test_artefact_contents_are_correct():
    """The artefact should contain exactly the bytes for ASCII 'hello'."""
    data = ARTEFACT_PATH.read_bytes()
    assert data == EXPECTED_ARTEFACT_BYTES, (
        f"Artefact contents differ from the expected 5 bytes 'hello'.\n"
        f"Expected: {EXPECTED_ARTEFACT_BYTES!r}\nObserved: {data!r}"
    )
    assert len(data) == 5, (
        f"Artefact size is {len(data)} bytes; expected exactly 5 bytes."
    )


def test_artefact_checksum_matches_expected():
    """The SHA-256 digest of the artefact must match the known value."""
    digest = sha256_of_file(ARTEFACT_PATH)
    assert digest == EXPECTED_SHA256, (
        "SHA-256 digest of the artefact is incorrect.\n"
        f"Expected: {EXPECTED_SHA256}\nObserved: {digest}"
    )


def test_sidecar_file_absent_initially():
    """
    The checksum side-car file must not exist yet; its creation is part of the task.

    The directory /home/user/checksums may or may not exist at this point, but
    the specific side-car file must be absent to ensure the student actually
    produces it.
    """
    assert not SIDECAR_PATH.exists(), (
        f"Side-car file {SIDECAR_PATH} already exists, but it should not be "
        "present before the task is completed."
    )