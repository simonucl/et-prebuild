# test_initial_state.py
#
# Pytest suite that verifies the INITIAL state of the operating-system
# before the student performs any actions for the “cloud-migration”
# exercise.  All checks must pass *before* the student starts working.

import os
import stat
from pathlib import Path

import pytest

# Canonical paths used in the exercise.
HOME_DIR = Path("/home/user")
LEGACY_DIR = HOME_DIR / "legacy_service"
CONFIG_FILE = LEGACY_DIR / "config.ini"
RELOAD_SENTINEL = LEGACY_DIR / ".reload"
MIGRATION_LOG = HOME_DIR / "migration.log"


def _read_file_lines(path: Path):
    """Return the file’s contents split into *raw* lines (retaining '\n')."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


@pytest.fixture(scope="module")
def config_lines():
    """Contents of config.ini split into lines (with newlines retained)."""
    return _read_file_lines(CONFIG_FILE)


def test_legacy_directory_exists_with_strict_permissions():
    """/home/user/legacy_service must exist and be 0700."""
    assert LEGACY_DIR.exists(), (
        "Directory /home/user/legacy_service is missing. "
        "It must exist BEFORE the migration begins."
    )
    assert LEGACY_DIR.is_dir(), (
        "/home/user/legacy_service exists but is not a directory."
    )

    mode = stat.S_IMODE(os.stat(LEGACY_DIR).st_mode)
    expected_mode = 0o700
    assert mode == expected_mode, (
        f"/home/user/legacy_service must have permissions 0700, "
        f"found {oct(mode)} instead."
    )


def test_config_ini_initial_contents(config_lines):
    """config.ini must contain exactly four specific lines before migration."""
    assert CONFIG_FILE.exists(), "/home/user/legacy_service/config.ini is missing."

    assert len(config_lines) == 4, (
        "config.ini should contain exactly four lines before migration:\n"
        "[server]\\nhost = 127.0.0.1\\nport = 5000\\n<blank line>"
    )

    # Strip trailing newlines for precise content comparison.
    stripped = [line.rstrip("\n") for line in config_lines]

    assert stripped[0] == "[server]", (
        "Line 1 of config.ini must be exactly '[server]' before migration."
    )
    assert stripped[1] == "host = 127.0.0.1", (
        "Line 2 of config.ini must be exactly 'host = 127.0.0.1' before migration."
    )
    assert stripped[2] == "port = 5000", (
        "Line 3 of config.ini must be exactly 'port = 5000' before migration."
    )
    assert stripped[3] == "", (
        "Line 4 of config.ini must be a blank line before migration."
    )


def test_reload_sentinel_does_not_exist_yet():
    """/home/user/legacy_service/.reload must *not* exist before migration."""
    assert not RELOAD_SENTINEL.exists(), (
        ".reload sentinel file already exists; it should be created only "
        "when the student triggers a configuration reload."
    )


def test_migration_log_exists_and_is_writable():
    """/home/user/migration.log must be present and writable."""
    assert MIGRATION_LOG.exists(), "/home/user/migration.log is missing."
    assert MIGRATION_LOG.is_file(), "/home/user/migration.log is not a regular file."
    assert os.access(MIGRATION_LOG, os.W_OK), (
        "/home/user/migration.log exists but is not writable by the student."
    )