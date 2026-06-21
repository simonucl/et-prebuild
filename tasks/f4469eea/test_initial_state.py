# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the student performs any actions.  It checks that the
# two configuration files are present with their expected
# default contents, and that the companion change-log does *not*
# yet exist.

import os
import pytest

HOME = "/home/user"
SYS_CONFIG_DIR = os.path.join(HOME, "system_config")
TZ_CONF = os.path.join(SYS_CONFIG_DIR, "timezone.conf")
LOCALE_CONF = os.path.join(SYS_CONFIG_DIR, "locale.conf")

CONFIG_CHANGES_DIR = os.path.join(HOME, "config-changes")
CHANGE_LOG = os.path.join(CONFIG_CHANGES_DIR, "time_locale.log")


@pytest.mark.describe("Initial configuration files must exist with default contents")
def test_timezone_conf_exists_with_default_content():
    """
    /home/user/system_config/timezone.conf must exist and contain exactly:
        TIMEZONE=UTC\n
    """
    assert os.path.isfile(TZ_CONF), (
        f"Missing file: {TZ_CONF}. It should already exist before you start."
    )
    with open(TZ_CONF, "r", encoding="utf-8") as f:
        content = f.read()
    expected = "TIMEZONE=UTC\n"
    assert content == expected, (
        f"{TZ_CONF} has unexpected contents.\n"
        f"Expected exactly (including trailing newline): {repr(expected)}\n"
        f"Found: {repr(content)}"
    )


def test_locale_conf_exists_with_default_content():
    """
    /home/user/system_config/locale.conf must exist and contain exactly:
        LANG=C\n
    """
    assert os.path.isfile(LOCALE_CONF), (
        f"Missing file: {LOCALE_CONF}. It should already exist before you start."
    )
    with open(LOCALE_CONF, "r", encoding="utf-8") as f:
        content = f.read()
    expected = "LANG=C\n"
    assert content == expected, (
        f"{LOCALE_CONF} has unexpected contents.\n"
        f"Expected exactly (including trailing newline): {repr(expected)}\n"
        f"Found: {repr(content)}"
    )


@pytest.mark.describe("Change-log must NOT exist before any edits are made")
def test_change_log_does_not_exist_yet():
    """
    The daemon's change-log file should *not* be present before the student
    carries out the task.  Its presence would signal that changes were already
    attempted, which violates the initial-state contract.
    """
    assert not os.path.exists(CHANGE_LOG), (
        f"{CHANGE_LOG} already exists. The initial state should not contain "
        "this log file. Remove it before starting the task."
    )