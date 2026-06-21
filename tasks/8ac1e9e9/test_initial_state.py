# test_initial_state.py
"""
Pytest suite that validates the **initial** on-disk state of the operating
system *before* the student begins the assignment.

The tests confirm that:
1. The /home/user/diagnostics directory exists.
2. The two required JSON files are present.
3. The contents of raw_diagnostic.json and device_schema.json match the
   specification given in the task description.
4. The output file support_summary.log does **not** yet exist.
"""

import json
from pathlib import Path

import pytest

DIAG_DIR = Path("/home/user/diagnostics")
RAW_FILE = DIAG_DIR / "raw_diagnostic.json"
SCHEMA_FILE = DIAG_DIR / "device_schema.json"
OUTPUT_FILE = DIAG_DIR / "support_summary.log"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def load_json(file_path: Path):
    """Load JSON from *file_path* and return the parsed object."""
    try:
        with file_path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        pytest.fail(f"Required file missing: {file_path}", pytrace=False)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{file_path} is not valid JSON: {exc}", pytrace=False)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_diagnostics_directory_exists():
    assert DIAG_DIR.is_dir(), (
        f"Expected diagnostics directory absent: {DIAG_DIR}"
    )


def test_required_json_files_exist():
    missing = [p for p in (RAW_FILE, SCHEMA_FILE) if not p.is_file()]
    assert not missing, (
        "Missing required JSON file(s): "
        + ", ".join(str(p) for p in missing)
    )


def test_raw_diagnostic_content():
    data = load_json(RAW_FILE)

    # Top-level checks
    expected_top_keys = {
        "device_id",
        "uptime_seconds",
        "firmware_version",
        "interfaces",
    }
    assert expected_top_keys.issubset(
        data
    ), (
        f"{RAW_FILE} is missing required keys: "
        f"{expected_top_keys - set(data)}"
    )

    assert data["device_id"] == "router-4431", (
        f'device_id should be "router-4431", found "{data["device_id"]}"'
    )
    assert data["uptime_seconds"] == 86400, (
        f"uptime_seconds should be 86400, found {data['uptime_seconds']}"
    )
    assert data["firmware_version"] == "v1.2.3", (
        f'firmware_version should be "v1.2.3", found "{data["firmware_version"]}"'
    )

    # Interfaces checks
    interfaces = data["interfaces"]
    assert isinstance(interfaces, list) and len(interfaces) == 2, (
        "interfaces should be a list containing exactly 2 items"
    )

    expected_ifaces = [
        {
            "name": "eth0",
            "rx_packets": 120000,
            "tx_packets": 118000,
            "status": "up",
        },
        {
            "name": "eth1",
            "rx_packets": 50000,
            "tx_packets": 52000,
            "status": "down",
        },
    ]

    for i, (actual, expected) in enumerate(zip(interfaces, expected_ifaces)):
        assert actual == expected, (
            f"Interface #{i} does not match expected content.\n"
            f"Expected: {expected}\n"
            f"Found   : {actual}"
        )


def test_device_schema_content():
    schema = load_json(SCHEMA_FILE)

    # Ensure basic Draft-04 schema structure is present.
    required_schema_keys = {"$schema", "type", "properties", "required"}
    assert required_schema_keys.issubset(
        schema
    ), (
        f"{SCHEMA_FILE} missing required schema keys: "
        f"{required_schema_keys - set(schema)}"
    )

    # Spot-check a few critical parts of the schema.
    props = schema["properties"]
    assert "interfaces" in props, (
        '"interfaces" definition missing in device_schema.json'
    )

    iface_items = props["interfaces"]["items"]["properties"]
    status_enum = iface_items["status"]["enum"]
    assert status_enum == ["up", "down"], (
        f'Status enum should be ["up", "down"], found {status_enum}'
    )


def test_output_file_not_yet_present():
    assert not OUTPUT_FILE.exists(), (
        f"Output file {OUTPUT_FILE} should NOT exist before the task is executed."
    )