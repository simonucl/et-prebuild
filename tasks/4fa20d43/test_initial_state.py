# Filename: test_initial_state.py
"""
Pytest suite that validates the initial filesystem state **before** the student
runs any commands for the “inventory service migration” exercise.

It asserts:
1. The directory /home/user/app/config exists.
2. The file /home/user/app/config/service.conf exists and has exactly the
   expected initial contents (including the single trailing newline).
3. No file named /home/user/app/config/migration.log is present yet.
"""

import os
from pathlib import Path

import pytest

CONFIG_DIR = Path("/home/user/app/config")
SERVICE_CONF = CONFIG_DIR / "service.conf"
MIGRATION_LOG = CONFIG_DIR / "migration.log"

EXPECTED_SERVICE_CONF_CONTENT = (
    "# Service configuration\n"
    "service_name=inventory\n"
    "endpoint=old.cloud.internal\n"
    "port=8080\n"
)


def test_config_directory_exists():
    """The configuration directory must exist and be a directory."""
    assert CONFIG_DIR.exists(), f"Directory {CONFIG_DIR} is missing."
    assert CONFIG_DIR.is_dir(), f"{CONFIG_DIR} exists but is not a directory."


def test_service_conf_exists_with_expected_content():
    """service.conf must exist and match the expected initial contents exactly."""
    assert SERVICE_CONF.exists(), f"Required file {SERVICE_CONF} is missing."
    assert SERVICE_CONF.is_file(), f"{SERVICE_CONF} exists but is not a regular file."

    content = SERVICE_CONF.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_SERVICE_CONF_CONTENT
    ), (
        f"{SERVICE_CONF} contents are not what the exercise expects.\n\n"
        "Expected:\n"
        f"{EXPECTED_SERVICE_CONF_CONTENT!r}\n\n"
        "Found:\n"
        f"{content!r}"
    )


def test_migration_log_does_not_yet_exist():
    """migration.log must not exist before the migration command is executed."""
    assert not MIGRATION_LOG.exists(), (
        f"{MIGRATION_LOG} should not exist yet. "
        "The student must create it with their one-line command."
    )