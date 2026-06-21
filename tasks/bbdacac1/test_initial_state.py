# test_initial_state.py
#
# This test-suite verifies that the **initial** filesystem state for the
# “permissions audit” exercise is correct ­— i.e. before the student
# creates any artefacts such as `validation.log` or `admin_users.json`.
#
# What we check:
#   1. The directory /home/user/audit exists.
#   2. /home/user/audit/permissions.json   exists and its *bytes* match the
#      canonical specimen provided in the task description.
#   3. /home/user/audit/permissions.schema.json exists and its *bytes* also
#      match the canonical specimen.
#   4. The JSON inside permissions.json parses without error and satisfies
#      the structural requirements spelled out in the text‐based schema
#      (top-level “users” array, each object has “username”, “uid”,
#      “permissions”).
#
# We deliberately DO NOT test for the presence or absence of any output
# artefacts (validation.log, admin_users.json) as per the specification.

import json
import pathlib
import pytest

AUDIT_DIR = pathlib.Path("/home/user/audit")
PERMISSIONS_FILE = AUDIT_DIR / "permissions.json"
SCHEMA_FILE = AUDIT_DIR / "permissions.schema.json"

# Canonical byte-for-byte expectations (including the final newline).
EXPECTED_PERMISSIONS_JSON = """{
  "users": [
    { "username": "alice", "uid": 1001, "permissions": ["read", "write"] },
    { "username": "bob", "uid": 1002, "permissions": ["read"] },
    { "username": "carol", "uid": 0, "permissions": ["read", "write", "execute", "admin"] },
    { "username": "dave", "uid": 1003, "permissions": ["read", "write", "execute"] }
  ]
}
"""

EXPECTED_SCHEMA_JSON = """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["users"],
  "properties": {
    "users": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["username", "uid", "permissions"],
        "properties": {
          "username": { "type": "string" },
          "uid": { "type": "integer" },
          "permissions": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    }
  }
}
"""

@pytest.fixture(scope="module")
def permissions_content():
    """
    Reads the raw bytes and the parsed JSON for permissions.json.
    Raises explicit assertion failures if the file is missing.
    """
    assert PERMISSIONS_FILE.exists(), (
        f"Expected file {PERMISSIONS_FILE} is missing. "
        "It must be present before starting the exercise."
    )
    raw = PERMISSIONS_FILE.read_text(encoding="utf-8")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{PERMISSIONS_FILE} is not valid JSON: {exc}")  # pragma: no cover
    return raw, parsed


def test_audit_directory_exists():
    assert AUDIT_DIR.exists() and AUDIT_DIR.is_dir(), (
        f"Required directory {AUDIT_DIR} does not exist."
    )


def test_permissions_json_exact_bytes(permissions_content):
    raw, _ = permissions_content
    assert raw == EXPECTED_PERMISSIONS_JSON, (
        f"Content of {PERMISSIONS_FILE} does not match the expected specimen.\n"
        "If this file was modified, restore it to the original state given in "
        "the task description."
    )


def test_schema_json_exact_bytes():
    assert SCHEMA_FILE.exists(), (
        f"Expected file {SCHEMA_FILE} is missing. "
        "It must be present before starting the exercise."
    )
    raw = SCHEMA_FILE.read_text(encoding="utf-8")
    assert raw == EXPECTED_SCHEMA_JSON, (
        f"Content of {SCHEMA_FILE} does not match the expected specimen.\n"
        "If this file was modified, restore it to the original state given in "
        "the task description."
    )


def test_permissions_json_structure(permissions_content):
    _, data = permissions_content

    # 1. Top-level must be a dict with key "users" that is a list.
    assert isinstance(data, dict), "Top-level JSON structure must be an object."
    assert "users" in data, 'Top-level key "users" is missing.'
    users = data["users"]
    assert isinstance(users, list), '"users" must be an array.'

    # 2. Each user object must have the three mandatory keys.
    required_keys = {"username", "uid", "permissions"}
    for idx, user in enumerate(users):
        assert isinstance(user, dict), f"User at index {idx} is not an object."
        missing = required_keys - user.keys()
        assert not missing, (
            f"User at index {idx} is missing required key(s): {', '.join(sorted(missing))}"
        )
        assert isinstance(user["username"], str), (
            f'"username" of user index {idx} is not a string.'
        )
        assert isinstance(user["uid"], int), (
            f'"uid" of user index {idx} is not an integer.'
        )
        assert isinstance(user["permissions"], list), (
            f'"permissions" of user index {idx} is not an array.'
        )


# EOF