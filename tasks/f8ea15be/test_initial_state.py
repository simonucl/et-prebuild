# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating-system /
# file-system for the “string-service” exercise **before** the student makes
# any changes.  All checks are performed against absolute paths under
# /home/user.  Failures should clearly describe the missing or incorrect
# prerequisite.

import os
import pytest

ROOT_DIR = "/home/user/string-service"
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
ENV_CONF = os.path.join(CONFIG_DIR, "env.conf")
LOG_FILE = os.path.join(LOGS_DIR, "translation_update.log")


def _assert_is_dir(path: str) -> None:
    assert os.path.isdir(path), f"Required directory missing: {path!r}"


def _assert_is_file(path: str) -> None:
    assert os.path.isfile(path), f"Required file missing: {path!r}"


def test_directory_structure():
    """
    Verify that the expected directory hierarchy exists:
        /home/user/string-service/
        /home/user/string-service/config/
        /home/user/string-service/logs/
    """
    _assert_is_dir(ROOT_DIR)
    _assert_is_dir(CONFIG_DIR)
    _assert_is_dir(LOGS_DIR)


def test_env_conf_initial_content():
    """
    The config file must exist and contain exactly one line:
        LOCALE="en_US"
    A trailing newline is permissible, but *no* additional lines
    or characters are allowed.
    """
    _assert_is_file(ENV_CONF)

    with open(ENV_CONF, "r", encoding="utf-8") as fp:
        contents = fp.read()

    # Splitlines removes trailing newline and is unambiguous for this test
    lines = contents.splitlines()
    assert lines == ['LOCALE="en_US"'], (
        f"{ENV_CONF!r} is expected to contain only "
        'LOCALE="en_US" on a single line; current contents: {lines!r}'
    )


def test_log_file_exists_and_is_empty():
    """
    The translation log file must exist and be *empty* (zero bytes)
    before the student performs any action.
    """
    _assert_is_file(LOG_FILE)

    size = os.stat(LOG_FILE).st_size
    assert size == 0, (
        f"{LOG_FILE!r} should be empty (0 bytes) initially, "
        f"but its size is {size} bytes."
    )