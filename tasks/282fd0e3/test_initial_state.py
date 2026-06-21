# test_initial_state.py
#
# Pytest suite that verifies the pristine evidence bundle for ir_case_41
# is present exactly as described _before_ the student begins work.
#
# What we check:
#   • The directory /home/user/ir_case_41 exists.
#   • Exactly two files are present so far: login_schema.json and
#     login_events.json – and their contents match the canonical strings
#     provided by the task description.
#   • Expected artefact files produced by the student do NOT exist yet.
#
# Only stdlib + pytest are used.

import json
import pathlib
import textwrap

import pytest

IR_DIR = pathlib.Path("/home/user/ir_case_41")
SCHEMA_PATH = IR_DIR / "login_schema.json"
EVENTS_PATH = IR_DIR / "login_events.json"

ARTEFACTS = [
    IR_DIR / "validation_summary.json",
    IR_DIR / "suspicious_logins.json",
    IR_DIR / "suspicious_logins.log",
]

# Canonical contents pulled verbatim from the task description.
_EXPECTED_SCHEMA_JSON = textwrap.dedent(
    """
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "additionalProperties": false,
      "required": ["timestamp", "username", "src_ip", "auth_result"],
      "properties": {
        "timestamp": {
          "type": "string",
          "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
        },
        "username": { "type": "string" },
        "src_ip": {
          "type": "string",
          "pattern": "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\\\\.|$)){4}$"
        },
        "auth_result": {
          "type": "string",
          "enum": ["SUCCESS", "FAILURE"]
        }
      }
    }
    """
).strip()

_EXPECTED_EVENTS_JSON = textwrap.dedent(
    """
    [
      {
        "timestamp": "2023-08-25T03:12:11Z",
        "username": "alice",
        "src_ip": "10.0.0.5",
        "auth_result": "SUCCESS"
      },
      {
        "timestamp": "2023-08-25T03:14:47Z",
        "username": "bob",
        "src_ip": "172.16.4.20",
        "auth_result": "FAILURE"
      },
      {
        "timestamp": "2023-08-25 03:15:00",
        "username": "charlie",
        "src_ip": "192.168.1.99",
        "auth_result": "SUCCESS"
      },
      {
        "timestamp": "2023-08-25T03:19:00Z",
        "user": "dave",
        "src_ip": "8.8.8.8",
        "auth_result": "FAILURE"
      },
      {
        "timestamp": "2023-08-25T03:20:00Z",
        "username": "eve",
        "src_ip": "not_an_ip",
        "auth_result": "SUCCESS"
      },
      {
        "timestamp": "2023-08-25T03:25:00Z",
        "username": "alice",
        "src_ip": "10.0.0.5",
        "auth_result": "SUCCESS",
        "session_id": "abcd1234"
      },
      {
        "timestamp": "2023-08-25T03:31:00Z",
        "username": "frank",
        "src_ip": "203.0.113.55",
        "auth_result": "FAILURE"
      },
      {
        "timestamp": "2023-08-25T03:37:00Z",
        "username": "bob",
        "src_ip": "172.16.4.20",
        "auth_result": "SUCCESS"
      }
    ]
    """
).strip()


def _load_json(path: pathlib.Path):
    """
    Helper that returns (string_contents, parsed_json_object).

    Reading first lets us perform a meaningful diff if necessary.
    """
    raw = path.read_text(encoding="utf-8").strip()
    return raw, json.loads(raw)


@pytest.fixture(scope="module")
def expected_schema_obj():
    return json.loads(_EXPECTED_SCHEMA_JSON)


@pytest.fixture(scope="module")
def expected_events_obj():
    return json.loads(_EXPECTED_EVENTS_JSON)


def test_evidence_directory_exists():
    assert IR_DIR.is_dir(), f"Required directory {IR_DIR} is missing."


def test_required_files_exist():
    for fp in (SCHEMA_PATH, EVENTS_PATH):
        assert fp.is_file(), f"Required file {fp} is missing."


def test_no_artefacts_yet():
    for fp in ARTEFACTS:
        assert not fp.exists(), (
            f"Artefact {fp.name} already exists but should be created "
            "only after the investigation code runs."
        )


def test_login_schema_contents(expected_schema_obj):
    actual_raw, actual_obj = _load_json(SCHEMA_PATH)

    # Structural comparison
    assert (
        actual_obj == expected_schema_obj
    ), f"{SCHEMA_PATH} does not match the canonical schema."

    # Quick sanity check on required keys to give clearer error message
    for key in [
        "$schema",
        "type",
        "additionalProperties",
        "required",
        "properties",
    ]:
        assert key in actual_obj, (
            f"{SCHEMA_PATH} is malformed: missing top-level key '{key}'."
        )


def test_login_events_contents(expected_events_obj):
    actual_raw, actual_obj = _load_json(EVENTS_PATH)

    assert (
        actual_obj == expected_events_obj
    ), f"{EVENTS_PATH} does not match the canonical list of events."

    # Additional sanity checks
    assert isinstance(actual_obj, list), f"{EVENTS_PATH} must contain a JSON array."
    assert (
        len(actual_obj) == 8
    ), f"{EVENTS_PATH} should contain exactly 8 events but contains {len(actual_obj)}."