# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student performs any credential-rotation task.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
APP_DIR = HOME / "app"
CONFIG_DIR = APP_DIR / "config"

SETTINGS_YAML = CONFIG_DIR / "settings.yaml"
SECRETS_TOML = CONFIG_DIR / "secrets.toml"
ROTATION_LOG = APP_DIR / "rotation.log"


@pytest.fixture(scope="module")
def settings_content():
    """Return the text of settings.yaml, fail early if file missing."""
    if not SETTINGS_YAML.exists():
        pytest.fail(f"Missing configuration file: {SETTINGS_YAML}")
    if not SETTINGS_YAML.is_file():
        pytest.fail(f"Expected a file at {SETTINGS_YAML}, but something else exists.")
    return SETTINGS_YAML.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def secrets_content():
    """Return the text of secrets.toml, fail early if file missing."""
    if not SECRETS_TOML.exists():
        pytest.fail(f"Missing secrets file: {SECRETS_TOML}")
    if not SECRETS_TOML.is_file():
        pytest.fail(f"Expected a file at {SECRETS_TOML}, but something else exists.")
    return SECRETS_TOML.read_text(encoding="utf-8")


def test_directories_exist():
    """Ensure /home/user/app/config hierarchy exists."""
    assert APP_DIR.exists(), f"Expected directory {APP_DIR} to exist."
    assert APP_DIR.is_dir(), f"{APP_DIR} exists but is not a directory."
    assert CONFIG_DIR.exists(), f"Expected directory {CONFIG_DIR} to exist."
    assert CONFIG_DIR.is_dir(), f"{CONFIG_DIR} exists but is not a directory."


def test_settings_yaml_contents(settings_content):
    """Validate that settings.yaml is in its original, un-rotated state."""
    expected = (
        "database:\n"
        "  host: db.prod.internal\n"
        "  username: admin\n"
        "  password: OldPassword123!\n"
    )
    assert settings_content == expected, (
        f"{SETTINGS_YAML} content is not in the expected *initial* state.\n"
        "If you have already rotated the credential, run these tests on the "
        "pristine starting environment."
    )
    # Ensure the file ends with a single trailing newline and nothing more.
    assert settings_content.endswith("\n"), "settings.yaml must end with a newline."
    assert not settings_content.endswith("\n\n"), (
        "settings.yaml has more than one trailing blank line."
    )


def test_secrets_toml_contents(secrets_content):
    """Validate that secrets.toml is in its original, un-rotated state."""
    expected = (
        "[api]\n"
        'token = "old_api_token_ABC123"\n'
        'expiry = "2024-12-31T23:59:59Z"\n'
    )
    assert secrets_content == expected, (
        f"{SECRETS_TOML} content is not in the expected *initial* state.\n"
        "If you have already rotated the credential, run these tests on the "
        "pristine starting environment."
    )
    # Ensure the file ends with a single trailing newline and nothing more.
    assert secrets_content.endswith("\n"), "secrets.toml must end with a newline."
    assert not secrets_content.endswith("\n\n"), (
        "secrets.toml has more than one trailing blank line."
    )


def test_rotation_log_absent():
    """rotation.log must not exist before the task is carried out."""
    assert not ROTATION_LOG.exists(), (
        f"{ROTATION_LOG} already exists. The rotation task has apparently "
        "been performed; these tests should run on the initial state."
    )