# test_initial_state.py
#
# This test-suite verifies the *initial* filesystem state **before**
# the student performs any actions.
#
# Expected initial state:
# 1. /home/user/app/config/settings.yaml exists with the exact
#    contents shown in the task description (port 8080).
# 2. /home/user/app/config/changes.log exists and is completely empty.
#
# Any deviation will fail with a clear, explanatory message.

import os
from pathlib import Path

import pytest

# Absolute paths used throughout the tests
SETTINGS_YAML = Path("/home/user/app/config/settings.yaml")
CHANGES_LOG   = Path("/home/user/app/config/changes.log")


@pytest.fixture(scope="session")
def expected_settings_content() -> str:
    """
    The exact YAML content that must be present *before* any modification.
    A trailing newline is expected because text editors typically end files
    with a newline.
    """
    return (
        "---\n"
        "server:\n"
        "  host: \"0.0.0.0\"\n"
        "  port: 8080\n"
        "debug: false\n"
        "---\n"
    )


def test_settings_yaml_exists(expected_settings_content):
    """Ensure settings.yaml exists and has the expected content (port 8080)."""
    assert SETTINGS_YAML.is_file(), (
        f"Missing file: {SETTINGS_YAML}. It must exist before any edits."
    )

    actual = SETTINGS_YAML.read_text(encoding="utf-8")
    assert actual == expected_settings_content, (
        f"{SETTINGS_YAML} contents are not as expected.\n"
        "The file should be *exactly*:\n"
        f"{expected_settings_content!r}\n"
        "but the actual content is:\n"
        f"{actual!r}"
    )


def test_changes_log_exists_and_empty():
    """Ensure changes.log exists and is empty before any actions."""
    assert CHANGES_LOG.is_file(), (
        f"Missing file: {CHANGES_LOG}. An empty file must pre-exist."
    )

    size = CHANGES_LOG.stat().st_size
    assert size == 0, (
        f"{CHANGES_LOG} should be empty initially, "
        f"but it is {size} bytes long."
    )