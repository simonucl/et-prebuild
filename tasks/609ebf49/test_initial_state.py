# test_initial_state.py
"""
Pytest suite that asserts the *initial* filesystem state is exactly as
expected **before** the remediation steps are carried out.

Only the standard library and pytest are used.
"""

import os
import stat
import filecmp
import pytest

HOME = "/home/user"
WEBAPP_ROOT = os.path.join(HOME, "webapp")

INDEX_PHP = os.path.join(WEBAPP_ROOT, "index.php")
SCRIPTS_DIR = os.path.join(WEBAPP_ROOT, "scripts")
DEPLOY_SH = os.path.join(SCRIPTS_DIR, "deploy.sh")
CONFIG_DIR = os.path.join(WEBAPP_ROOT, "config")
SETTINGS_INI = os.path.join(CONFIG_DIR, "settings.ini")
SETTINGS_BAK = os.path.join(CONFIG_DIR, "settings.ini.bak")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def octal_mode(path):
    """
    Return the permission bits of *path* as an integer in octal form.
    """
    return stat.S_IMODE(os.lstat(path).st_mode)


def assert_path_mode(path, expected_mode):
    """
    Assert that *path* exists and has the given *expected_mode*.
    """
    assert os.path.exists(path), f"Expected path {path} to exist."
    mode = octal_mode(path)
    assert mode == expected_mode, (
        f"{path} has mode {mode:04o}; expected {expected_mode:04o}"
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directory_tree_presence_and_permissions():
    """
    Ensure the directory hierarchy exists with the expected permissions.
    """
    # /home/user/webapp/ (0755)
    assert_path_mode(WEBAPP_ROOT, 0o755)

    # /home/user/webapp/scripts/ (0777) – insecure on purpose
    assert_path_mode(SCRIPTS_DIR, 0o777)

    # /home/user/webapp/config/ (0755)
    assert_path_mode(CONFIG_DIR, 0o755)


def test_file_presence_and_permissions():
    """
    Verify that the key files exist with their initial permissions.
    """
    # /home/user/webapp/index.php (0644)
    assert_path_mode(INDEX_PHP, 0o644)

    # /home/user/webapp/scripts/deploy.sh (0777) – insecure on purpose
    assert_path_mode(DEPLOY_SH, 0o777)

    # /home/user/webapp/config/settings.ini (0644)
    assert_path_mode(SETTINGS_INI, 0o644)

    # /home/user/webapp/config/settings.ini.bak (0644)
    assert_path_mode(SETTINGS_BAK, 0o644)


def test_settings_ini_content():
    """
    settings.ini must contain exactly one line: 'disable-auth = true\\n'
    """
    with open(SETTINGS_INI, "r", encoding="utf-8") as f:
        content = f.read()

    expected_line = "disable-auth = true\n"
    assert content == expected_line, (
        f"{SETTINGS_INI} content mismatch.\n"
        f"Expected exactly: {repr(expected_line)}\n"
        f"Got: {repr(content)}"
    )


def test_backup_is_identical_to_original():
    """
    The obsolete backup file must be present and identical to settings.ini
    in the initial state.
    """
    identical = filecmp.cmp(SETTINGS_INI, SETTINGS_BAK, shallow=False)
    assert identical, (
        f"{SETTINGS_BAK} is expected to be an exact copy of {SETTINGS_INI}"
    )