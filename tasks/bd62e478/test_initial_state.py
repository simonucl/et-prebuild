# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the expected initial state **before** the student executes
# any provisioning command.
#
# The truth value for this exercise dictates that the following
# objects must already exist:
#
#   1. Directory : /home/user/provisioning
#   2. File      : /home/user/provisioning/infra.env
#   3. Contents  : Exactly two lines—
#        APP_ENV=production\n
#        MAX_CONNECTIONS=200\n
#
# The tests below assert the presence of these objects and verify the
# file’s byte-for-byte contents.  Any failure pinpoints what is missing
# or incorrect so that the baseline image can be fixed **before** the
# student attempts the task.
#
# Only Python’s standard library and pytest are used, per the rules.

import os
from pathlib import Path

import pytest

HOME_DIR = Path("/home/user").expanduser().resolve()
PROVISIONING_DIR = HOME_DIR / "provisioning"
ENV_FILE = PROVISIONING_DIR / "infra.env"

EXPECTED_CONTENT = b"APP_ENV=production\nMAX_CONNECTIONS=200\n"
EXPECTED_SIZE = len(EXPECTED_CONTENT)  # 33 bytes


def _common_failure_msg(item: Path, what: str) -> str:
    """
    Helper to generate a clear error message when an expected filesystem
    object is missing or of the wrong type.
    """
    return (
        f"Expected {what} at absolute path '{item}'.\n"
        f"Current state:\n"
        f"  Exists : {item.exists()}\n"
        f"  Is dir : {item.is_dir()}\n"
        f"  Is file: {item.is_file()}"
    )


def test_provisioning_directory_exists():
    """The provisioning directory must pre-exist."""
    assert PROVISIONING_DIR.exists(), _common_failure_msg(PROVISIONING_DIR, "directory")
    assert PROVISIONING_DIR.is_dir(), _common_failure_msg(PROVISIONING_DIR, "directory")


def test_env_file_exists():
    """The infra.env file must pre-exist inside the provisioning directory."""
    assert ENV_FILE.exists(), _common_failure_msg(ENV_FILE, "file")
    assert ENV_FILE.is_file(), _common_failure_msg(ENV_FILE, "file")


def test_env_file_contents_and_size():
    """
    The infra.env file must contain exactly the two required lines
    and be the correct byte size (33 bytes).
    """
    with ENV_FILE.open("rb") as f:
        data = f.read()

    # Validate byte-for-byte contents.
    assert (
        data == EXPECTED_CONTENT
    ), (
        "File '/home/user/provisioning/infra.env' does not contain the expected "
        "exact contents.\n\n"
        "Expected (hex):\n"
        f"{EXPECTED_CONTENT.hex(' ')}\n\n"
        "Actual (hex):\n"
        f"{data.hex(' ')}"
    )

    # Validate size explicitly for completeness.
    assert (
        len(data) == EXPECTED_SIZE
    ), (
        f"File '/home/user/provisioning/infra.env' has incorrect size.\n"
        f"Expected: {EXPECTED_SIZE} bytes\n"
        f"Actual  : {len(data)} bytes"
    )