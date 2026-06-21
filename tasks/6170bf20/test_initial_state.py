# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before**
# the student (or automated script) begins the “credential rotation &
# dependency refresh” task.  Any failure here means the playground
# already deviates from the documented starting conditions and the
# subsequent grading logic would be unreliable.
#
# Convention:  /home/user is the home directory available to the student.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
MICROSERVICE_DIR = HOME / "microservice"
MICROSERVICE_ENV = MICROSERVICE_DIR / ".env"
SEC_ROTATION_DIR = HOME / "security_rotation"         # Must NOT exist yet!
BACKUP_DIR = SEC_ROTATION_DIR / "backup"
PACKAGES_DIR = SEC_ROTATION_DIR / "packages"
LOGS_DIR = SEC_ROTATION_DIR / "logs"


@pytest.fixture(scope="module")
def original_env_contents():
    """
    Read and return the contents of /home/user/microservice/.env
    so we can validate it in multiple tests if necessary.
    """
    if not MICROSERVICE_ENV.exists():
        pytest.skip(f"{MICROSERVICE_ENV} is missing – cannot read contents.")
    return MICROSERVICE_ENV.read_bytes()


def test_microservice_directory_exists():
    """The /home/user/microservice directory must already exist before work starts."""
    assert MICROSERVICE_DIR.exists(), f"Expected directory {MICROSERVICE_DIR} to exist."
    assert MICROSERVICE_DIR.is_dir(), f"{MICROSERVICE_DIR} exists but is not a directory."


def test_old_env_file_exists_and_has_expected_content(original_env_contents):
    """
    The initial .env must contain exactly the two legacy credentials with
    a newline after each line.
    """
    expected = b"API_KEY=oldkey123\nAPI_SECRET=oldsecret456\n"
    assert MICROSERVICE_ENV.exists(), f"Expected file {MICROSERVICE_ENV} to exist."
    assert MICROSERVICE_ENV.is_file(), f"{MICROSERVICE_ENV} exists but is not a regular file."
    assert original_env_contents == expected, (
        "The original .env file does not match the expected legacy contents.\n"
        "Expected:\n"
        "  API_KEY=oldkey123\n"
        "  API_SECRET=oldsecret456\n"
        "(with a trailing newline)\n"
        f"Actual bytes:\n{original_env_contents!r}"
    )


def test_security_rotation_workspace_not_present_yet():
    """
    The /home/user/security_rotation workspace (and any of its sub-directories)
    should NOT exist before the student starts the task.  Its presence would
    indicate that work has already begun or that the playground is dirty.
    """
    assert not SEC_ROTATION_DIR.exists(), (
        f"Found unexpected directory {SEC_ROTATION_DIR}. "
        "The security_rotation workspace should not exist before the task begins."
    )


def test_no_premature_backup_or_artifacts():
    """
    Ensure none of the rotation artifacts already exist.  Their presence would
    break the 'initial state' contract.
    """
    unexpected_paths = [
        BACKUP_DIR,
        PACKAGES_DIR,
        LOGS_DIR,
        BACKUP_DIR / ".env",
        PACKAGES_DIR / "packages_to_upgrade.txt",
        PACKAGES_DIR / "requests-2.31.0.pkg",
        PACKAGES_DIR / "cryptography-42.0.1.pkg",
        LOGS_DIR / "rotation.log",
    ]
    for path in unexpected_paths:
        assert not path.exists(), (
            f"Unexpected pre-existing path detected: {path}. "
            "No rotation artifacts should exist before the task starts."
        )