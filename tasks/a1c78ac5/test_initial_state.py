# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state **before**
# any deployment actions are performed.  It confirms that only the two
# original configuration files exist under /home/user/app/config and
# that their contents and permissions match the expected baseline.
#
# If any test here fails it means the machine is not in the pristine
# state required by the assignment, so the student must fix the
# environment *before* attempting the deployment steps.

import os
from pathlib import Path
import stat
import pytest

# ---------------------------------------------------------------------------
# Constants describing the required initial state
# ---------------------------------------------------------------------------

APP_DIR = Path("/home/user/app")
CONFIG_DIR = APP_DIR / "config"
SETTINGS_PATH = CONFIG_DIR / "settings.yaml"
DATABASE_PATH = CONFIG_DIR / "database.toml"
BACKUP_DIR = CONFIG_DIR / "backup"
LOGS_DIR = APP_DIR / "logs"

EXPECTED_SETTINGS_CONTENT = (
    "service:\n"
    "  enabled: false\n"
    '  version: "1.4.3"\n'
    "  port: 8080\n"
    "logging:\n"
    '  level: "DEBUG"\n'
    '  format: "text"\n'
)

EXPECTED_DATABASE_CONTENT = (
    "[database]\n"
    'name = "test_db"\n'
    'user = "dev"\n'
    'password = "devpass"\n'
    'host = "localhost"\n'
    "port = 5432\n"
    "pool_size = 5\n"
)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _mode_bits(path: Path) -> int:
    """
    Return the permission bits (e.g., 0o644) for the given filesystem entry.
    """
    return stat.S_IMODE(path.stat().st_mode)


def _assert_permissions(path: Path, expected_mode: int):
    """
    Assert that the permission bits on *path* equal *expected_mode*.
    """
    actual = _mode_bits(path)
    assert (
        actual == expected_mode
    ), f"Expected permissions {oct(expected_mode)} on {path}, found {oct(actual)}."


# ---------------------------------------------------------------------------
# Test suite
# ---------------------------------------------------------------------------

def test_app_and_config_directories_exist():
    assert APP_DIR.is_dir(), f"Missing directory: {APP_DIR}"
    assert CONFIG_DIR.is_dir(), f"Missing directory: {CONFIG_DIR}"


@pytest.mark.parametrize(
    "file_path, expected_mode",
    [
        (SETTINGS_PATH, 0o644),
        (DATABASE_PATH, 0o644),
    ],
)
def test_config_files_exist_with_correct_permissions(file_path: Path, expected_mode: int):
    assert file_path.is_file(), f"Expected configuration file not found: {file_path}"
    _assert_permissions(file_path, expected_mode)


def test_settings_yaml_initial_content_exact():
    actual = SETTINGS_PATH.read_text(encoding="utf-8")
    assert (
        actual == EXPECTED_SETTINGS_CONTENT
    ), (
        f"{SETTINGS_PATH} content mismatch.\n"
        "It must exactly match the initial baseline (including newlines)."
    )


def test_database_toml_initial_content_exact():
    actual = DATABASE_PATH.read_text(encoding="utf-8")
    assert (
        actual == EXPECTED_DATABASE_CONTENT
    ), (
        f"{DATABASE_PATH} content mismatch.\n"
        "It must exactly match the initial baseline (including newlines)."
    )


def test_no_backup_directory_yet():
    assert (
        not BACKUP_DIR.exists()
    ), f"Backup directory {BACKUP_DIR} should NOT exist before deployment."


def test_no_logs_directory_yet():
    assert (
        not LOGS_DIR.exists()
    ), f"Logs directory {LOGS_DIR} should NOT exist before deployment."