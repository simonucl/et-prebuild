# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the expected *initial* state before the student performs any
# action.  All paths are absolute and referenced exactly as specified
# in the task description.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
CONFIG_DIR = HOME / "app" / "config"
LOGS_DIR = HOME / "logs"

YAML_FILE = CONFIG_DIR / "service.yaml"
TOML_FILE = CONFIG_DIR / "service.toml"
INCIDENT_LOG = LOGS_DIR / "incident_maintenance_toggle.log"

###############################################################################
# Helper utilities
###############################################################################


def _read_text(path: Path) -> str:
    """Read the entire file as text, returning an empty string if it cannot
    be read for any reason.  Tests will explicitly check for existence first.
    """
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


###############################################################################
# Tests for the YAML configuration file
###############################################################################


def test_yaml_file_exists():
    """Verify service.yaml exists in the expected absolute location."""
    assert YAML_FILE.is_file(), (
        f"Missing YAML configuration file: {YAML_FILE}. "
        "It must exist before any modification is attempted."
    )


def test_yaml_initial_contents():
    """Ensure maintenance_mode is FALSE and not TRUE in the YAML file."""
    contents = _read_text(YAML_FILE)
    assert (
        "maintenance_mode: false" in contents
    ), "The YAML file must start with maintenance_mode set to false."
    assert (
        "maintenance_mode: true" not in contents
    ), "The YAML file already contains 'maintenance_mode: true'—should be false initially."


###############################################################################
# Tests for the TOML configuration file
###############################################################################


def test_toml_file_exists():
    """Verify service.toml exists in the expected absolute location."""
    assert TOML_FILE.is_file(), (
        f"Missing TOML configuration file: {TOML_FILE}. "
        "It must exist before any modification is attempted."
    )


def test_toml_initial_contents():
    """Ensure maintenance_mode is FALSE and not TRUE in the TOML file."""
    contents = _read_text(TOML_FILE)
    assert (
        "maintenance_mode = false" in contents
    ), "The TOML file must start with maintenance_mode set to false."
    assert (
        "maintenance_mode = true" not in contents
    ), "The TOML file already contains 'maintenance_mode = true'—should be false initially."


###############################################################################
# Tests for the logs directory and incident log file
###############################################################################


def test_logs_directory_exists_and_writable():
    """Verify the /home/user/logs directory exists and is writable."""
    assert LOGS_DIR.is_dir(), f"Logs directory is missing: {LOGS_DIR}"
    assert os.access(LOGS_DIR, os.W_OK), (
        f"Logs directory {LOGS_DIR} is not writable by the current user."
    )


def test_incident_log_absent():
    """The incident_maintenance_toggle.log must NOT exist before the task."""
    assert not INCIDENT_LOG.exists(), (
        f"Log file {INCIDENT_LOG} should not exist at the start of the task."
    )