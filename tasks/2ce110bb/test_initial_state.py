# test_initial_state.py
#
# Pytest suite that verifies the **initial** state of the container
# before the student starts working on the task.  It checks that the
# expected directory and JSON files exist, that their contents are
# exactly as described in the specification, and that no output files
# produced by the task are present yet.
#
# Requirements verified:
#   • /home/user/iot_config           : directory exists
#   • /home/user/iot_config/device_config.json
#   • /home/user/iot_config/device_schema.json
#   • jq is installed and executable
#   • Output artefacts *do not* yet exist
#
# Only stdlib + pytest are used.

import json
import subprocess
from pathlib import Path

import pytest

HOME = Path("/home/user")
CFG_DIR = HOME / "iot_config"

DEVICE_CONFIG_PATH = CFG_DIR / "device_config.json"
DEVICE_SCHEMA_PATH = CFG_DIR / "device_schema.json"

INVALID_DEVICES_PATH = CFG_DIR / "invalid_devices.json"
VALIDATION_REPORT_PATH = CFG_DIR / "validation_report.log"


@pytest.fixture(scope="module")
def device_config_json():
    """
    Load and return the JSON data from device_config.json once per test session.
    """
    try:
        with DEVICE_CONFIG_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        pytest.fail(f"Required file missing: {DEVICE_CONFIG_PATH}", pytrace=False)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{DEVICE_CONFIG_PATH} is not valid JSON: {exc}", pytrace=False)


@pytest.fixture(scope="module")
def device_schema_json():
    """
    Load and return the JSON data from device_schema.json once per test session.
    """
    try:
        with DEVICE_SCHEMA_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        pytest.fail(f"Required file missing: {DEVICE_SCHEMA_PATH}", pytrace=False)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{DEVICE_SCHEMA_PATH} is not valid JSON: {exc}", pytrace=False)


def test_cfg_directory_exists():
    assert CFG_DIR.is_dir(), f"Directory missing: {CFG_DIR}"


def test_required_files_exist():
    assert DEVICE_CONFIG_PATH.is_file(), f"device_config.json missing at {DEVICE_CONFIG_PATH}"
    assert DEVICE_SCHEMA_PATH.is_file(), f"device_schema.json missing at {DEVICE_SCHEMA_PATH}"


def test_device_config_structure(device_config_json):
    """
    Validate that device_config.json contains exactly the five expected objects
    with the specified field values.
    """
    expected = [
        {"id": "dev-001", "status": "active", "ip": "192.168.1.10"},
        {"id": "dev-002", "status": "pending"},
        {"id": "dev-003", "status": "active", "ip": "192.168.1.12"},
        {"id": "dev-004", "status": "inactive", "ip": "192.168.1.13"},
        {"id": "dev-005", "status": "pending"},
    ]

    assert isinstance(
        device_config_json, list
    ), f"{DEVICE_CONFIG_PATH} must be a JSON array."

    assert (
        device_config_json == expected
    ), (
        f"{DEVICE_CONFIG_PATH} content does not match the expected structure.\n"
        f"Expected:\n{json.dumps(expected, indent=2)}\n\n"
        f"Found:\n{json.dumps(device_config_json, indent=2)}"
    )


def test_device_schema_structure(device_schema_json):
    """
    Validate that device_schema.json contains exactly the required key list.
    """
    expected_schema = {"required": ["id", "status", "ip"]}

    assert isinstance(
        device_schema_json, dict
    ), f"{DEVICE_SCHEMA_PATH} must be a JSON object."

    assert (
        device_schema_json == expected_schema
    ), (
        f"{DEVICE_SCHEMA_PATH} content does not match the expected schema.\n"
        f"Expected: {expected_schema}\nFound   : {device_schema_json}"
    )


def test_jq_is_available():
    """
    Ensure that the jq CLI is installed and callable from the shell.
    """
    try:
        result = subprocess.run(
            ["jq", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        pytest.fail(
            "jq command is not available in PATH but is required for the exercise.",
            pytrace=False,
        )

    assert (
        result.stdout.strip().startswith("jq-") or result.stderr.strip().startswith("jq-")
    ), "jq did not return its version string as expected."


def test_output_files_do_not_exist_yet():
    """
    Ensure that the files the student is supposed to create are *not* present
    before the task starts.
    """
    assert (
        not INVALID_DEVICES_PATH.exists()
    ), f"Output file already exists before validation: {INVALID_DEVICES_PATH}"

    assert (
        not VALIDATION_REPORT_PATH.exists()
    ), f"Output file already exists before validation: {VALIDATION_REPORT_PATH}"