# test_initial_state.py
#
# Pytest suite verifying the **initial** state of the filesystem before the
# student edits the backup-configuration files.  These tests make sure that
# the starting conditions are correct: the two configuration files already
# exist (but are still *incorrect*) and the log file has **not** yet been
# created.

import os
import pytest

HOME = "/home/user"
BASE_DIR = os.path.join(HOME, "db_backup")

CONFIG_YAML_PATH = os.path.join(BASE_DIR, "config.yaml")
SETTINGS_TOML_PATH = os.path.join(BASE_DIR, "settings.toml")
LOG_PATH = os.path.join(BASE_DIR, "operation_summary.log")

# --------------------------------------------------------------------------- #
# Canonical “finished” contents.  In the *initial* state the files must
# NOT yet match these strings verbatim.
# --------------------------------------------------------------------------- #

EXPECTED_CONFIG_YAML = (
    'version: "2.1"\n'
    "retention_days: 30\n"
    'compression: "lz4"\n'
    'backup_type: "incremental"\n'
    "schedules:\n"
    '  nightly: "02:00"\n'
    '  weekly: "Sunday 03:00"\n'
    'encryption: "aes256"\n'
)

EXPECTED_SETTINGS_TOML = (
    "# Application-level settings\n"
    "[app]\n"
    'name = "pg-backup-agent"\n'
    'version = "1.3.0"\n'
    "\n"
    "# Storage backend\n"
    "[storage]\n"
    'provider = "s3"\n'
    'region   = "us-west-2"\n'
    'bucket   = "prod-backups"\n'
    "\n"
    "# Databases being backed up\n"
    "[[databases]]\n"
    'name     = "production"\n'
    'host     = "prod.db.internal"\n'
    "port     = 5432\n"
    "\n"
    "[[databases]]\n"
    'name     = "analytics"\n'
    'host     = "analytics.db.internal"\n'
    "port     = 5432\n"
)


# --------------------------------------------------------------------------- #
# Helper
# --------------------------------------------------------------------------- #
def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fp:
        return fp.read()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_db_backup_directory_exists():
    """
    The /home/user/db_backup directory must already exist so the student can
    work inside it.
    """
    assert os.path.isdir(
        BASE_DIR
    ), f"Expected directory {BASE_DIR} to exist before the task begins."


def test_config_yaml_exists_and_needs_update():
    """
    config.yaml should already exist but MUST NOT yet contain the final
    expected content.  The student will fix it.
    """
    assert os.path.isfile(
        CONFIG_YAML_PATH
    ), "config.yaml is missing. It should be present before edits."

    current_content = _read_file(CONFIG_YAML_PATH)
    assert (
        current_content != EXPECTED_CONFIG_YAML
    ), "config.yaml already matches the final required content—nothing left for the student to do."


def test_settings_toml_exists_and_needs_update():
    """
    settings.toml should already exist but MUST NOT yet contain the final
    expected content.  The student will fix it.
    """
    assert os.path.isfile(
        SETTINGS_TOML_PATH
    ), "settings.toml is missing. It should be present before edits."

    current_content = _read_file(SETTINGS_TOML_PATH)
    assert (
        current_content != EXPECTED_SETTINGS_TOML
    ), "settings.toml already matches the final required content—nothing left for the student to do."


def test_operation_summary_log_not_present():
    """
    The log file must NOT exist yet; the student will create it after updating
    the configs.
    """
    assert not os.path.exists(
        LOG_PATH
    ), "operation_summary.log already exists but should be created only after the configs are updated."