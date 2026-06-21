# test_initial_state.py
"""
Pytest suite to validate the initial filesystem state *before* the student
performs any action.

The checks performed here assert that the security configuration directory
and its two configuration files exist in their expected, pristine form, and
that no rotation log is present yet.

If any of the assertions fail, the accompanying error message will tell the
student exactly what is missing or unexpected.
"""

from pathlib import Path
import pytest

# Base directory and file paths
BASE_DIR = Path("/home/user/security")
CONFIG_YAML = BASE_DIR / "config.yaml"
SETTINGS_TOML = BASE_DIR / "settings.toml"
ROTATION_LOG = BASE_DIR / "rotation.log"


@pytest.fixture(scope="module")
def expected_yaml_content():
    # Exact content the YAML file must contain (no surrounding blank lines)
    return (
        "api:\n"
        "  token: oldtoken123\n"
        "  url: https://internal.example.com/api\n"
    )


@pytest.fixture(scope="module")
def expected_toml_content():
    # Exact content the TOML file must contain (no surrounding blank lines)
    return (
        "[api]\n"
        'token = "oldtoken123"\n'
        'url   = "https://internal.example.com/api"\n'
    )


def test_security_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Expected directory {BASE_DIR} to exist, "
        "but it is missing."
    )


def test_config_yaml_exists_and_content(expected_yaml_content):
    assert CONFIG_YAML.is_file(), (
        f"Expected file {CONFIG_YAML} to exist, "
        "but it is missing."
    )
    actual = CONFIG_YAML.read_text()
    assert actual == expected_yaml_content, (
        f"Content of {CONFIG_YAML} is not as expected.\n"
        "---- Expected ----\n"
        f"{expected_yaml_content}"
        "---- Actual ----\n"
        f"{actual}"
    )


def test_settings_toml_exists_and_content(expected_toml_content):
    assert SETTINGS_TOML.is_file(), (
        f"Expected file {SETTINGS_TOML} to exist, "
        "but it is missing."
    )
    actual = SETTINGS_TOML.read_text()
    assert actual == expected_toml_content, (
        f"Content of {SETTINGS_TOML} is not as expected.\n"
        "---- Expected ----\n"
        f"{expected_toml_content}"
        "---- Actual ----\n"
        f"{actual}"
    )


def test_rotation_log_absent():
    assert not ROTATION_LOG.exists(), (
        f"{ROTATION_LOG} should NOT exist before rotation, "
        "but it is present."
    )