# test_initial_state.py
#
# This test-suite validates that the operating-system is in the **initial**
# state expected by the task description *before* the student performs any
# actions.  It checks:
#
# 1. The qa_resources directory exists with the correct permissions.
# 2. The patch_release_v1.0.0.zip file exists, is zero bytes, and its
#    SHA-256 digest matches the required reference value.
# 3. The checksum_verification.log file is **not** present yet.
#
# If any of these conditions are not met, the tests will fail with an
# informative message so that the student immediately knows what is wrong.
#
# NOTE: Only the Python standard library and pytest are used.

import hashlib
import os
import stat
from pathlib import Path

import pytest

# Constants
HOME = Path("/home/user")
QA_DIR = HOME / "qa_resources"
PATCH_FILE = QA_DIR / "patch_release_v1.0.0.zip"
LOG_FILE = QA_DIR / "checksum_verification.log"
EXPECTED_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)


def sha256_of_file(path: Path) -> str:
    """Return the SHA-256 hex digest of a file in a memory-efficient manner."""
    sha256 = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def test_qa_resources_directory_exists_and_is_accessible():
    assert QA_DIR.exists(), (
        f"Required directory '{QA_DIR}' is missing. "
        "Create it before running the task."
    )
    assert QA_DIR.is_dir(), f"'{QA_DIR}' exists but is not a directory."
    # Check that owner has rwx (octal 0700) in the expected 0755 mode (drwxr-xr-x)
    mode = QA_DIR.stat().st_mode
    # stat.S_IMODE extracts permission bits only
    perms_octal = stat.S_IMODE(mode)
    expected_perms = 0o755
    assert perms_octal == expected_perms, (
        f"Directory '{QA_DIR}' has permissions {oct(perms_octal)}, "
        f"expected {oct(expected_perms)} (drwxr-xr-x)."
    )


def test_patch_file_exists_and_is_zero_bytes():
    assert PATCH_FILE.exists(), (
        f"Required patch file '{PATCH_FILE}' is missing. "
        "Place the zero-byte patch file in the directory before proceeding."
    )
    assert PATCH_FILE.is_file(), f"'{PATCH_FILE}' exists but is not a regular file."
    size = PATCH_FILE.stat().st_size
    assert size == 0, (
        f"Patch file '{PATCH_FILE}' is expected to be 0 bytes, "
        f"but its size is {size} bytes."
    )


def test_patch_file_sha256_is_correct():
    digest = sha256_of_file(PATCH_FILE)
    assert (
        digest == EXPECTED_SHA256
    ), f"SHA-256 of '{PATCH_FILE}' is {digest}, expected {EXPECTED_SHA256}."


def test_log_file_does_not_exist_yet():
    assert not LOG_FILE.exists(), (
        f"Log file '{LOG_FILE}' should NOT exist before the student "
        "performs the checksum verification step."
    )