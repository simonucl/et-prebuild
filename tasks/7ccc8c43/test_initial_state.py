# test_initial_state.py
#
# Pytest suite to validate that the starting operating-system / file-system
# state is correct *before* the student performs any actions for the
# “Generate HTTP Status-Code Frequency Report” task.
#
# NOTE:  Per the authoring rules we **only** test for the existence and exact
#        content of the pre-existing log file.  We intentionally avoid any
#        assertion about the output directory or the report file that the
#        student is required to create.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

LOG_PATH = Path("/home/user/api_test/logs/responses.log")

_EXPECTED_CONTENT = """\
2024-01-01T10:00:00Z GET /users 200
2024-01-01T10:00:01Z POST /users 201
2024-01-01T10:00:02Z GET /accounts 200
2024-01-01T10:00:03Z GET /users/123 404
2024-01-01T10:00:04Z GET /users 200
2024-01-01T10:00:05Z PUT /accounts/456 400
2024-01-01T10:00:06Z DELETE /users/789 200
2024-01-01T10:00:07Z GET /users 200
2024-01-01T10:00:08Z POST /login 400
2024-01-01T10:00:09Z GET /users 200
2024-01-01T10:00:10Z GET /accounts 500
2024-01-01T10:00:11Z GET /users 200
2024-01-01T10:00:12Z PATCH /accounts/456 500
2024-01-01T10:00:13Z POST /users 201
2024-01-01T10:00:14Z GET /transactions 400
"""  # The file is expected to end with a single UNIX newline.

# --------------------------------------------------------------------------- #
# Helper(s)
# --------------------------------------------------------------------------- #


def read_file_contents(path: Path) -> str:
    """Return the full textual contents of *path*."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


def test_responses_log_exists_and_is_file():
    """Verify that the responses.log file exists and is a regular file."""
    assert LOG_PATH.exists(), (
        f"Pre-existing log file not found at expected location: {LOG_PATH}"
    )
    assert LOG_PATH.is_file(), (
        f"Expected {LOG_PATH} to be a file, but something else exists there."
    )
    # Basic sanity: file should not be empty
    assert LOG_PATH.stat().st_size > 0, f"{LOG_PATH} should not be empty."


def test_responses_log_content_is_exact():
    """
    Verify that the responses.log file contains exactly the expected lines.

    This guards against accidental mutation or truncation of the fixture
    before the student starts working.
    """
    actual = read_file_contents(LOG_PATH)

    assert (
        actual == _EXPECTED_CONTENT
    ), (
        "The content of /home/user/api_test/logs/responses.log does not match "
        "the expected fixture.\n"
        "If this file has been altered, restore it before proceeding."
    )