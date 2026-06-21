# test_initial_state.py
#
# Pytest suite that validates the filesystem *before* the student
# performs any action for the “account audit” exercise.
#
# This file checks that:
#   1. The expected data directory exists.
#   2. Exactly the two source files (users.json, user_schema.json) exist.
#   3. Neither of the two *output* files (valid_users.json,
#      invalid_users.log) exists yet.
#   4. users.json contains the 5 user objects that the exercise
#      description promises (and nothing else).
#   5. user_schema.json is a valid JSON-Schema enforcing the required
#      constraints (type, required properties, and additionalProperties).
#
# The tests purposefully fail with explicit, actionable messages if any
# pre-condition is violated.

import json
import os
from pathlib import Path

import pytest

# Constants
DATA_DIR = Path("/home/user/site_admin_data")
USERS_FILE = DATA_DIR / "users.json"
SCHEMA_FILE = DATA_DIR / "user_schema.json"
VALID_USERS_FILE = DATA_DIR / "valid_users.json"
INVALID_USERS_LOG = DATA_DIR / "invalid_users.log"


def _load_json(path: Path):
    """Utility: read JSON and return the parsed object, with nice errors."""
    try:
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        pytest.fail(f"Expected file {path} does not exist.")
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path} is not valid JSON: {exc}")


# ---------------------------------------------------------------------------
# Directory & file-presence checks
# ---------------------------------------------------------------------------

def test_data_directory_exists():
    assert DATA_DIR.exists(), f"Data directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."


def test_only_expected_source_files_present():
    """
    The directory must contain exactly the two source files and nothing
    that looks like the eventual outputs.
    """
    assert USERS_FILE.exists(), f"Missing source file: {USERS_FILE}"
    assert SCHEMA_FILE.exists(), f"Missing source file: {SCHEMA_FILE}"

    # Output files must NOT exist yet.
    assert not VALID_USERS_FILE.exists(), (
        f"{VALID_USERS_FILE} already exists; the student must create it only "
        "after running their solution."
    )
    assert not INVALID_USERS_LOG.exists(), (
        f"{INVALID_USERS_LOG} already exists; the student must create it only "
        "after running their solution."
    )


# ---------------------------------------------------------------------------
# Content checks for users.json
# ---------------------------------------------------------------------------

def test_users_json_structure_and_content():
    users = _load_json(USERS_FILE)

    # Must be a list of exactly five objects
    assert isinstance(users, list), "users.json must contain a JSON array."
    assert len(users) == 5, f"users.json should contain 5 user objects, found {len(users)}."

    # Helper: expected order & minimal fields (do NOT touch this ordering)
    expected_ids = [1, 2, 3, 4, 5]
    for idx, user in enumerate(users):
        assert isinstance(user, dict), f"Element {idx} in users.json is not a JSON object."

        # Each object must have an integer 'id' field (even if other fields
        # are intentionally wrong/missing for the exercise).
        assert "id" in user, f"User object at index {idx} is missing required key 'id'."
        assert user["id"] == expected_ids[idx], (
            f"User object at index {idx} has id {user['id']} "
            f"but expected id {expected_ids[idx]}."
        )

    # The first and last objects are the *valid* ones according to the
    # exercise description; make sure they still look correct so that
    # later tests have a stable baseline.
    first = users[0]
    last = users[-1]

    assert first == {
        "id": 1,
        "username": "alice",
        "active": True,
        "roles": ["admin", "editor"],
    }, "The first user object in users.json does not match the expected baseline."

    assert last["id"] == 5, "The last user object should have id 5."
    # Only basic sanity checks for the last object; its correctness is what
    # the student will have to verify later.
    for key in ("username", "active", "roles"):
        assert key in last, f"User id 5 should contain key '{key}'."


# ---------------------------------------------------------------------------
# Content checks for user_schema.json
# ---------------------------------------------------------------------------

def test_user_schema_enforces_required_constraints():
    schema = _load_json(SCHEMA_FILE)

    # Top-level expectations
    assert schema.get("type") == "object", "Schema 'type' must be 'object'."
    required_fields = schema.get("required")
    assert required_fields == ["id", "username", "active", "roles"], (
        "Schema must require the fields: id, username, active, roles "
        f"(found {required_fields})."
    )

    # Property type checks
    props = schema.get("properties", {})
    assert props.get("id", {}).get("type") == "integer", "Property 'id' type must be 'integer'."
    assert props.get("username", {}).get("type") == "string", "Property 'username' type must be 'string'."
    assert props.get("active", {}).get("type") == "boolean", "Property 'active' type must be 'boolean'."

    roles_prop = props.get("roles", {})
    assert roles_prop.get("type") == "array", "Property 'roles' must be of type array."
    assert roles_prop.get("items", {}).get("type") == "string", "Items of 'roles' array must be strings."

    # No additional properties allowed
    assert schema.get("additionalProperties") is False, (
        "Schema must disallow additional properties (additionalProperties: false)."
    )