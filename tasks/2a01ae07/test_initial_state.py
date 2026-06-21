# test_initial_state.py
"""
Pytest suite that verifies the initial filesystem state **before** the student
performs the credential-rotation exercise.

The checks performed here purposefully do **not** touch any of the files that
will be produced or modified by the student solution (e.g. `rotation.log`
or the *rotated* version of `credentials.json`).  Instead, we assert that the
starting conditions are exactly as described in the task statement.

Only the Python standard library and `pytest` are used, in accordance with the
specification.
"""

import json
import re
from pathlib import Path

import pytest


HOME = Path("/home/user")
SECRETS_DIR = HOME / "secrets"

# Full, absolute paths to the three **input** files
CREDENTIALS_JSON = SECRETS_DIR / "credentials.json"
SCHEMA_JSON = SECRETS_DIR / "credentials_schema.json"
NEW_TOKENS_JSON = SECRETS_DIR / "new_tokens.json"

DATE_PATTERN = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


@pytest.fixture(scope="session")
def credentials_data():
    with CREDENTIALS_JSON.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@pytest.fixture(scope="session")
def schema_data():
    with SCHEMA_JSON.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@pytest.fixture(scope="session")
def new_tokens_data():
    with NEW_TOKENS_JSON.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def test_secrets_directory_exists():
    assert SECRETS_DIR.is_dir(), (
        f"Expected secrets directory at '{SECRETS_DIR}', "
        "but it does not exist or is not a directory."
    )


@pytest.mark.parametrize(
    "path_obj,description",
    [
        (CREDENTIALS_JSON, "credentials.json"),
        (SCHEMA_JSON, "credentials_schema.json"),
        (NEW_TOKENS_JSON, "new_tokens.json"),
    ],
)
def test_required_files_exist(path_obj: Path, description: str):
    assert path_obj.is_file(), f"Missing required file: {path_obj} ({description})"


def test_credentials_json_structure(credentials_data):
    """
    The initial credentials.json must:

    1. Be a JSON array.
    2. Contain exactly two objects (db and ci).
    3. Each object must have the required keys with string values.
    4. The 'created' and 'expires' fields must match YYYY-MM-DD.
    5. Tokens must *not* yet be rotated (old values are expected).
    """
    # 1 – must be a list
    assert isinstance(credentials_data, list), (
        f"Expected credentials.json to contain a JSON array, "
        f"got {type(credentials_data).__name__}"
    )

    # 2 – exact number of entries
    assert len(credentials_data) == 2, (
        "credentials.json should contain exactly two credential objects "
        f"(db and ci), but contains {len(credentials_data)}."
    )

    # 3,4,5 – per-entry checks
    expected_entries = {
        "db": {
            "token": "db-12345",
            "created": "2022-12-01",
            "expires": "2023-03-01",
        },
        "ci": {
            "token": "ci-abcde",
            "created": "2022-12-15",
            "expires": "2023-03-15",
        },
    }

    services_seen = set()
    for entry in credentials_data:
        # Must be a dict
        assert isinstance(entry, dict), "Each array element must be a JSON object."

        # Required keys
        required_keys = {"service", "token", "created", "expires"}
        missing = required_keys - entry.keys()
        assert not missing, f"Credential object missing required keys: {missing}"

        # All values should be strings
        for key in required_keys:
            assert isinstance(entry[key], str), (
                f"Value for '{key}' in service '{entry['service']}' "
                f"should be a string."
            )

        # 'created' and 'expires' format
        for date_key in ("created", "expires"):
            value = entry[date_key]
            assert DATE_PATTERN.fullmatch(value), (
                f"Value for '{date_key}' in service '{entry['service']}' "
                f"does not match YYYY-MM-DD: '{value}'"
            )

        # Check expected initial content (tokens not yet rotated)
        service = entry["service"]
        services_seen.add(service)
        assert service in expected_entries, (
            f"Unexpected service '{service}' found in credentials.json."
        )

        for key, expected_val in expected_entries[service].items():
            actual_val = entry[key]
            assert (
                actual_val == expected_val
            ), f"Mismatch for '{service}.{key}': expected '{expected_val}', got '{actual_val}'"

    # Ensure no extra / missing services
    assert services_seen == set(expected_entries), (
        f"Services present {services_seen}; expected {set(expected_entries)}."
    )


def test_schema_json_is_draft_07(schema_data):
    """
    Basic sanity check that the supplied schema advertises Draft-07.
    (Full JSON-Schema validation is intentionally avoided to keep the
    dependency footprint at stdlib-only.)
    """
    assert (
        schema_data.get("$schema") == "http://json-schema.org/draft-07/schema#"
    ), "credentials_schema.json should declare Draft-07 compatibility."


def test_credentials_conforms_to_schema_subset(credentials_data, schema_data):
    """
    Minimal, *manual* validation of credentials.json against the schema:
    we make sure the required properties exist and that 'created' /
    'expires' satisfy the declared regex.

    This is **not** a full JSON-Schema implementation, but it is enough
    to guarantee that the starting data set is valid and ready for the
    student solution.
    """
    required = set(schema_data["items"]["required"])
    pattern = re.compile(schema_data["items"]["properties"]["created"]["pattern"])

    for entry in credentials_data:
        assert required <= entry.keys(), (
            f"Credential object {entry} is missing one or more required keys: "
            f"{required - entry.keys()}"
        )
        assert pattern.fullmatch(entry["created"]), (
            f"'created' value '{entry['created']}' does not match pattern."
        )
        assert pattern.fullmatch(entry["expires"]), (
            f"'expires' value '{entry['expires']}' does not match pattern."
        )


def test_new_tokens_json_content(new_tokens_data):
    """
    Confirm that new_tokens.json contains exactly the expected two entries
    with the correct new token values.
    """
    assert isinstance(new_tokens_data, list), "new_tokens.json must be a JSON array."
    expected = {"db": "db-67890", "ci": "ci-fghij"}
    assert len(new_tokens_data) == 2, (
        "new_tokens.json should contain exactly two token objects "
        f"(db and ci), got {len(new_tokens_data)}."
    )
    seen = {}
    for obj in new_tokens_data:
        assert isinstance(obj, dict), "Each token entry should be a JSON object."
        for key in ("service", "token"):
            assert key in obj, f"Token entry missing key '{key}': {obj}"
            assert isinstance(obj[key], str), f"Value for '{key}' should be a string."
        svc, tok = obj["service"], obj["token"]
        seen[svc] = tok

    assert seen == expected, (
        "new_tokens.json contents do not match expected values.\n"
        f"Expected: {expected}\nGot:      {seen}"
    )