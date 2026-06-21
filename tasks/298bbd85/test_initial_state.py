# test_initial_state.py
#
# This pytest file validates the *initial* operating-system state
# BEFORE the student runs any commands.
#
# What we expect to be present already:
#   • /home/user/watched/critical_report.txt   (regular file)
#     └─ Its SHA-256 digest must be
#        2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
#
# What we deliberately do *NOT* check for:
#   • /home/user/alerts/ or integrity.log (these are output artefacts)
#
# Only stdlib + pytest are used.

import hashlib
import os
from pathlib import Path

import pytest

WATCHED_PATH = Path("/home/user/watched/critical_report.txt")
EXPECTED_SHA256 = (
    "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824".lower()
)


def compute_sha256(path: Path) -> str:
    """Return the hex SHA-256 digest of the file at *path*."""
    sha256 = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8192), b""):
            sha256.update(block)
    return sha256.hexdigest().lower()


@pytest.fixture(scope="module")
def watched_file_digest():
    """Read the watched file once and provide its digest to both tests."""
    if not WATCHED_PATH.exists():
        pytest.skip(f"{WATCHED_PATH} is absent; cannot compute digest.")
    return compute_sha256(WATCHED_PATH)


def test_watched_file_exists_and_is_regular():
    """Ensure the critical file exists and is a regular file."""
    assert WATCHED_PATH.exists(), (
        f"Required pre-existing file {WATCHED_PATH} is missing. "
        "The task cannot proceed without it."
    )
    assert WATCHED_PATH.is_file(), (
        f"{WATCHED_PATH} exists but is not a regular file "
        "(e.g., it might be a directory or symlink)."
    )


def test_watched_file_checksum(watched_file_digest):
    """Validate the SHA-256 checksum of the critical file."""
    assert (
        watched_file_digest == EXPECTED_SHA256
    ), (
        "The contents of the pre-existing file do not match the expected "
        f"SHA-256 digest.\nExpected: {EXPECTED_SHA256}\nFound:    {watched_file_digest}"
    )