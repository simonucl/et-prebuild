# test_initial_state.py
#
# Pytest suite validating the *starting* operating-system / filesystem
# state for the “credential rotation” exercise.
#
# These tests must pass *before* the student carries out any actions.
# If any assertion fails, the student environment is not in the
# expected pristine state and the exercise itself would be invalid.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
SECRETS_DIR = HOME / ".secrets"
OLD_TOKEN_TXT = SECRETS_DIR / "old_api_token.txt"
OLD_TOKEN_BAK = SECRETS_DIR / "old_api_token.bak"
BENCHMARK_LOG = HOME / "credential_rotation_benchmark.log"

###############################################################################
# Helper utilities
###############################################################################

def assert_not_exists(path: Path, what: str) -> None:
    if path.exists():
        pytest.fail(f"{what} {path} should NOT exist in the initial state, "
                    "but it is already present. "
                    "Make sure to start from the clean environment provided.")

###############################################################################
# Tests
###############################################################################

def test_secrets_directory_exists_and_is_writable():
    """
    The directory /home/user/.secrets/ must exist *and* be writable
    by the current (regular) user.
    """
    assert SECRETS_DIR.exists(), f"Required directory {SECRETS_DIR} is missing."
    assert SECRETS_DIR.is_dir(), f"{SECRETS_DIR} exists but is not a directory."
    # Check that the user has write permission.
    mode = SECRETS_DIR.stat().st_mode
    writable = bool(mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
    assert writable, f"Directory {SECRETS_DIR} is not writable."


def test_only_old_token_txt_exists_with_correct_contents():
    """
    Validate that the *only* credential file present is the old token txt file
    and that its contents match the specification exactly.
    """
    # Positive check: old_api_token.txt must exist with expected content.
    assert OLD_TOKEN_TXT.exists(), f"Required file {OLD_TOKEN_TXT} is missing."
    assert OLD_TOKEN_TXT.is_file(), f"{OLD_TOKEN_TXT} exists but is not a regular file."

    expected_content = "OLD_TOKEN_qwerty\n"
    actual_content = OLD_TOKEN_TXT.read_text(encoding="utf-8")
    assert actual_content == expected_content, (
        f"File {OLD_TOKEN_TXT} contents mismatch.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Found:    {repr(actual_content)}"
    )

    # Negative checks: .bak file and new token (will be created later) must NOT yet exist.
    assert_not_exists(OLD_TOKEN_BAK, ".bak backup file")
    # A new token file would have the same path as the old token; since the old token
    # file exists, we already validated that. Nothing else to check here.


def test_benchmark_log_does_not_exist_initially():
    """
    The benchmark log is produced only AFTER the rotation logic runs.
    It must not exist in the pristine starting image.
    """
    assert_not_exists(BENCHMARK_LOG, "Benchmark log file")