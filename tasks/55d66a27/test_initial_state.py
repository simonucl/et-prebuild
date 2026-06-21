# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the student performs any actions for the “record SHA-256 checksum”
# task.
#
# What we assert:
#   1. /home/user/tracked/empty.conf exists, is a regular file, is zero bytes
#      long, and its SHA-256 digest matches the well-known value for an
#      empty file.
#   2. /home/user/config_checksums.log must NOT exist yet; the student is
#      supposed to create (or overwrite) it.
#
# Only Python’s standard library and pytest are used.

import hashlib
import os
from pathlib import Path

import pytest

# --- Constants -------------------------------------------------------------

EMPTY_CONF_PATH = Path("/home/user/tracked/empty.conf")
EXPECTED_DIGEST = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)
CHECKSUM_LOG_PATH = Path("/home/user/config_checksums.log")


# --- Helper ----------------------------------------------------------------


def sha256_hex(path: Path) -> str:
    """Return the SHA-256 hex digest of the file at *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --- Tests -----------------------------------------------------------------


def test_empty_conf_exists_and_is_zero_byte_with_correct_digest():
    """Validate that the tracked/empty.conf file is present and pristine."""
    assert EMPTY_CONF_PATH.exists(), (
        f"Required file {EMPTY_CONF_PATH} is missing. "
        "It must be present before the task begins."
    )
    assert EMPTY_CONF_PATH.is_file(), (
        f"{EMPTY_CONF_PATH} exists but is not a regular file."
    )

    size = EMPTY_CONF_PATH.stat().st_size
    assert size == 0, (
        f"{EMPTY_CONF_PATH} should be 0 bytes, but is {size} bytes long."
    )

    digest = sha256_hex(EMPTY_CONF_PATH)
    assert (
        digest == EXPECTED_DIGEST
    ), f"{EMPTY_CONF_PATH} digest mismatch: expected {EXPECTED_DIGEST}, got {digest}"


def test_config_checksums_log_absent_initially():
    """
    The log file must not pre-exist. The student’s task is to create or
    overwrite it with exactly one line.
    """
    assert not CHECKSUM_LOG_PATH.exists(), (
        f"{CHECKSUM_LOG_PATH} already exists. "
        "The workspace should start without this file so the student can "
        "create it."
    )