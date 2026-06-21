# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student performs any action.  It checks that the source
# backup file exists and has the expected SHA-256 digest.  It does NOT
# inspect any of the artefacts the student is supposed to create
# (/home/user/backup_verification/*), in accordance with the spec.

import hashlib
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BACKUP_FILE = Path("/home/user/backups/daily/important_data.tar.gz")
# Known-good SHA-256 for the backup file, as provided in the task
EXPECTED_SHA256 = (
    "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def sha256_of_file(path: Path, chunk_size: int = 1 << 16) -> str:
    """
    Compute the SHA-256 hex digest of *path* without reading the entire file
    into memory.  Returns a 64-character lowercase hexadecimal string.
    """
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_backup_file_exists_and_is_regular():
    """
    The critical archive must be present *before* the student starts.
    """
    assert BACKUP_FILE.exists(), (
        f"Required backup file {BACKUP_FILE} does not exist. "
        "Restore it before proceeding."
    )
    assert BACKUP_FILE.is_file(), (
        f"{BACKUP_FILE} exists but is not a regular file."
    )
    assert BACKUP_FILE.stat().st_size > 0, (
        f"{BACKUP_FILE} is empty; expected non-zero size."
    )


def test_backup_file_sha256_is_expected():
    """
    Verify that the backup file's SHA-256 digest matches the value
    provided in the task description.
    """
    actual = sha256_of_file(BACKUP_FILE)
    assert (
        actual == EXPECTED_SHA256
    ), (
        "SHA-256 mismatch for the backup file.\n"
        f"Expected: {EXPECTED_SHA256}\n"
        f"Actual:   {actual}\n"
        "Ensure the correct file is in place before continuing."
    )