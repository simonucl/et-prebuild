# test_initial_state.py
#
# This pytest suite verifies that the *initial* filesystem state is exactly
# what the exercise specification promises.  It must run **before** the
# student performs any action, therefore we purposely do **not** look for
# output artefacts such as “invalid_updates.log”.
#
# If any assertion fails the error message will precisely indicate what is
# missing or malformed so that the student immediately knows what to fix.

import json
import os
from pathlib import Path

import pytest

DEPLOY_DIR = Path("/home/user/deployment")
SCHEMA_PATH = DEPLOY_DIR / "schema.json"
UPDATES_PATH = DEPLOY_DIR / "updates.json"


@pytest.fixture(scope="module")
def schema_json():
    """Load and return schema.json as a Python object."""
    if not SCHEMA_PATH.is_file():
        pytest.fail(f"Missing file: {SCHEMA_PATH}")
    try:
        with SCHEMA_PATH.open(encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{SCHEMA_PATH} is not valid JSON: {exc}")


@pytest.fixture(scope="module")
def updates_json():
    """Load and return updates.json as a Python object."""
    if not UPDATES_PATH.is_file():
        pytest.fail(f"Missing file: {UPDATES_PATH}")
    try:
        with UPDATES_PATH.open(encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{UPDATES_PATH} is not valid JSON: {exc}")


def test_deployment_directory_exists():
    assert DEPLOY_DIR.is_dir(), f"Required directory {DEPLOY_DIR} does not exist."


def test_schema_file_content(schema_json):
    """
    Verify that schema.json exactly matches the specification given in the
    problem statement.
    """
    expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Update descriptor",
        "type": "object",
        "required": ["update_id", "version", "status"],
        "properties": {
            "update_id": {"type": "string"},
            "version": {
                "type": "string",
                "pattern": r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$",
            },
            "status": {
                "type": "string",
                "enum": ["pending", "applied"],
            },
        },
        "additionalProperties": False,
    }

    assert schema_json == expected_schema, (
        f"{SCHEMA_PATH} does not match the expected content.\n"
        "If the file was edited, please restore it to the exact specification."
    )


def test_updates_file_content(updates_json):
    """
    Verify that updates.json contains exactly the five records described in the
    task (order matters).
    """
    expected_updates = [
        {"update_id": "udp-100", "version": "1.2.0", "status": "pending"},
        {"update_id": "udp-101", "version": "1.2", "status": "pending"},
        {"update_id": "udp-102", "version": "1.3.0", "status": "deploying"},
        {"update_id": "udp-103", "version": "1.4.0", "status": "applied"},
        {"update_id": "udp-104", "version": "1.5.0"},
    ]

    assert updates_json == expected_updates, (
        f"{UPDATES_PATH} does not contain the expected data.\n"
        "Ensure the file matches the initial test fixture exactly."
    )