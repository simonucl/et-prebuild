# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating system /
# file-system **before** the learner starts modifying anything.
#
# It asserts that:
#   1. The directory /home/user/site-config/ exists and is writable.
#   2. The file /home/user/site-config/users.conf exists with the expected
#      four-line content (and nothing more).
#   3. The file /home/user/site-config/user_update.log is not present yet.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest

SITE_CONFIG_DIR = Path("/home/user/site-config")
USERS_CONF_FILE = SITE_CONFIG_DIR / "users.conf"
LOG_FILE = SITE_CONFIG_DIR / "user_update.log"

# Expected initial content of users.conf
EXPECTED_INITIAL_USERS_CONF = (
    "alice:admin\n"
    "bob:editor\n"
    "charlie:viewer\n"
    "diana:viewer\n"
)


def test_site_config_directory_exists_and_writable():
    """
    The directory /home/user/site-config/ must already exist and be writable
    by the current user so that the student can modify its contents.
    """
    assert SITE_CONFIG_DIR.exists(), (
        f"Required directory {SITE_CONFIG_DIR} is missing. "
        "Create it before proceeding."
    )
    assert SITE_CONFIG_DIR.is_dir(), (
        f"{SITE_CONFIG_DIR} exists but is not a directory."
    )
    assert os.access(SITE_CONFIG_DIR, os.W_OK), (
        f"Directory {SITE_CONFIG_DIR} is not writable by the current user."
    )


def test_users_conf_exists_with_expected_initial_content():
    """
    The users.conf file must exist and contain the four expected lines
    (with Unix newlines and no extra blank lines).
    """
    assert USERS_CONF_FILE.exists(), (
        f"Required file {USERS_CONF_FILE} is missing."
    )
    assert USERS_CONF_FILE.is_file(), (
        f"{USERS_CONF_FILE} exists but is not a regular file."
    )

    # Read the file exactly as bytes to avoid newline translation issues
    actual_content = USERS_CONF_FILE.read_bytes()
    expected_content = EXPECTED_INITIAL_USERS_CONF.encode()

    assert actual_content == expected_content, (
        f"{USERS_CONF_FILE} does not match the expected initial content.\n"
        "---- Expected ----\n"
        f"{EXPECTED_INITIAL_USERS_CONF!r}\n"
        "---- Found ----\n"
        f"{actual_content.decode(errors='replace')!r}\n"
        "Please restore the file so it matches the expected starting point."
    )


def test_log_file_absent_initially():
    """
    user_update.log must *not* exist yet.  Its presence would indicate
    that the final state was applied before the tests that check the
    initial state were executed.
    """
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists, but it should be created *after* the "
        "required modifications are performed."
    )