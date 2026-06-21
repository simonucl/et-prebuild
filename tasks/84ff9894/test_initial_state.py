# test_initial_state.py
#
# This pytest suite validates that the *initial* operating-system / filesystem
# state exactly matches what the student task description promises *before*
# the student performs any action.  It deliberately avoids checking anything
# inside /home/user/output in accordance with the grading instructions.

import json
import os
from pathlib import Path

import pytest


DATA_DIR = Path("/home/user/data")
SCAN_RESULTS_PATH = DATA_DIR / "scan_results.json"
SCAN_SCHEMA_PATH = DATA_DIR / "scan_schema.json"


@pytest.fixture(scope="session")
def expected_scan_results():
    """Return the Python representation of the expected scan_results.json."""
    return [
        {
            "id": "VULN-001",
            "name": "Remote Code Execution",
            "severity": "critical",
            "cvss": 9.8,
        },
        {
            "id": "VULN-002",
            "name": "SQL Injection",
            "severity": "high",
            "cvss": 9.0,
        },
        {
            "id": "VULN-003",
            "name": "Directory Traversal",
            "severity": "medium",
            "cvss": 6.5,
        },
        {
            "id": "VULN-004",
            "name": "Buffer Overflow",
            "severity": "critical",
            "cvss": 9.1,
        },
        {
            "id": "VULN-005",
            "name": "Cross-Site Scripting",
            "severity": "low",
            "cvss": 4.3,
        },
    ]


@pytest.fixture(scope="session")
def expected_scan_schema():
    """Return the Python representation of the expected scan_schema.json."""
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "array",
        "items": {
            "type": "object",
            "required": ["id", "name", "severity", "cvss"],
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "severity": {
                    "type": "string",
                    "enum": ["critical", "high", "medium", "low"],
                },
                "cvss": {"type": "number"},
            },
            "additionalProperties": False,
        },
    }


def _assert_trailing_newline(path: Path) -> None:
    """Ensure the file ends with a single trailing newline."""
    with path.open("rb") as fh:
        fh.seek(-1, os.SEEK_END)
        last_byte = fh.read(1)
    assert (
        last_byte == b"\n"
    ), f"{path} is expected to end with a single trailing newline, but it does not."


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), f"Expected directory {DATA_DIR} to exist."


def test_scan_results_file_contents(expected_scan_results):
    assert SCAN_RESULTS_PATH.is_file(), (
        f"Required file {SCAN_RESULTS_PATH} is missing."
    )

    _assert_trailing_newline(SCAN_RESULTS_PATH)

    with SCAN_RESULTS_PATH.open("r", encoding="utf-8") as fh:
        try:
            actual = json.load(fh)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{SCAN_RESULTS_PATH} is not valid JSON: {exc}")

    assert (
        actual == expected_scan_results
    ), f"{SCAN_RESULTS_PATH} contents do not match the expected initial data."


def test_scan_schema_file_contents(expected_scan_schema):
    assert SCAN_SCHEMA_PATH.is_file(), (
        f"Required file {SCAN_SCHEMA_PATH} is missing."
    )

    _assert_trailing_newline(SCAN_SCHEMA_PATH)

    with SCAN_SCHEMA_PATH.open("r", encoding="utf-8") as fh:
        try:
            actual = json.load(fh)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{SCAN_SCHEMA_PATH} is not valid JSON: {exc}")

    assert (
        actual == expected_scan_schema
    ), f"{SCAN_SCHEMA_PATH} contents do not match the expected initial schema."