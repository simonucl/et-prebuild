# test_initial_state.py
"""
pytest suite that validates the required *initial* filesystem state
before the credential-rotation script is executed.

Only the pre-conditions explicitly guaranteed in the task description
are asserted here.  If any of these tests fail, the environment is not
in the expected starting state and the rotation procedure cannot
proceed safely.
"""

import os
from pathlib import Path

import pytest

# ----------------------------------------------------------------------
# CONSTANTS – hard-coded absolute paths per the task specification
# ----------------------------------------------------------------------

HOME = Path("/home/user")
PIPELINE_DIR = HOME / "data_pipeline"
CONFIG_DIR = PIPELINE_DIR / "config"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.env"

EXPECTED_INITIAL_CREDENTIALS = [
    "DB_USER=analytics_user",
    "DB_PASSWORD=oldPass123",
    "API_KEY=oldApiKey456",
]


# ----------------------------------------------------------------------
# TESTS
# ----------------------------------------------------------------------

def test_pipeline_directories_exist():
    """
    The data_pipeline and its config sub-directory must already exist.
    """
    assert PIPELINE_DIR.is_dir(), (
        f"Required directory missing: {PIPELINE_DIR}.\n"
        "The rotation procedure expects the data_pipeline directory "
        "to be present before it starts."
    )
    assert CONFIG_DIR.is_dir(), (
        f"Required directory missing: {CONFIG_DIR}.\n"
        "The rotation procedure expects the config directory to be "
        "present before it starts."
    )


def test_initial_credentials_file_exists_and_contents():
    """
    The credentials.env file must exist and contain exactly the three
    original key/value pairs in the correct order.
    """
    assert CREDENTIALS_FILE.is_file(), (
        f"Required credential file missing: {CREDENTIALS_FILE}.\n"
        "The rotation procedure needs this file to back up and replace."
    )

    # Read raw lines preserving newline characters to validate count
    with CREDENTIALS_FILE.open("r", encoding="utf-8") as fp:
        raw_lines = fp.readlines()

    # Strip only the trailing newline for content comparison
    stripped_lines = [ln.rstrip("\n") for ln in raw_lines]

    assert len(
        stripped_lines
    ) == 3, (
        f"{CREDENTIALS_FILE} must contain exactly 3 lines, "
        f"found {len(stripped_lines)}."
    )

    assert (
        stripped_lines == EXPECTED_INITIAL_CREDENTIALS
    ), (
        f"{CREDENTIALS_FILE} contents do not match the expected initial "
        "credentials.\n"
        "Expected:\n"
        + "\n".join(EXPECTED_INITIAL_CREDENTIALS)
        + "\nFound:\n"
        + "\n".join(stripped_lines)
    )