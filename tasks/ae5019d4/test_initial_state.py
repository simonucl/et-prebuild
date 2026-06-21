# test_initial_state.py
#
# This pytest suite validates the ORIGINAL state of the filesystem *before* the
# student performs any edits.  It asserts that the two configuration files are
# present with their initial contents and that the change-log file does NOT yet
# exist.  All paths are absolute and rooted at /home/user.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
PROJECT_ROOT = HOME / "projects" / "observability"
GRAFANA_DIR = PROJECT_ROOT / "grafana"

DASHBOARD_YAML = GRAFANA_DIR / "dashboard.yaml"
ALERTING_TOML = PROJECT_ROOT / "alerting.toml"
UPDATE_LOG    = PROJECT_ROOT / "update_log.txt"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _read_text(path: Path) -> str:
    """
    Read a text file as UTF-8.  If the file is missing, pytest will fail with a
    helpful message.
    """
    assert path.exists(), f"Expected file {path} does NOT exist."
    assert path.is_file(), f"Expected {path} to be a regular file."
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# Expected ORIGINAL contents
# --------------------------------------------------------------------------- #
EXPECTED_DASHBOARD_ORIGINAL = "\n".join(
    [
        'title: "Service Overview"',
        "panels:",
        "  - id: 1",
        '    title: "CPU Usage"',
        '    datasource: "Prometheus"',
        "    targets:",
        '      - expr: "rate(node_cpu_seconds_total[5m])"',
    ]
)

EXPECTED_ALERTING_ORIGINAL = "\n".join(
    [
        "[alerting]",
        "enabled = false",
    ]
)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_dashboard_yaml_original_state():
    """
    The dashboard YAML should exist and match the *original* 7-line definition
    provided to the learner.  Indentation and spacing must be exact.
    """
    actual = _read_text(DASHBOARD_YAML).rstrip("\n")
    expected = EXPECTED_DASHBOARD_ORIGINAL
    assert (
        actual == expected
    ), (
        "dashboard.yaml does not match the expected ORIGINAL contents.\n\n"
        "----- EXPECTED -----\n"
        f"{expected}\n"
        "--------------------\n"
        "----- ACTUAL -------\n"
        f"{actual}\n"
        "--------------------"
    )


def test_alerting_toml_original_state():
    """
    The alerting TOML should exist with `enabled = false` before any edits are
    made by the student.
    """
    actual = _read_text(ALERTING_TOML).rstrip("\n")
    expected = EXPECTED_ALERTING_ORIGINAL
    assert (
        actual == expected
    ), (
        "alerting.toml does not match the expected ORIGINAL contents.\n\n"
        "----- EXPECTED -----\n"
        f"{expected}\n"
        "--------------------\n"
        "----- ACTUAL -------\n"
        f"{actual}\n"
        "--------------------"
    )


def test_update_log_does_not_exist_yet():
    """
    The update_log.txt file should NOT exist before the student performs any
    changes.
    """
    assert not UPDATE_LOG.exists(), (
        f"{UPDATE_LOG} is present, but it should NOT exist before the task is "
        "completed."
    )