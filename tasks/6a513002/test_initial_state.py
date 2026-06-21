# test_initial_state.py
#
# Pytest suite that validates the state of the filesystem *before* the student
# runs the required single-command solution.
#
# Checks performed:
#   1. /home/user/mock/api/greeting.json must already exist.
#   2. That file must contain *exactly* the expected one-line JSON string
#      with no leading/trailing whitespace or newline.
#   3. /home/user/api_test/curl_response.log must NOT exist yet.
#
# Only stdlib + pytest are used.

import os
from pathlib import Path

import pytest

GREETING_PATH = Path("/home/user/mock/api/greeting.json")
EXPECTED_GREETING_CONTENT = b'{"message":"Hello, integration test!"}'

RESPONSE_LOG_PATH = Path("/home/user/api_test/curl_response.log")


def test_greeting_json_exists_and_contents_are_correct():
    """Verify that the mock greeting.json file is present and correct."""
    assert GREETING_PATH.is_file(), (
        f"Required file not found: {GREETING_PATH}. "
        "It must exist before the student runs their command."
    )

    # Read raw bytes to ensure no extra newline or whitespace.
    content = GREETING_PATH.read_bytes()
    assert content == EXPECTED_GREETING_CONTENT, (
        f"Contents of {GREETING_PATH} are incorrect.\n"
        f"Expected exact bytes:\n{EXPECTED_GREETING_CONTENT!r}\n"
        f"Found:\n{content!r}"
    )


def test_response_log_does_not_yet_exist():
    """
    The output file should NOT exist before the student runs their single command.
    Its presence would indicate the task was already completed or that the
    environment is in an unexpected state.
    """
    assert not RESPONSE_LOG_PATH.exists(), (
        f"Output file {RESPONSE_LOG_PATH} already exists, "
        "but it should be created only by the student's command."
    )