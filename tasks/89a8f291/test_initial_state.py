# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system / filesystem
# state for the “legacy config encoding” exercise.  It asserts that the legacy
# Windows-1252 file and its parent directory are present and correct, and that
# the artefacts the student must create **do not yet exist**.
#
# The checks are intentionally explicit so that any failure message clearly
# explains what is missing or incorrect.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Immutable, canonical paths used by all tests
# --------------------------------------------------------------------------- #
CICD_DIR = Path("/home/user/projects/cicd")
LEGACY_FILE = CICD_DIR / "legacy_config_win1252.txt"
UTF8_FILE = CICD_DIR / "legacy_config_utf8.txt"
LOG_FILE = CICD_DIR / "encoding_conversion.log"

# --------------------------------------------------------------------------- #
# Expected legacy file content
# --------------------------------------------------------------------------- #
EXPECTED_TEXT = (
    "# Build configuration – ACME CI/CD\n"
    "BUILD_SERVER=alpha\n"
    "DEPLOY_TARGET=production\n"
    "CURRENCY=€\n"
)
EXPECTED_BYTES = EXPECTED_TEXT.encode("windows-1252")  # Windows-1252 byte sequence


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_cicd_directory_exists():
    """The /home/user/projects/cicd directory must exist and be a directory."""
    assert CICD_DIR.exists(), f"Required directory missing: {CICD_DIR}"
    assert CICD_DIR.is_dir(), f"Expected {CICD_DIR} to be a directory"


def test_legacy_file_exists():
    """The legacy Windows-1252 file must exist before any conversion happens."""
    assert LEGACY_FILE.exists(), f"Required file missing: {LEGACY_FILE}"
    assert LEGACY_FILE.is_file(), f"Expected {LEGACY_FILE} to be a regular file"


def test_legacy_file_bytes_and_encoding():
    """
    The legacy file must:
      • contain the exact expected Windows-1252 byte sequence
      • decode to the expected Unicode text
    """
    data = LEGACY_FILE.read_bytes()

    # Verify byte-for-byte equality
    assert (
        data == EXPECTED_BYTES
    ), (
        "The legacy file's byte sequence does not match the expected Windows-1252 "
        "content.  Ensure the file has not been modified."
    )

    # Verify that decoding using Windows-1252 round-trips to the expected text
    decoded = data.decode("windows-1252")
    assert (
        decoded == EXPECTED_TEXT
    ), "Decoding the legacy file with Windows-1252 did not yield the expected text"


def test_target_files_do_not_exist_yet():
    """
    Before the student begins, neither the UTF-8 copy nor the conversion
    log should be present.  They will be created as part of the task.
    """
    assert not UTF8_FILE.exists(), (
        f"{UTF8_FILE} already exists, but it should only be created by the student. "
        "Delete it before starting the exercise."
    )
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists, but it should only be created by the student. "
        "Delete it before starting the exercise."
    )