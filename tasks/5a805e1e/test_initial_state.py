# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the expected *initial* state, before any credential-rotation
# work begins.  It intentionally avoids touching or asserting about
# any files or directories that the rotation procedure is supposed to
# create or modify later on.

import os
from pathlib import Path

import pytest

# Constants describing the expected initial state
SECURE_APP_DIR = Path("/home/user/projects/secure-app")
ENV_FILE = SECURE_APP_DIR / ".env"

EXPECTED_ENV_LINES = [
    "OLD_API_KEY=oldkey123",
    "OLD_SECRET=oldsecret321",
]


def test_secure_app_directory_exists():
    """
    The secure-app project directory must already be present before
    rotation begins.
    """
    assert SECURE_APP_DIR.is_dir(), (
        f"Expected directory {SECURE_APP_DIR} is missing. "
        "Make sure the project has been checked out to the correct path."
    )


def test_env_file_exists():
    """
    The original .env file must be present so that it can later be moved
    to the rotation folder.
    """
    assert ENV_FILE.is_file(), (
        f"Expected .env file at {ENV_FILE} is missing. "
        "Ensure the project contains the credentials file before rotating."
    )


def test_env_file_contents_are_correct():
    """
    The .env file must contain exactly the two legacy credentials lines,
    in the specified order, with no extra lines or whitespace.
    """
    with ENV_FILE.open("r", encoding="utf-8") as fh:
        # Read and normalise line endings / trailing whitespace
        content_lines = [ln.rstrip("\n\r") for ln in fh.read().splitlines()]

    assert content_lines == EXPECTED_ENV_LINES, (
        f"The contents of {ENV_FILE} are not as expected.\n"
        f"Expected exactly:\n{EXPECTED_ENV_LINES!r}\n"
        f"Found:\n{content_lines!r}"
    )