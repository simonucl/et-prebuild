# test_initial_state.py
#
# This test-suite verifies the **initial** condition of the filesystem
# before the learner starts moving files / creating symlinks / writing logs.
#
# It purposefully FAILS if anything has already been migrated or if the
# expected legacy layout is missing or altered.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
OLD_CFG_DIR = HOME / "old_configs"
CLOUD_MIGRATION_DIR = HOME / "cloud_migration"
CLOUD_CFG_DIR = CLOUD_MIGRATION_DIR / "configs"
MIGRATION_LOGS_DIR = HOME / "migration_logs"
AUDIT_LOG = MIGRATION_LOGS_DIR / "symlink_audit.log"

# Expected legacy files and their exact contents (with trailing newlines)
EXPECTED_FILES = {
    "app.conf": "APP_ENV=production\n",
    "auth.conf": "AUTH_METHOD=oauth2\n",
    "cache.conf": "CACHE_SIZE=256\n",
    "db.conf": "DB_HOST=localhost\n",
}


def _read_text(path: Path) -> str:
    """
    Read text from *path* without universal-newline conversion so that the test
    can precisely match the trailing newline (or lack thereof).
    """
    with path.open("r", newline="") as fp:
        return fp.read()


def test_old_configs_directory_exists():
    assert OLD_CFG_DIR.exists(), (
        f"Directory {OLD_CFG_DIR} is expected to exist but is missing. "
        "Nothing can be migrated if the source directory is gone."
    )
    assert OLD_CFG_DIR.is_dir(), (
        f"{OLD_CFG_DIR} exists but is not a directory. "
        "It must be a directory containing the legacy *.conf files."
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_each_conf_file_present_with_correct_content(filename, expected_content):
    fp = OLD_CFG_DIR / filename
    assert fp.exists(), f"Missing expected file: {fp}"
    assert fp.is_file(), f"{fp} exists but is not a regular file."
    assert not fp.is_symlink(), f"{fp} should be a regular file, not a symlink."
    actual_content = _read_text(fp)
    assert actual_content == expected_content, (
        f"Content mismatch in {fp}.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Found:    {repr(actual_content)}"
    )


def test_no_extra_conf_files_in_old_configs():
    legacy_files = {p.name for p in OLD_CFG_DIR.glob("*.conf")}
    extras = legacy_files - EXPECTED_FILES.keys()
    assert not extras, (
        f"Unexpected *.conf files found in {OLD_CFG_DIR}: {sorted(extras)}. "
        "The initial state should contain only the predefined 4 files."
    )


def test_no_migration_directories_present_yet():
    assert not CLOUD_MIGRATION_DIR.exists(), (
        f"{CLOUD_MIGRATION_DIR} should NOT exist yet. "
        "Migration directories must be created by the learner."
    )
    assert not MIGRATION_LOGS_DIR.exists(), (
        f"{MIGRATION_LOGS_DIR} should NOT exist yet. "
        "Log directories must be created by the learner."
    )


def test_no_audit_log_present_yet():
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} already exists. "
        "The audit file must be generated during the migration, not before."
    )