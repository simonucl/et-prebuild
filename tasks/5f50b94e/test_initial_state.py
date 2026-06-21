# test_initial_state.py
#
# Pytest suite that validates the starting (pre-task) operating-system state
# for the “incident responder” assignment.  These tests confirm that:
#
# 1. The two source files supplied to the student exist and contain the exact
#    sample data described in the specification.
# 2. No output directory or artefacts from the yet-to-be-performed task are
#    present.
#
# NOTE: Only modules from the Python standard library and pytest are used.

import json
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOGS_DIR = HOME / "logs"
SCHEMAS_DIR = HOME / "schemas"
WORK_DIR = HOME / "incident2024"


###############################################################################
# Helper data used for the assertions
###############################################################################

EXPECTED_ALERTS = [
    {
        "id": "a1",
        "timestamp": "2024-05-01T10:00:00Z",
        "host": "web01",
        "severity": "low",
        "signature": "SQLi attempt",
        "src_ip": "10.0.0.5",
    },
    {
        "id": "a2",
        "timestamp": "2024-05-01T10:05:00Z",
        "host": "web02",
        "severity": "high",
        "signature": "XSS attempt",
        "src_ip": "10.0.0.6",
    },
    {
        "id": "a3",
        "timestamp": "2024-05-01T10:10:00Z",
        "host": "db01",
        "severity": "medium",
        "signature": "Login failure",
        "src_ip": "10.0.0.7",
    },
    {
        "id": "a4",
        "timestamp": "2024-05-01T10:15:00Z",
        "host": "web02",
        "severity": "high",
        "signature": "SQLi attempt",
        "src_ip": "10.0.0.8",
    },
    {
        "id": "a5",
        "timestamp": "2024-05-01T10:20:00Z",
        "host": "web03",
        "severity": "low",
        "signature": "Port scan",
        "src_ip": "10.0.0.9",
    },
]

EXPECTED_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["id", "timestamp", "host", "severity", "signature", "src_ip"],
    "properties": {
        "id": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "host": {"type": "string"},
        "severity": {"type": "string", "enum": ["low", "medium", "high"]},
        "signature": {"type": "string"},
        "src_ip": {"type": "string", "format": "ipv4"},
    },
    "additionalProperties": False,
}


###############################################################################
# Tests for the presence and correctness of the input artefacts
###############################################################################


def test_alerts_json_exists_and_is_correct():
    """
    Verify that /home/user/logs/alerts.json exists, is newline-delimited JSON,
    contains exactly five lines, and that each parsed object matches the
    expected data in both content and order.
    """
    alerts_path = LOGS_DIR / "alerts.json"
    assert alerts_path.is_file(), f"Missing alerts file at {alerts_path!s}"

    with alerts_path.open("r", encoding="utf-8") as fp:
        lines = fp.readlines()

    assert (
        len(lines) == len(EXPECTED_ALERTS)
    ), f"{alerts_path} should have {len(EXPECTED_ALERTS)} lines, found {len(lines)}"

    parsed_alerts = []
    for idx, line in enumerate(lines, start=1):
        line = line.rstrip("\n")
        assert line, f"Line {idx} in {alerts_path} is blank; ND-JSON must have JSON per line"
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            pytest.fail(f"Line {idx} in {alerts_path} is not valid JSON: {exc}")
        parsed_alerts.append(obj)

    # Compare each object to the expected one field-for-field
    for idx, (parsed, expected) in enumerate(zip(parsed_alerts, EXPECTED_ALERTS), start=1):
        assert parsed == expected, (
            f"Object on line {idx} of {alerts_path} does not match the expected content.\n"
            f"Expected: {expected}\nActual  : {parsed}"
        )


def test_alert_schema_exists_and_is_correct():
    """
    Verify that /home/user/schemas/alert_schema.json exists and that its JSON
    contents exactly match the schema laid out in the assignment.
    """
    schema_path = SCHEMAS_DIR / "alert_schema.json"
    assert schema_path.is_file(), f"Missing schema file at {schema_path!s}"

    try:
        with schema_path.open("r", encoding="utf-8") as fp:
            schema_data = json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{schema_path} is not valid JSON: {exc}")

    assert (
        schema_data == EXPECTED_SCHEMA
    ), f"The contents of {schema_path} do not match the expected schema."


###############################################################################
# Tests to ensure that no output artefacts exist before the student runs code
###############################################################################


def test_no_incident2024_directory_yet():
    """
    The working directory /home/user/incident2024 should NOT exist before the
    student carries out the task.
    """
    assert not WORK_DIR.exists(), (
        f"The directory {WORK_DIR} already exists, "
        "but it should only be created by the student's solution."
    )