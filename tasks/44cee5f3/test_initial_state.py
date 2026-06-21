# test_initial_state.py
#
# Pytest suite to validate the *initial* state of the operating-system /
# file-system **before** the student performs any action.
#
# The tests assert that:
#   1. The two original configuration files exist **and** contain exactly the
#      expected _initial_ content (no “staging” environment yet).
#   2. No backup files have been created (names matching *.bak_YYYYMMDD_HHMMSS).
#   3. No audit log file exists (or, if it does, it is completely empty).
#
# If any of these assertions fail, the accompanying error message will tell the
# student precisely what is missing or unexpectedly present.
#
# Only Python’s stdlib plus pytest are used, in accordance with the rules.

import os
import glob
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Helper constants                                                            #
# --------------------------------------------------------------------------- #

HOME               = Path("/home/user")
PROJECT_ROOT       = HOME / "projects" / "app"
CONFIG_DIR         = PROJECT_ROOT / "config"

DEFAULT_YAML_PATH  = CONFIG_DIR / "default.yaml"
SETTINGS_TOML_PATH = CONFIG_DIR / "settings.toml"
AUDIT_LOG_PATH     = HOME / "config_update.log"

# Exact **initial** contents of the files, stripped of any trailing newline so
# the comparison can tolerate the presence or absence of a final '\n' in the
# actual file on disk.
EXPECTED_DEFAULT_YAML = """
app:
  name: SampleApp
  environments:
    development:
      host: localhost
      debug: true
      version: 1.4
""".lstrip("\n").rstrip("\n")

EXPECTED_SETTINGS_TOML = """
[app]
name = "SampleApp"

[app.environments.development]
host = "localhost"
debug = true
version = "1.4"
""".lstrip("\n").rstrip("\n")

# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def _read_strip(path: Path) -> str:
    """Read file content and strip a single trailing newline for comparison."""
    with path.open("r", encoding="utf-8") as fh:
        data = fh.read()
    return data.rstrip("\n")


def test_configuration_files_exist():
    """Both configuration files must already exist."""
    assert DEFAULT_YAML_PATH.is_file(), f"Missing file: {DEFAULT_YAML_PATH}"
    assert SETTINGS_TOML_PATH.is_file(), f"Missing file: {SETTINGS_TOML_PATH}"


def test_default_yaml_initial_content():
    """default.yaml should contain ONLY the development environment (no staging)."""
    actual = _read_strip(DEFAULT_YAML_PATH)
    assert actual == EXPECTED_DEFAULT_YAML, (
        "The content of default.yaml does not match the expected INITIAL state.\n"
        "If you have already inserted the 'staging' environment or altered "
        "indentation/values, remove those changes before running the task."
    )
    assert "staging:" not in actual, (
        "Found the word 'staging' in default.yaml, but the file should contain "
        "ONLY the development environment at this stage."
    )


def test_settings_toml_initial_content():
    """settings.toml should contain ONLY the development table (no staging)."""
    actual = _read_strip(SETTINGS_TOML_PATH)
    assert actual == EXPECTED_SETTINGS_TOML, (
        "The content of settings.toml does not match the expected INITIAL state.\n"
        "If you have already inserted the '[app.environments.staging]' table or "
        "changed any values, undo those changes before proceeding."
    )
    assert "[app.environments.staging]" not in actual, (
        "Found the '[app.environments.staging]' table in settings.toml, but the "
        "file should contain ONLY the development configuration at this stage."
    )


def test_no_backup_files_exist_yet():
    """
    There must be NO backup files in the config directory before the student
    starts the task. We look for any filename that matches '*.bak_YYYYMMDD_HHMMSS'.
    """
    pattern = str(CONFIG_DIR / "*.bak_*")
    backups = glob.glob(pattern)
    assert not backups, (
        "Detected backup file(s) *before* any action should have been taken:\n"
        f"  {backups}\n"
        "Please start from a clean state with NO backups present."
    )


def test_no_audit_log_yet():
    """
    The audit log should not exist yet (or must be completely empty if it does).
    """
    if AUDIT_LOG_PATH.exists():
        size = AUDIT_LOG_PATH.stat().st_size
        assert size == 0, (
            f"{AUDIT_LOG_PATH} already exists and is not empty (size={size} bytes). "
            "Start the task with no audit log, or an empty file at most."
        )