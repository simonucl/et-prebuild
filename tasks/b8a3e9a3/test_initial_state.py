# test_initial_state.py
#
# This test-suite validates the **initial** filesystem state that must be
# present **before** the student attempts the JSON → CSV conversion task.
#
# It deliberately avoids checking for the eventual CSV export or its
# directory, in accordance with the grading rules.
#
# Requirements being verified:
#
# 1. /home/user/project/assets/users.json must exist as a regular file.
# 2. The file must contain valid JSON representing a list of exactly three
#    objects, each having the keys: id, name, email
# 3. The values of those objects must match the specification so the student
#    starts from a known, correct dataset.
#
# Any failure message is crafted to tell the student precisely what is
# missing or malformed.

import json
from pathlib import Path
import pytest


JSON_PATH = Path("/home/user/project/assets/users.json")


@pytest.fixture(scope="module")
def users_json_text():
    """
    Returns the raw text of the users.json file, or fails with a helpful
    message if the file is missing.
    """
    if not JSON_PATH.exists():
        pytest.fail(
            f"Required input file not found: {JSON_PATH}\n"
            "Make sure the project scaffolding is intact before starting the exercise."
        )

    if not JSON_PATH.is_file():
        pytest.fail(
            f"Expected {JSON_PATH} to be a regular file, but something else exists at that path."
        )

    try:
        return JSON_PATH.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {JSON_PATH}: {exc}")


def test_json_is_valid(users_json_text):
    """
    The file must contain syntactically valid JSON.
    """
    try:
        json.loads(users_json_text)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{JSON_PATH} does not contain valid JSON: {exc}")


def test_json_structure_and_content(users_json_text):
    """
    Assert the JSON represents the exact list of users described in the
    task instructions.
    """
    data = json.loads(users_json_text)

    # 1. Must be a list
    assert isinstance(data, list), (
        f"{JSON_PATH} should contain a JSON array, "
        f"but we found a {type(data).__name__} instead."
    )

    # 2. Must contain exactly three user objects
    expected_length = 3
    assert len(data) == expected_length, (
        f"{JSON_PATH} should contain exactly {expected_length} user objects, "
        f"but it has {len(data)}."
    )

    # 3. Each object must have id, name, email keys and match expected values
    expected_records = [
        {"id": 1, "name": "Ada Lovelace",     "email": "ada@example.com"},
        {"id": 2, "name": "Linus Torvalds",   "email": "linus@example.com"},
        {"id": 3, "name": "Grace Hopper",     "email": "grace@example.com"},
    ]

    for idx, (record, expected) in enumerate(zip(data, expected_records), start=1):
        assert isinstance(record, dict), (
            f"Element #{idx} in {JSON_PATH} should be an object, "
            f"but found {type(record).__name__}."
        )

        # Ensure all required keys exist
        missing = [key for key in ("id", "name", "email") if key not in record]
        if missing:
            pytest.fail(
                f"Element #{idx} in {JSON_PATH} is missing keys: {', '.join(missing)}"
            )

        # Check value equality
        assert record == expected, (
            f"Element #{idx} in {JSON_PATH} differs from expected.\n"
            f"  Expected: {expected}\n"
            f"  Found   : {record}"
        )