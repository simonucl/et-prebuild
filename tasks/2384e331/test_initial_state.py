# test_initial_state.py
#
# This pytest file validates the *initial* state of the operating-system /
# file-system **before** the student performs any actions.
#
# What we expect to be present *already*:
#   • /home/user/project/release-2024-04-15.log  ← exact contents verified
#
# IMPORTANT:  We deliberately do **not** check for the eventual output
# artifacts (e.g. /home/user/project/deploy/ …) in keeping with the
# “DO NOT test for any of the output files or directories” rule.

import pathlib
import pytest

ROOT = pathlib.Path("/home/user/project")
RAW_LOG = ROOT / "release-2024-04-15.log"

EXPECTED_LOG_CONTENT = (
    "2024-04-15T08:00:01Z INFO  app-01 Starting deployment\n"
    "2024-04-15T08:00:05Z ERROR app-01 Failed to fetch artifact\n"
    "2024-04-15T08:00:10Z WARN  app-02 Slow response from repository\n"
    "2024-04-15T08:00:12Z ERROR app-02 Missing environment variable\n"
    "2024-04-15T08:00:15Z INFO  app-03 Deployment completed\n"
    "2024-04-15T08:00:18Z ERROR app-03 Timeout contacting service\n"
    "2024-04-15T08:00:20Z ERROR app-02 Port already in use\n"
    "2024-04-15T08:00:25Z INFO  app-01 Rollback initiated\n"
)

def test_raw_log_exists_and_is_file():
    """Verify that the raw application log exists and is a regular file."""
    assert RAW_LOG.exists(), (
        f"Required log file {RAW_LOG} is missing. "
        "It must be present before the student starts."
    )
    assert RAW_LOG.is_file(), (
        f"{RAW_LOG} exists but is not a regular file "
        "(perhaps it is a directory or symlink)."
    )


def test_raw_log_contents_are_exact():
    """Verify that the raw log file has exactly the expected byte contents."""
    actual = RAW_LOG.read_text(encoding="utf-8")
    assert actual == EXPECTED_LOG_CONTENT, (
        f"The contents of {RAW_LOG} do not match the expected initial state.\n"
        "Differences may indicate the environment was modified before the task "
        "began.\n"
        "Expected content:\n"
        "----------------\n"
        f"{EXPECTED_LOG_CONTENT}"
        "----------------\n"
        "Actual content:\n"
        "----------------\n"
        f"{actual}"
        "----------------"
    )