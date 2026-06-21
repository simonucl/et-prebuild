# test_initial_state.py
#
# This test-suite validates the **initial** filesystem state _before_ the
# student performs any actions for the “database-reliability engineer” task.
#
# It asserts that:
#   1. Both expected configuration files exist with the original, unmodified
#      contents.
#   2. No new log file has been created yet.
#
# NOTE:
#   • Only the standard library and pytest are used.
#   • All failure messages precisely describe what is missing or incorrect so
#     that the student knows what to fix *before* starting the task.
#   • We compare raw text because external YAML/TOML parsers are not part of
#     the Python standard library.

from pathlib import Path
import pytest
import re

HOME = Path("/home/user")
DB_DIR = HOME / "db_backup"
YAML_PATH = DB_DIR / "backup_config.yaml"
TOML_PATH = DB_DIR / "storage.conf.toml"
LOG_PATH = DB_DIR / "config_update.log"


@pytest.fixture(scope="module")
def yaml_text():
    """Return the raw text of backup_config.yaml or fail early if file missing."""
    if not YAML_PATH.exists():
        pytest.fail(f"Required file {YAML_PATH} is missing.")
    if not YAML_PATH.is_file():
        pytest.fail(f"{YAML_PATH} exists but is not a regular file.")
    return YAML_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def toml_text():
    """Return the raw text of storage.conf.toml or fail early if file missing."""
    if not TOML_PATH.exists():
        pytest.fail(f"Required file {TOML_PATH} is missing.")
    if not TOML_PATH.is_file():
        pytest.fail(f"{TOML_PATH} exists but is not a regular file.")
    return TOML_PATH.read_text(encoding="utf-8")


def test_directory_structure():
    """Ensure /home/user/db_backup directory exists as a directory."""
    assert DB_DIR.exists(), f"Directory {DB_DIR} is missing."
    assert DB_DIR.is_dir(), f"{DB_DIR} exists but is not a directory."


def test_backup_config_yaml_has_original_contents(yaml_text):
    """Verify that backup_config.yaml is still in its original, unedited state."""
    expected_lines = [
        "schedule:",
        "  frequency: daily",
        '  window: "00:00-06:00"',
        "  compression: false",
        "database:",
        "  host: localhost",
        "  port: 5432",
    ]

    for line in expected_lines:
        assert line in yaml_text.splitlines(), (
            f"{YAML_PATH} is missing the expected line: {line!r}"
        )

    # Ensure the file has NOT already been modified to 'hourly' or compression true.
    assert "frequency: hourly" not in yaml_text, (
        f"{YAML_PATH} already contains 'frequency: hourly'; "
        "this should only appear **after** the student edits the file."
    )
    hourly_pattern = re.compile(r"compression:\s*true\b")
    assert not hourly_pattern.search(yaml_text), (
        f"{YAML_PATH} already sets compression to true; "
        "initial state must have 'compression: false'."
    )


def test_storage_conf_toml_has_original_contents(toml_text):
    """Verify that storage.conf.toml is still untouched."""
    expected_entries = {
        'storage_mode = "s3"',
        'bucket = "prod-backups"',
        "retention_days = 7",
        "[network]",
        "timeout_secs = 30",
    }

    for entry in expected_entries:
        assert entry in toml_text.splitlines(), (
            f"{TOML_PATH} is missing expected entry: {entry!r}"
        )

    # Ensure retention_days not already modified.
    assert "retention_days = 30" not in toml_text, (
        f"{TOML_PATH} already sets retention_days to 30; "
        "initial state must have 'retention_days = 7'."
    )

    # Ensure no [encryption] table yet.
    assert "[encryption]" not in toml_text, (
        f"{TOML_PATH} already contains an [encryption] table; "
        "this should be added by the student."
    )


def test_log_file_does_not_exist_yet():
    """The update log must not exist before the task begins."""
    assert not LOG_PATH.exists(), (
        f"{LOG_PATH} should NOT exist yet. "
        "It must be created by the student after modifying the configs."
    )