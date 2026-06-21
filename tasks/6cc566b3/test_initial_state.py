# test_initial_state.py
#
# This pytest suite validates the initial state of the operating system
# that must exist *before* the student performs any actions for the
# “diagnostic snapshot” task.  It purposefully does NOT look for any of
# the output artefacts that the student will create (e.g. the diagnostics
# directory, the tar-ball, the remote copy, or the status log).  It only
# checks the required **source** data and that the expected directories
# and files are in place with the correct contents and permissions.
#
# Requirements validated here:
#   • /home/user/app/logs/app.log
#   • /home/user/app/config/settings.conf
#
# The tests give clear failure messages so that a missing or mis-configured
# prerequisite can be identified quickly.

import os
from pathlib import Path
import stat

import pytest

# ----- Constants ----------------------------------------------------------------

HOME = Path("/home/user")
APP_ROOT = HOME / "app"

LOG_DIR = APP_ROOT / "logs"
CONFIG_DIR = APP_ROOT / "config"

APP_LOG_FILE = LOG_DIR / "app.log"
SETTINGS_FILE = CONFIG_DIR / "settings.conf"

APP_LOG_CONTENT = "Log Start\n"
SETTINGS_CONTENT = "setting1=value1\nsetting2=value2\n"

FILE_MODE_EXPECTED = 0o644      # rw-r--r--
DIR_MODE_MIN = 0o755            # rwxr-xr-x (directories must be at least this open)


# ----- Helper utilities ----------------------------------------------------------

def _assert_path_is_dir(path: Path):
    assert path.exists(), f"Directory expected but missing: {path}"
    assert path.is_dir(), f"Path exists but is not a directory: {path}"
    mode = path.stat().st_mode & 0o777
    assert mode >= DIR_MODE_MIN, (
        f"Directory {path} exists but permissions are too restrictive "
        f"(expected at least {oct(DIR_MODE_MIN)}, found {oct(mode)})"
    )


def _assert_regular_file(path: Path, expected_content: str):
    assert path.exists(), f"Required file is missing: {path}"
    assert path.is_file(), f"Path exists but is not a regular file: {path}"

    # Check permissions
    mode = path.stat().st_mode & 0o777
    assert mode == FILE_MODE_EXPECTED, (
        f"File {path} permissions are incorrect. "
        f"Expected {oct(FILE_MODE_EXPECTED)}, found {oct(mode)}"
    )

    # Check exact content
    with path.open("r", encoding="utf-8") as fh:
        actual_content = fh.read()
    assert actual_content == expected_content, (
        f"File {path} content mismatch.\n"
        f"Expected:\n{repr(expected_content)}\n"
        f"Found:\n{repr(actual_content)}"
    )


# ----- Tests --------------------------------------------------------------------

def test_app_log_present_and_correct():
    """
    Ensure /home/user/app/logs/app.log exists with the exact
    expected content and permissions.
    """
    _assert_path_is_dir(LOG_DIR)
    _assert_regular_file(APP_LOG_FILE, APP_LOG_CONTENT)


def test_settings_conf_present_and_correct():
    """
    Ensure /home/user/app/config/settings.conf exists with the exact
    expected content and permissions.
    """
    _assert_path_is_dir(CONFIG_DIR)
    _assert_regular_file(SETTINGS_FILE, SETTINGS_CONTENT)