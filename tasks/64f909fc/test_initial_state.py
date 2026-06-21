# test_initial_state.py
#
# This pytest suite verifies the *initial* on-disk state of the backup
# configuration before the student performs any edits.  The tests are
# intentionally strict, because later grading logic assumes this exact
# starting point.

import difflib
from pathlib import Path

import pytest

BACKUP_DIR = Path("/home/user/db_backup")
CONFIG_YAML = BACKUP_DIR / "config.yaml"
RETENTION_TOML = BACKUP_DIR / "retention.toml"
CHANGELOG = BACKUP_DIR / "changes.log"


def _assert_text_equals(actual: str, expected: str, file_description: str) -> None:
    """
    Helper that compares two multi-line strings and raises an assertion
    with a unified diff if they differ.
    """
    if actual != expected:
        diff = "\n".join(
            difflib.unified_diff(
                expected.splitlines(),
                actual.splitlines(),
                fromfile="expected",
                tofile="actual",
                lineterm="",
            )
        )
        pytest.fail(
            f"{file_description} contents do not match the expected initial state:\n{diff}"
        )


def test_backup_directory_exists():
    assert BACKUP_DIR.exists(), f"Required directory {BACKUP_DIR} is missing."
    assert BACKUP_DIR.is_dir(), f"{BACKUP_DIR} exists but is not a directory."


def test_config_yaml_initial_content():
    assert CONFIG_YAML.exists(), f"Missing required file: {CONFIG_YAML}"

    expected = (
        'database:\n'
        '  host: "localhost"\n'
        '  port: 5432\n'
        '  name: "maindb"\n'
        'backup:\n'
        '  enabled: false\n'
        '  schedule: "not_set"\n'
        '  compression: "none"\n'
    )

    actual = CONFIG_YAML.read_text()
    _assert_text_equals(actual, expected, str(CONFIG_YAML))


def test_retention_toml_initial_content():
    assert RETENTION_TOML.exists(), f"Missing required file: {RETENTION_TOML}"

    expected = (
        "[retention]\n"
        "max_backups = 0\n"
        "keep_days   = 0\n"
        "cold_storage = true\n"
    )

    actual = RETENTION_TOML.read_text()
    _assert_text_equals(actual, expected, str(RETENTION_TOML))


def test_changes_log_absent():
    assert not CHANGELOG.exists(), (
        f"{CHANGELOG} should NOT exist at the beginning of the exercise. "
        "It must be created only after the required edits are performed."
    )