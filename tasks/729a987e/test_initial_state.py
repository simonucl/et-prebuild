# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state **before** the
# student carries out any actions for the “myapp” configuration-management task.
#
# Rules enforced:
#   1. /home/user/myapp must exist and contain exactly one file: config.ini
#   2. /home/user/myapp/config.ini must contain the expected four lines with a
#      final newline and the port set to 8080.
#   3. /home/user/myapp/config.ini.bak must *not* exist yet.
#   4. /home/user/config-change-log.json must *not* exist yet.
#
# If any assertion fails, the error message explains precisely what is wrong
# so the learner knows what prerequisite is missing or incorrect.

import os
import stat
import pytest

HOME = "/home/user"
MYAPP_DIR = os.path.join(HOME, "myapp")
CONFIG_FILE = os.path.join(MYAPP_DIR, "config.ini")
BACKUP_FILE = CONFIG_FILE + ".bak"
AUDIT_LOG = os.path.join(HOME, "config-change-log.json")

EXPECTED_CONFIG_BYTES = (
    b"[service]\n"
    b"name=myapp\n"
    b"port=8080\n"
    b"debug=false\n"
)


def test_myapp_directory_exists_and_is_directory():
    assert os.path.exists(MYAPP_DIR), (
        f"Required directory {MYAPP_DIR!r} is missing. "
        "Create it before proceeding."
    )
    assert stat.S_ISDIR(os.stat(MYAPP_DIR).st_mode), (
        f"{MYAPP_DIR!r} exists but is not a directory."
    )


def test_config_file_exists_and_is_regular_file():
    assert os.path.exists(CONFIG_FILE), (
        f"Required file {CONFIG_FILE!r} is missing."
    )
    assert stat.S_ISREG(os.stat(CONFIG_FILE).st_mode), (
        f"{CONFIG_FILE!r} exists but is not a regular file."
    )


def test_config_file_contents_match_expected():
    with open(CONFIG_FILE, "rb") as fh:
        data = fh.read()
    assert data == EXPECTED_CONFIG_BYTES, (
        "The contents of config.ini do not match the expected initial state.\n"
        "Expected (repr):\n"
        f"{EXPECTED_CONFIG_BYTES!r}\n"
        "Found (repr):\n"
        f"{data!r}"
    )


def test_no_extra_files_in_myapp_directory():
    # Only config.ini should be present at start.
    files = sorted(os.listdir(MYAPP_DIR))
    assert files == ["config.ini"], (
        f"Unexpected files or directories found in {MYAPP_DIR!r}: {files}. "
        "Only 'config.ini' should be present prior to making changes."
    )


def test_backup_file_does_not_exist_yet():
    assert not os.path.exists(BACKUP_FILE), (
        f"Backup file {BACKUP_FILE!r} should not exist before any changes are made."
    )


def test_audit_log_does_not_exist_yet():
    assert not os.path.exists(AUDIT_LOG), (
        f"Audit log {AUDIT_LOG!r} should not exist before any changes are made."
    )