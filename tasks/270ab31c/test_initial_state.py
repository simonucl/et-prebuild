# test_initial_state.py
#
# Pytest suite that validates the PRE-task operating-system / filesystem
# state for the “API credential rotation” exercise.
#
# Do NOT modify this file.  The tests must pass *before* the student starts
# doing any rotation steps.  If a test here fails, it means the starting
# environment is not as described in the assignment and the subsequent
# grading cannot be trusted.

import os
from pathlib import Path
import stat

import pytest


CREDS_DIR = Path("/home/user/creds")
CREDS_FILE = CREDS_DIR / "api_creds.json"

EXPECTED_INITIAL_JSON = (
    '{"api_key":"old_key_123","expires":"2023-01-01T00:00:00Z"}'
)


def _read_file_no_trailing_newline(path: Path) -> str:
    """
    Read the file and remove exactly one trailing newline if present.
    This lets the comparison accept files that either have or do not have
    a final '\n', while still rejecting any other whitespace differences.
    """
    data = path.read_text(encoding="utf-8")
    return data[:-1] if data.endswith("\n") else data


def test_creds_directory_exists_and_writable():
    assert CREDS_DIR.exists(), (
        f"Required directory {CREDS_DIR} is missing."
    )
    assert CREDS_DIR.is_dir(), (
        f"{CREDS_DIR} exists but is not a directory."
    )

    # Check write permission for the current user (no sudo required).
    can_write = os.access(CREDS_DIR, os.W_OK)
    mode = stat.filemode(CREDS_DIR.stat().st_mode)
    assert can_write, (
        f"Directory {CREDS_DIR} is not writable by the current user. "
        f"Observed permissions: {mode}"
    )


def test_creds_file_exists_with_expected_content():
    assert CREDS_FILE.exists(), (
        f"Credential file {CREDS_FILE} is missing."
    )
    assert CREDS_FILE.is_file(), (
        f"{CREDS_FILE} exists but is not a regular file."
    )

    actual_content = _read_file_no_trailing_newline(CREDS_FILE)
    assert actual_content == EXPECTED_INITIAL_JSON, (
        "Initial credential file content is incorrect.\n"
        f"Expected exactly:\n  {EXPECTED_INITIAL_JSON!r}\n"
        f"Found:\n  {actual_content!r}"
    )