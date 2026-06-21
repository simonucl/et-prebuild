# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any action for the “site-admin” task.
#
# The tests confirm that:
#   • Required directories exist.
#   • Required files exist.
#   • File contents match the expected *initial* state only.
#   • No new content (e.g., the jdoe account or audit entry) has been added yet.
#
# Any failure message should immediately reveal what part of the initial
# environment is missing or already altered.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
SITE_ADMIN_DIR = HOME / "site-admin"
CONF_DIR = SITE_ADMIN_DIR / "conf"
LOGS_DIR = SITE_ADMIN_DIR / "logs"

ACCOUNTS_DB = CONF_DIR / "accounts.db"
ACCOUNT_LOG = LOGS_DIR / "account_changes.log"


@pytest.fixture(scope="module")
def expected_accounts_content():
    """
    Expected *initial* content of accounts.db, including the *single trailing
    newline* character.
    """
    return (
        "alice:1000:admin:active\n"
        "bob:1001:editor:inactive\n"
        "carol:1002:viewer:active\n"
    )


@pytest.fixture(scope="module")
def expected_log_content():
    """
    Expected *initial* content of account_changes.log, including the
    *single trailing newline* character.
    """
    return "[2023-01-14 09:30:00] ADD carol 1002 viewer active\n"


def _assert_single_trailing_newline(raw_bytes: bytes, file_path: Path):
    """
    Helper: ensure the file ends in exactly one newline and not two+.
    """
    assert raw_bytes.endswith(b"\n"), (
        f"{file_path} must end with a single trailing newline."
    )
    assert not raw_bytes.endswith(b"\n\n"), (
        f"{file_path} has more than one trailing newline."
    )


def test_directories_exist():
    """
    Validate that /home/user/site-admin directory hierarchy is present.
    """
    for directory in (SITE_ADMIN_DIR, CONF_DIR, LOGS_DIR):
        assert directory.is_dir(), f"Missing required directory: {directory}"


def test_files_exist():
    """
    Validate that the two required files are present and are regular files.
    """
    for file_path in (ACCOUNTS_DB, ACCOUNT_LOG):
        assert file_path.is_file(), f"Required file does not exist: {file_path}"


def test_accounts_db_initial_content(expected_accounts_content):
    """
    Validate accounts.db has *only* the initial three lines and the correct
    trailing newline; ensure the jdoe record has NOT yet been appended.
    """
    raw = ACCOUNTS_DB.read_bytes()
    _assert_single_trailing_newline(raw, ACCOUNTS_DB)

    text = raw.decode("utf-8")
    assert text == expected_accounts_content, (
        "accounts.db content is not in the expected initial state.\n"
        "It should contain exactly:\n"
        f"{expected_accounts_content!r}\n"
        f"Found instead:\n{text!r}"
    )
    # Explicitly confirm jdoe has not yet been added
    assert "jdoe:1003:editor:active" not in text, (
        "The new account line for 'jdoe' is already present. "
        "The initial state should *not* contain this line."
    )


def test_account_log_initial_content(expected_log_content):
    """
    Validate account_changes.log has exactly the initial single entry and
    a correct trailing newline; ensure the new audit line has NOT yet been
    appended.
    """
    raw = ACCOUNT_LOG.read_bytes()
    _assert_single_trailing_newline(raw, ACCOUNT_LOG)

    text = raw.decode("utf-8")
    assert text == expected_log_content, (
        "account_changes.log content is not in the expected initial state.\n"
        "It should contain exactly:\n"
        f"{expected_log_content!r}\n"
        f"Found instead:\n{text!r}"
    )
    # Explicitly confirm the future audit line is absent
    expected_future_line = "[2023-01-15 10:00:00] ADD jdoe 1003 editor active"
    assert expected_future_line not in text, (
        "The new audit trail line for 'jdoe' is already present. "
        "The initial state should *not* contain this line."
    )