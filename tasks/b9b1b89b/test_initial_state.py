# test_initial_state.py
"""
Pytest suite to validate the initial filesystem state **before** the student
runs any commands for the “Android application release summary” exercise.

This file checks that:
1. The expected directory structure already exists.
2. app_build.ini is present and contains the required keys / values.
3. No latest_build.conf file exists yet (it must be created by the student).

Only the Python standard library and pytest are used.
"""

import os
import stat
import configparser
import pytest

# ----- CONSTANTS -------------------------------------------------------------

HOME = "/home/user"
ROOT_DIR = os.path.join(HOME, "mobile_build")
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
INI_PATH = os.path.join(CONFIG_DIR, "app_build.ini")
EXPECTED_VALUES = {
    ("build", "build_flavor"): "production",
    ("build", "min_sdk"): "21",
    ("build", "target_sdk"): "34",
    ("version", "version_name"): "2.3.5",
    ("version", "version_code"): "235",
}
LATEST_CONF = os.path.join(LOGS_DIR, "latest_build.conf")
DIR_PERMS = 0o700  # expected directory permissions


# ----- HELPER FUNCTIONS ------------------------------------------------------


def _assert_dir(path: str, perms: int):
    """
    Assert that a path exists, is a directory, and has the specified permissions.
    """
    assert os.path.exists(path), f"Expected directory {path} to exist."
    assert os.path.isdir(path), f"Expected {path} to be a directory."
    st_mode = os.stat(path).st_mode
    actual_perms = stat.S_IMODE(st_mode)
    assert (
        actual_perms == perms
    ), f"Directory {path} permissions are {oct(actual_perms)}, expected {oct(perms)}."


# ----- TESTS -----------------------------------------------------------------


def test_directory_structure_and_permissions():
    """
    The root, config, and logs directories must exist with 0700 permissions.
    """
    _assert_dir(ROOT_DIR, DIR_PERMS)
    _assert_dir(CONFIG_DIR, DIR_PERMS)
    _assert_dir(LOGS_DIR, DIR_PERMS)


def test_app_build_ini_exists_and_contains_expected_values():
    """
    app_build.ini must be present, parse correctly, and contain the expected
    key/value pairs in their respective sections.
    """
    assert os.path.exists(
        INI_PATH
    ), f"Config file {INI_PATH} is missing. It must exist before the task starts."

    config = configparser.ConfigParser()
    read_files = config.read(INI_PATH)
    assert (
        read_files
    ), f"ConfigParser could not read {INI_PATH}. Ensure the file is readable."

    missing_entries = []
    wrong_values = []

    for (section, key), expected_val in EXPECTED_VALUES.items():
        if not config.has_section(section):
            missing_entries.append(f"[{section}] (entire section missing)")
            continue

        if not config.has_option(section, key):
            missing_entries.append(f"{section}.{key}")
            continue

        actual_val = config.get(section, key)
        if actual_val != expected_val:
            wrong_values.append(
                f"{section}.{key} = {actual_val!r} (expected {expected_val!r})"
            )

    assert (
        not missing_entries
    ), f"The following INI entries are missing: {', '.join(missing_entries)}"
    assert (
        not wrong_values
    ), "The following INI entries have incorrect values:\n" + "\n".join(wrong_values)


def test_latest_build_conf_does_not_exist_yet():
    """
    latest_build.conf must NOT exist before the student's solution runs.
    """
    assert not os.path.exists(
        LATEST_CONF
    ), f"{LATEST_CONF} already exists, but it should be created by the student's commands."