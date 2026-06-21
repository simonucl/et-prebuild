# test_initial_state.py
#
# Pytest suite that validates the starting state of the filesystem for the
# “IoT connection report” exercise *before* the student begins to write code.
# It checks that:
#   • The expected directory structure exists.
#   • devices.json exists, is valid JSON, and contains the expected data.
#   • The reports directory exists and is empty.
#
# No tests are made against artefacts the student is expected to create
# (e.g. connection_summary.log).

import json
from pathlib import Path

import pytest


BASE_DIR = Path("/home/user/edge_devices")
DEVICES_JSON = BASE_DIR / "devices.json"
REPORTS_DIR = BASE_DIR / "reports"

# Expected values derived from the task description.
EXPECTED_TOTAL = 5
EXPECTED_ONLINE = 3
EXPECTED_OFFLINE = 2
EXPECTED_OFFLINE_LIST = "camera-1,sensor-2"


@pytest.fixture(scope="session")
def devices_data():
    """Load and return the parsed JSON from devices.json."""
    if not DEVICES_JSON.exists():
        pytest.fail(
            f"Required file not found: {DEVICES_JSON}. "
            "It should be provided in the initial exercise state."
        )
    if not DEVICES_JSON.is_file():
        pytest.fail(f"{DEVICES_JSON} exists but is not a regular file.")

    try:
        data = json.loads(DEVICES_JSON.read_text())
    except json.JSONDecodeError as exc:
        pytest.fail(f"{DEVICES_JSON} is not valid JSON: {exc}")

    if not isinstance(data, list):
        pytest.fail(f"{DEVICES_JSON} must contain a JSON array at top level.")

    return data


def test_base_directory_exists():
    assert BASE_DIR.exists(), f"Directory missing: {BASE_DIR}"
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


def test_reports_directory_exists_and_empty():
    assert REPORTS_DIR.exists(), f"Directory missing: {REPORTS_DIR}"
    assert REPORTS_DIR.is_dir(), f"{REPORTS_DIR} exists but is not a directory."

    # Ensure the directory is empty (no files/subdirs).
    contents = list(REPORTS_DIR.iterdir())
    assert (
        len(contents) == 0
    ), f"{REPORTS_DIR} should be empty before the exercise starts, found: {contents}"


def test_devices_json_structure_and_counts(devices_data):
    required_keys = {"id", "ip", "status"}

    for idx, device in enumerate(devices_data):
        msg_prefix = f"Entry index {idx} in {DEVICES_JSON}"
        assert isinstance(
            device, dict
        ), f"{msg_prefix} should be an object but found {type(device).__name__!s}"

        missing = required_keys - device.keys()
        assert (
            not missing
        ), f"{msg_prefix} is missing keys: {', '.join(sorted(missing))}"

        status = device["status"]
        assert status in {
            "online",
            "offline",
        }, f"{msg_prefix} has invalid status: {status!r}"

    # Compute counts.
    total = len(devices_data)
    online = sum(1 for d in devices_data if d["status"] == "online")
    offline = sum(1 for d in devices_data if d["status"] == "offline")
    offline_ids = sorted(d["id"] for d in devices_data if d["status"] == "offline")
    offline_list = ",".join(offline_ids)

    assert (
        total == EXPECTED_TOTAL
    ), f"Expected TOTAL={EXPECTED_TOTAL}, got {total} from {DEVICES_JSON}"
    assert (
        online == EXPECTED_ONLINE
    ), f"Expected ON={EXPECTED_ONLINE}, got {online} from {DEVICES_JSON}"
    assert (
        offline == EXPECTED_OFFLINE
    ), f"Expected OFF={EXPECTED_OFFLINE}, got {offline} from {DEVICES_JSON}"
    assert (
        offline_list == EXPECTED_OFFLINE_LIST
    ), f"Expected offline LIST='{EXPECTED_OFFLINE_LIST}', got '{offline_list}'"