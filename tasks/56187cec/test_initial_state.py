# test_initial_state.py
#
# This test-suite validates that the OS / filesystem is in the
# REQUIRED **INITIAL** state _before_ the student toggles the
# application into maintenance mode.
#
# It checks that:
#   • /home/user/project/      exists and is a directory.
#   • /home/user/project/config.yaml       exists with the original “maintenance: false”.
#   • /home/user/project/settings.toml     exists with the original “maintenance = false”.
#   • /home/user/project/maintenance_change.log does NOT yet exist.
#
# Only stdlib + pytest are used.

import os
import textwrap
import pytest
from pathlib import Path

PROJECT_DIR = Path("/home/user/project")
CONFIG_YAML = PROJECT_DIR / "config.yaml"
SETTINGS_TOML = PROJECT_DIR / "settings.toml"
MAINT_LOG = PROJECT_DIR / "maintenance_change.log"


@pytest.fixture(scope="module")
def yaml_expected_lines():
    # Keep the exact indentation, spacing and quoting from the
    # specification (trailing LF deliberately omitted here).
    expected = textwrap.dedent(
        """\
        server:
          host: "0.0.0.0"
          port: 8080
        feature_flags:
          maintenance: false
          beta: true
        """
    )
    return expected.splitlines(keepends=False)


@pytest.fixture(scope="module")
def toml_expected_lines():
    expected = textwrap.dedent(
        """\
        [database]
        host = "localhost"
        port = 5432
        user = "webapp"
        maintenance = false
        """
    )
    return expected.splitlines(keepends=False)


def assert_no_crlf(path: Path, content: str) -> None:
    """
    Ensure the file uses UNIX line endings only.
    """
    assert "\r" not in content, (
        f"{path} must use UNIX (LF) line endings only — found CRLF characters."
    )


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), (
        f"Expected directory {PROJECT_DIR} does not exist.  "
        "The project directory must be present before any changes are made."
    )


def test_config_yaml_initial_state(yaml_expected_lines):
    assert CONFIG_YAML.is_file(), (
        f"{CONFIG_YAML} is missing.  "
        "The YAML configuration file must exist before maintenance mode is enabled."
    )

    raw = CONFIG_YAML.read_text(encoding="utf-8")
    assert_no_crlf(CONFIG_YAML, raw)

    actual_lines = raw.splitlines(keepends=False)
    assert actual_lines == yaml_expected_lines, (
        f"{CONFIG_YAML} does not match the required INITIAL contents.\n"
        "If you have already modified the file, restore it to its original state before proceeding.\n\n"
        "Expected:\n"
        + "\n".join(repr(l) for l in yaml_expected_lines)
        + "\n\nFound:\n"
        + "\n".join(repr(l) for l in actual_lines)
    )


def test_settings_toml_initial_state(toml_expected_lines):
    assert SETTINGS_TOML.is_file(), (
        f"{SETTINGS_TOML} is missing.  "
        "The TOML configuration file must exist before maintenance mode is enabled."
    )

    raw = SETTINGS_TOML.read_text(encoding="utf-8")
    assert_no_crlf(SETTINGS_TOML, raw)

    actual_lines = raw.splitlines(keepends=False)
    assert actual_lines == toml_expected_lines, (
        f"{SETTINGS_TOML} does not match the required INITIAL contents.\n"
        "If you have already modified the file, restore it to its original state before proceeding.\n\n"
        "Expected:\n"
        + "\n".join(repr(l) for l in toml_expected_lines)
        + "\n\nFound:\n"
        + "\n".join(repr(l) for l in actual_lines)
    )


def test_maintenance_log_does_not_exist_yet():
    assert not MAINT_LOG.exists(), (
        f"{MAINT_LOG} should NOT exist yet.  "
        "Create this file only after both configuration files have been updated."
    )