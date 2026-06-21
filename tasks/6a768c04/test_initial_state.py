# test_initial_state.py
#
# This test suite validates the **initial** filesystem state that must be
# present before the student performs the migration task.  It purposefully
# avoids checking for any of the *output* paths that the student is expected
# to create, in accordance with the grading rubric.
#
# What is verified here:
#
# 1. /home/user/legacy_configs exists and is a directory.
# 2. /home/user/legacy_configs/payment_service.conf exists and
#    contains exactly the four expected lines in the expected order.
#
# If any of these assertions fail, the student is starting from an
# unexpected state and the assignment should be fixed before continuing.
#
# The tests rely solely on the Python standard library and pytest.

import os
import pytest

LEGACY_DIR = "/home/user/legacy_configs"
LEGACY_CONF = os.path.join(LEGACY_DIR, "payment_service.conf")

EXPECTED_LEGACY_CONTENT = [
    "SERVICE_NAME=payment",
    "SERVICE_PORT=8080",
    "DB_HOST=localhost",
    "DB_PORT=5432",
]


def test_legacy_directory_exists():
    """Verify that the legacy configuration directory is present."""
    assert os.path.isdir(
        LEGACY_DIR
    ), f"Required directory {LEGACY_DIR} is missing or not a directory."


def test_legacy_config_file_exists():
    """Verify that the legacy configuration file is present."""
    assert os.path.isfile(
        LEGACY_CONF
    ), f"Required configuration file {LEGACY_CONF} is missing."


def test_legacy_config_file_contents():
    """Verify that the legacy configuration file has exactly the expected contents."""
    with open(LEGACY_CONF, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    assert (
        lines == EXPECTED_LEGACY_CONTENT
    ), (
        f"{LEGACY_CONF} does not contain the expected contents.\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_LEGACY_CONTENT)
        + "\n\nActual lines:\n"
        + "\n".join(lines)
    )