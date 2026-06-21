# test_initial_state.py
#
# This test-suite validates the **initial** state of the operating system
# before the student applies any compliance fixes.
#
# It asserts that:
# * The two configuration files exist and still contain their original,
#   non-compliant values.
# * No compliance audit log has yet been created.
#
# If any of these assertions fail, the workstation is **not** in the expected
# starting state and the student must not proceed until the issues are fixed.

import os
from pathlib import Path
import pytest


HOME = Path("/home/user")
CONFIG_DIR = HOME / "configs"
AUDIT_DIR = HOME / "audit_logs"
YAML_PATH = CONFIG_DIR / "app_config.yml"
TOML_PATH = CONFIG_DIR / "app_settings.toml"
AUDIT_LOG_PATH = AUDIT_DIR / "compliance_audit.log"


@pytest.fixture(scope="module")
def yaml_contents():
    """Return the raw text of app_config.yml (raises if file missing)."""
    if not YAML_PATH.is_file():
        pytest.fail(
            f"Required file {YAML_PATH} is missing. "
            "Create it with the initial, non-compliant contents before proceeding."
        )
    return YAML_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def toml_contents():
    """Return the raw text of app_settings.toml (raises if file missing)."""
    if not TOML_PATH.is_file():
        pytest.fail(
            f"Required file {TOML_PATH} is missing. "
            "Create it with the initial, non-compliant contents before proceeding."
        )
    return TOML_PATH.read_text(encoding="utf-8")


def test_config_files_exist():
    """Both configuration files must exist as regular files."""
    for path in (YAML_PATH, TOML_PATH):
        assert path.is_file(), f"Expected file {path} to exist."


def test_app_config_initial_contents(yaml_contents):
    """
    The YAML file must still contain the non-compliant value:
        logging.level: info
    and must NOT already have been changed to 'warn'.
    """
    assert "level: info" in yaml_contents, (
        f"{YAML_PATH} should contain 'level: info' under the logging section "
        "in the initial state."
    )
    assert "level: warn" not in yaml_contents, (
        f"{YAML_PATH} already contains 'level: warn'; "
        "the file appears to have been modified before the audit started."
    )


def test_app_settings_initial_contents(toml_contents):
    """
    The TOML file must still contain the non-compliant value:
        enable_beta = false
    and must NOT already have been changed to true.
    """
    # Normalise whitespace for robust matching
    condensed = " ".join(toml_contents.split())
    assert "enable_beta = false" in condensed, (
        f"{TOML_PATH} should contain 'enable_beta = false' in the initial state."
    )
    assert "enable_beta = true" not in condensed, (
        f"{TOML_PATH} already contains 'enable_beta = true'; "
        "the file appears to have been modified before the audit started."
    )


def test_audit_log_absent():
    """
    No audit log should exist before the student runs the compliance script.
    The directory may or may not exist, but the log file itself must not.
    """
    assert not AUDIT_LOG_PATH.exists(), (
        f"{AUDIT_LOG_PATH} already exists. The compliance audit log "
        "must be created only after changes are applied."
    )