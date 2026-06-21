# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem / OS state
# for the “monitoring-platform” assignment *before* the student
# carries out any work.
#
# What we assert:
#   1. Required input directory and files already exist.
#   2. Input files are valid JSON and have the expected structure.
#   3. The two output artefacts **do not** exist yet.
#
# Nothing else is checked so as not to over-specify the task.
#
# NOTE: Only stdlib + pytest are used.

import json
import os
from pathlib import Path

import pytest

MONITORING_DIR = Path("/home/user/monitoring")
SCHEMA_FILE = MONITORING_DIR / "alert-schema.json"
ALERTS_FILE = MONITORING_DIR / "alerts.json"

LOG_FILE = MONITORING_DIR / "alert_validation.log"
CRITICAL_FILE = MONITORING_DIR / "critical_alerts.json"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _load_json(path: Path):
    """Load and return JSON content from *path*."""
    try:
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as e:
        pytest.fail(f"File '{path}' is not valid JSON: {e}")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_monitoring_directory_exists():
    assert MONITORING_DIR.is_dir(), (
        f"Directory '{MONITORING_DIR}' is missing. "
        "The assignment specifies that all files reside inside it."
    )


def test_required_input_files_exist():
    missing = [p for p in (SCHEMA_FILE, ALERTS_FILE) if not p.is_file()]
    assert not missing, (
        "The following required input files are missing:\n"
        + "\n".join(str(p) for p in missing)
    )


def test_output_files_do_not_preexist():
    present = [p for p in (LOG_FILE, CRITICAL_FILE) if p.exists()]
    assert not present, (
        "The following output artefact(s) already exist but should *not* be "
        "present prior to the student's work:\n"
        + "\n".join(str(p) for p in present)
    )


def test_schema_file_is_valid_json_object():
    data = _load_json(SCHEMA_FILE)
    assert isinstance(
        data, dict
    ), f"Schema file '{SCHEMA_FILE}' must contain a JSON object."


def test_alerts_file_is_valid_json_array_with_expected_items():
    data = _load_json(ALERTS_FILE)

    assert isinstance(
        data, list
    ), f"Alerts file '{ALERTS_FILE}' must contain a JSON array."

    # We expect exactly 3 alerts as per the task description.
    expected_count = 3
    assert len(data) == expected_count, (
        f"Alerts file should contain exactly {expected_count} "
        f"objects but has {len(data)}."
    )

    # Spot-check the three alert IDs to ensure the file
    # is the one described in the task.
    expected_ids = {"a1", "a2", 100}
    actual_ids = {obj.get("id") for obj in data}
    assert actual_ids == expected_ids, (
        "Unexpected alert IDs found in alerts.json. "
        "Make sure you are using the draft alerts dataset provided in the task."
    )