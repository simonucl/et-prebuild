# test_initial_state.py
"""
Pytest suite that validates the operating-system / filesystem **before**
the student runs the solution command for the IoT-thermostat task.

Only the initial, pre-existing artefacts are checked here.
Nothing related to the files that the student must create is asserted.
"""

import json
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DEPLOYMENT_DIR = HOME / "iot" / "deployment"
LOGS_DIR = HOME / "iot" / "logs"
DEVICE_STATUS_JSON = DEPLOYMENT_DIR / "device_status.json"
DEVICE_STATUS_SCHEMA = DEPLOYMENT_DIR / "device_status_schema.json"


def _read_json(path: Path):
    """Utility: read a JSON file and return the parsed data."""
    with path.open("r", encoding="utf-8") as fp:
        try:
            return json.load(fp)
        except json.JSONDecodeError as exc:  # pragma: no cover
            pytest.fail(f"{path} contains invalid JSON: {exc}")  # noqa: TRY003


def test_deployment_directory_exists():
    assert DEPLOYMENT_DIR.is_dir(), (
        f"Required directory missing: {DEPLOYMENT_DIR}\n"
        "Make sure the IoT deployment directory hierarchy is present."
    )


def test_logs_directory_exists_and_is_writable():
    assert LOGS_DIR.is_dir(), (
        f"Required directory missing: {LOGS_DIR}\n"
        "The student needs this directory to append the log entry."
    )
    assert os.access(LOGS_DIR, os.W_OK), (
        f"Directory not writable: {LOGS_DIR}\n"
        "Ensure the regular user can create/append log files here."
    )


def test_device_status_json_exists_and_has_expected_shape():
    # File existence ---------------------------------------------------------
    assert DEVICE_STATUS_JSON.is_file(), (
        f"Missing file: {DEVICE_STATUS_JSON}\n"
        "The task cannot proceed without the device status data."
    )

    # Content is valid JSON --------------------------------------------------
    data = _read_json(DEVICE_STATUS_JSON)

    # Must be a list ---------------------------------------------------------
    assert isinstance(data, list), (
        f"{DEVICE_STATUS_JSON} should contain a JSON array, "
        f"but found {type(data).__name__}."
    )

    # Expected number of entries --------------------------------------------
    expected_count = 5
    assert len(data) == expected_count, (
        f"{DEVICE_STATUS_JSON} should contain {expected_count} elements, "
        f"found {len(data)}."
    )

    # Validate each element --------------------------------------------------
    required_keys = {"device_id", "status", "ip"}
    for idx, element in enumerate(data):
        assert isinstance(element, dict), (
            f"Element #{idx} in {DEVICE_STATUS_JSON} is not an object."
        )
        missing = required_keys - element.keys()
        assert not missing, (
            f"Element #{idx} is missing required keys: {sorted(missing)}"
        )

    # Ensure the expected offline devices are present ------------------------
    offline_ids = sorted(
        elem["device_id"] for elem in data if elem.get("status") == "offline"
    )
    expected_offline = sorted(["edge-therm-02", "edge-therm-05"])
    assert offline_ids == expected_offline, (
        "Offline devices do not match the expected initial state.\n"
        f"Expected offline IDs: {expected_offline}\n"
        f"Found offline IDs:    {offline_ids}"
    )


def test_device_status_schema_exists():
    assert DEVICE_STATUS_SCHEMA.is_file(), (
        f"Missing file: {DEVICE_STATUS_SCHEMA}\n"
        "The JSON-Schema reference file must be present even if the student "
        "does not need to modify it."
    )