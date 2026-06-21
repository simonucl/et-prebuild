# test_initial_state.py
"""
Pytest suite that validates the operating-system / filesystem *before* the student
performs any action for the “Log the SHA-256 signature of the retired credential file” task.

Rules enforced:
1. The file /home/user/secrets/old_credentials.txt must exist and be a regular file.
2. The file must be zero bytes in size (it has been “shredded” to empty).
3. The SHA-256 digest of the file must match the well-known digest of an empty file:
   e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

No checks are performed on any output artefacts that the student will create
(e.g. /home/user/rotation or its contents).
"""

import hashlib
import os
import stat
import pytest

# Absolute path to the credential file that must pre-exist
CREDENTIAL_PATH = "/home/user/secrets/old_credentials.txt"
EMPTY_FILE_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)


@pytest.fixture(scope="module")
def credential_stat():
    """
    Return the os.stat_result for the credential file.
    A single stat call is shared by all tests in this module.
    """
    try:
        return os.stat(CREDENTIAL_PATH)
    except FileNotFoundError as exc:
        pytest.skip(f"Required file not found: {CREDENTIAL_PATH}")  # Will be asserted explicitly


def test_credential_file_exists(credential_stat):
    """
    Verify that the credential file exists and is a regular file.
    """
    assert os.path.exists(
        CREDENTIAL_PATH
    ), f"Expected file {CREDENTIAL_PATH} to exist, but it is missing."

    assert stat.S_ISREG(
        credential_stat.st_mode
    ), f"Expected {CREDENTIAL_PATH} to be a regular file, but it is not."


def test_credential_file_is_empty(credential_stat):
    """
    The file must be zero bytes in size.
    """
    assert (
        credential_stat.st_size == 0
    ), f"Expected {CREDENTIAL_PATH} to be empty (0 bytes), but size is {credential_stat.st_size} bytes."


def test_credential_file_sha256_is_correct():
    """
    Compute the SHA-256 digest of the file and ensure it matches the known digest
    of an empty file.
    """
    # Read the entire file (should be zero bytes)
    try:
        with open(CREDENTIAL_PATH, "rb") as f:
            file_bytes = f.read()
    except FileNotFoundError:
        pytest.fail(f"Required file {CREDENTIAL_PATH} does not exist for SHA-256 check.")

    digest = hashlib.sha256(file_bytes).hexdigest()

    assert (
        digest == EMPTY_FILE_SHA256
    ), (
        f"SHA-256 digest mismatch for {CREDENTIAL_PATH}.\n"
        f"Expected: {EMPTY_FILE_SHA256}\n"
        f"Found   : {digest}"
    )