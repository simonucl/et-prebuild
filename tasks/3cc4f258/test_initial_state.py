# test_initial_state.py
#
# This test-suite verifies that the machine is in the **initial**
# state expected by the assignment.  Only the pre-existing hardening
# data are checked; the files that the student is supposed to create
# later (validation.log, open_ports.txt, config_hardened.json, …) are
# deliberately **not** tested here.

import json
from pathlib import Path

import pytest

HARDENING_DIR = Path("/home/user/hardening")

EXPECTED_CONFIG = {
    "system": "webserver",
    "ssh": {
        "permitRootLogin": "no",
        "passwordAuthentication": "no",
    },
    "firewall": {"portsOpen": [22, 80, 443]},
}

EXPECTED_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["system", "ssh", "firewall"],
    "properties": {
        "system": {"type": "string"},
        "ssh": {
            "type": "object",
            "required": ["permitRootLogin", "passwordAuthentication"],
            "properties": {
                "permitRootLogin": {"type": "string", "enum": ["yes", "no"]},
                "passwordAuthentication": {"type": "string", "enum": ["yes", "no"]},
            },
            "additionalProperties": False,
        },
        "firewall": {
            "type": "object",
            "required": ["portsOpen"],
            "properties": {
                "portsOpen": {"type": "array", "items": {"type": "integer"}}
            },
            "additionalProperties": False,
        },
    },
    "additionalProperties": False,
}


@pytest.fixture(scope="module")
def config_path() -> Path:
    return HARDENING_DIR / "config.json"


@pytest.fixture(scope="module")
def schema_path() -> Path:
    return HARDENING_DIR / "schema.json"


def test_hardening_directory_exists():
    assert HARDENING_DIR.is_dir(), (
        f"Expected directory {HARDENING_DIR} to exist. "
        "Make sure the hardening data are located at the correct path."
    )


def test_config_json_exists(config_path: Path):
    assert config_path.is_file(), (
        f"Missing file: {config_path}. "
        "The original JSON configuration must be present before any action is taken."
    )


def test_schema_json_exists(schema_path: Path):
    assert schema_path.is_file(), (
        f"Missing file: {schema_path}. "
        "The JSON-schema file must be present before any action is taken."
    )


def _load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path} is not valid JSON: {exc}")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {path}: {exc}")


def test_config_json_content(config_path: Path):
    data = _load_json(config_path)
    assert data == EXPECTED_CONFIG, (
        f"Content of {config_path} does not match the expected initial configuration.\n"
        "If you already modified this file, restore it to the original state."
    )


def test_schema_json_content(schema_path: Path):
    data = _load_json(schema_path)
    assert data == EXPECTED_SCHEMA, (
        f"Content of {schema_path} does not match the expected initial JSON schema.\n"
        "If you already modified this file, restore it to the original state."
    )