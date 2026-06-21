# test_initial_state.py
#
# This pytest suite validates that the filesystem is in the EXPECTED
# *initial* state – i.e. before the student has applied any of the
# required edits for the “widget-service” release task.
#
# The tests purposely **fail** if they detect any of the “after”
# conditions (e.g. bumped versions, added environment variable,
# new log file, etc.).  Clear assert-messages explain what is wrong
# so the student knows exactly what is missing or what was
# accidentally changed ahead of time.

import os
import pathlib
import re

import pytest

# ---------------------------------------------------------------------------
# Helper constants
# ---------------------------------------------------------------------------
HOME = pathlib.Path("/home/user")
PROJECT_ROOT = HOME / "projects" / "widget-service"
CONFIG_DIR = PROJECT_ROOT / "config"
DEPLOYMENTS_DIR = CONFIG_DIR / "deployments"
PROD_YAML = DEPLOYMENTS_DIR / "prod.yaml"
SETTINGS_TOML = CONFIG_DIR / "settings.toml"
DEPLOYMENT_LOGS_DIR = PROJECT_ROOT / "deployment_logs"
DEPLOYMENT_LOG = DEPLOYMENT_LOGS_DIR / "2024-05-02_update.log"


# ---------------------------------------------------------------------------
# Sanity checks on directory structure
# ---------------------------------------------------------------------------
@pytest.mark.initial_state
def test_project_directory_exists():
    assert PROJECT_ROOT.is_dir(), (
        f"Expected project directory {PROJECT_ROOT} to exist in the initial "
        "state, but it is missing."
    )


@pytest.mark.initial_state
def test_config_structure_exists():
    missing = [str(p) for p in (CONFIG_DIR, DEPLOYMENTS_DIR) if not p.is_dir()]
    assert not missing, f"Missing configuration directories: {', '.join(missing)}"


# ---------------------------------------------------------------------------
# prod.yaml must be in its original 1.4.2 state
# ---------------------------------------------------------------------------
@pytest.mark.initial_state
def test_prod_yaml_initial_state():
    assert PROD_YAML.is_file(), f"File {PROD_YAML} should exist before any edits."

    text = PROD_YAML.read_text()

    # 1.4.2 tag MUST be present
    assert "registry.example.com/widget-service:1.4.2" in text, (
        "Initial prod.yaml should reference image tag 1.4.2, but it does not."
    )

    # 1.5.0 tag MUST NOT be present yet
    assert "registry.example.com/widget-service:1.5.0" not in text, (
        "prod.yaml already contains the 1.5.0 tag; this should only appear "
        "AFTER the student performs the task."
    )

    # RELEASE_TAG env var must NOT be present yet
    assert "RELEASE_TAG" not in text, (
        "prod.yaml already contains RELEASE_TAG env var; it should not appear "
        "until after the task is completed."
    )


# ---------------------------------------------------------------------------
# settings.toml must be in its original 1.4.2 / info state
# ---------------------------------------------------------------------------
@pytest.mark.initial_state
def test_settings_toml_initial_state():
    assert SETTINGS_TOML.is_file(), f"File {SETTINGS_TOML} should exist before any edits."

    text = SETTINGS_TOML.read_text()

    # Version 1.4.2 must exist, 1.5.0 must not
    assert re.search(r'version\s*=\s*"1\.4\.2"', text), (
        "settings.toml should contain version = \"1.4.2\" in the initial state."
    )
    assert "version = \"1.5.0\"" not in text, (
        "settings.toml already contains version 1.5.0; this should only appear "
        "AFTER the student performs the task."
    )

    # logging.level should still be "info", NOT "debug"
    assert re.search(r'level\s*=\s*"info"', text), (
        "settings.toml should have logging.level = \"info\" in the initial state."
    )
    assert 'level = "debug"' not in text, (
        "settings.toml already contains logging.level = \"debug\"; "
        "this should only appear AFTER the task is completed."
    )

    # No [feature_flags] table yet
    assert "[feature_flags]" not in text, (
        "settings.toml already has a [feature_flags] table; "
        "it should only be added AFTER the student completes the task."
    )


# ---------------------------------------------------------------------------
# Deployment log file must NOT exist yet
# ---------------------------------------------------------------------------
@pytest.mark.initial_state
def test_deployment_log_not_present():
    # The directory may or may not exist initially; if it does, log file must not.
    if DEPLOYMENT_LOGS_DIR.exists():
        assert DEPLOYMENT_LOGS_DIR.is_dir(), (
            f"{DEPLOYMENT_LOGS_DIR} exists but is not a directory."
        )
        assert not DEPLOYMENT_LOG.exists(), (
            f"Log file {DEPLOYMENT_LOG} is already present; "
            "it should only be created AFTER the student performs the task."
        )
    else:
        # Directory not present is acceptable in the initial state
        assert not DEPLOYMENT_LOG.exists(), (
            "Deployment log file should not exist before the task is completed."
        )