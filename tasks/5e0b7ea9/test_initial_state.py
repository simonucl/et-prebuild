# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system /
# file-system **before** the student makes any changes.
#
# RULES (re-stated from the instructions)
#   • Never test for artefacts that must be produced by the student – only check
#     the pre-existing environment.
#   • Use absolute paths everywhere.
#   • Provide clear assertion messages so that a missing or malformed resource
#     is easy to diagnose.

import os
import textwrap
import pytest

# --------------------------------------------------------------------------- #
# Paths that must already exist
# --------------------------------------------------------------------------- #

CONFIG_PATH = "/home/user/webapp/config/server.env"
TMP_DIR     = "/home/user/webapp/tmp"
LOG_PATH    = "/home/user/webapp/logs/webapp.log"

# --------------------------------------------------------------------------- #
# Expected baseline contents
# --------------------------------------------------------------------------- #

EXPECTED_SERVER_ENV = textwrap.dedent("""\
    APP_PORT=8080
    LOG_LEVEL=info
    DB_HOST=localhost
""").splitlines()  # intentionally strip the trailing '\n' for comparison

EXPECTED_LOG_LINES = [
    "2023-10-09 12:34:56 [DEBUG] Connected to database",
    "2023-10-09 12:35:01 [INFO]  Request processed",
    "2023-10-09 12:35:02 [DEBUG] Cache miss for key: user_123",
    "2023-10-09 12:35:04 [ERROR] Failed to send email",
    "2023-10-09 12:35:05 [DEBUG] Retrying request id: 456",
]

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_config_file_exists_with_correct_content():
    """The server.env file must be present *and* still be on LOG_LEVEL=info."""
    assert os.path.isfile(CONFIG_PATH), (
        f"Expected config file at {CONFIG_PATH} to exist before any work starts."
    )

    with open(CONFIG_PATH, encoding="utf-8") as fh:
        contents = fh.read().splitlines()

    assert contents == EXPECTED_SERVER_ENV, (
        "The initial /home/user/webapp/config/server.env file does not match "
        "the expected baseline. Make sure you have not modified it yet."
    )


def test_tmp_directory_exists():
    """The tmp directory must already be in place (empty is fine)."""
    assert os.path.isdir(TMP_DIR), (
        f"Expected directory {TMP_DIR} to exist before the task begins."
    )


def test_log_file_exists_and_has_expected_lines():
    """
    The historical log file must be present and start with the five canonical
    lines that the exercise describes.
    """
    assert os.path.isfile(LOG_PATH), (
        f"Expected log file at {LOG_PATH} to exist before any work starts."
    )

    with open(LOG_PATH, encoding="utf-8") as fh:
        log_lines = fh.read().splitlines()

    # The log might grow over time, but the first five lines must be identical
    # to the canonical sample provided in the task description.
    assert log_lines[:5] == EXPECTED_LOG_LINES, (
        "The initial contents of webapp.log do not match the expected baseline. "
        "Make sure the exercise is started from a clean slate."
    )

    # Sanity-check: ensure there are at least three '[DEBUG]' lines present.
    debug_count = sum(1 for line in log_lines if "[DEBUG]" in line)
    assert debug_count >= 3, "Expected at least three '[DEBUG]' lines in the log."