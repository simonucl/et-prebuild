# test_initial_state.py
#
# This test-suite validates that the filesystem contains
# exactly the raw materials promised in the task description
# *before* the student performs any action.
#
# It intentionally DOES NOT look for the output artefacts
# (usage_summary.json, validation.log, …).  Its only purpose
# is to guarantee that the starting point is correct.

import json
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/projects/profile")
RUN1_PATH = BASE_DIR / "run1.json"
RUN2_PATH = BASE_DIR / "run2.json"
SCHEMA_DIR = BASE_DIR / "schema"
SCHEMA_PATH = SCHEMA_DIR / "usage_summary.schema.json"


@pytest.fixture(scope="module")
def run1_data():
    """Return JSON data from run1.json."""
    with RUN1_PATH.open(encoding="utf-8") as fp:
        return json.load(fp)


@pytest.fixture(scope="module")
def run2_data():
    """Return JSON data from run2.json."""
    with RUN2_PATH.open(encoding="utf-8") as fp:
        return json.load(fp)


@pytest.fixture(scope="module")
def schema_data():
    """Return JSON data from usage_summary.schema.json."""
    with SCHEMA_PATH.open(encoding="utf-8") as fp:
        return json.load(fp)


def test_directory_structure_exists():
    assert BASE_DIR.is_dir(), f"Expected directory {BASE_DIR} to exist."
    assert RUN1_PATH.is_file(), f"Missing file: {RUN1_PATH}"
    assert RUN2_PATH.is_file(), f"Missing file: {RUN2_PATH}"
    assert SCHEMA_DIR.is_dir(), f"Expected directory {SCHEMA_DIR} to exist."
    assert SCHEMA_PATH.is_file(), f"Missing schema file: {SCHEMA_PATH}"


def test_run1_contents(run1_data):
    # Expected content for /home/user/projects/profile/run1.json
    expected = [
        {
            "process": "nginx",
            "cpu_usage": 12.5,
            "mem_usage": 150.2,
            "threads": 4,
            "pid": 1023,
        },
        {
            "process": "redis",
            "cpu_usage": 7.9,
            "mem_usage": 85.0,
            "threads": 2,
            "pid": 1078,
        },
    ]

    assert isinstance(
        run1_data, list
    ), f"{RUN1_PATH} should contain a JSON array, got {type(run1_data).__name__}"

    assert len(run1_data) == len(
        expected
    ), f"{RUN1_PATH} should contain {len(expected)} objects, found {len(run1_data)}."

    for idx, (got, exp) in enumerate(zip(run1_data, expected)):
        assert got == exp, (
            f"Mismatch in {RUN1_PATH} at index {idx}.\n"
            f"Expected: {exp}\n"
            f"Got     : {got}"
        )


def test_run2_contents(run2_data):
    # Expected content for /home/user/projects/profile/run2.json
    expected = [
        {
            "process": "postgres",
            "cpu_usage": 18.2,
            "mem_usage": 230.4,
            "threads": 5,
            "pid": 1337,
        }
    ]

    assert isinstance(
        run2_data, list
    ), f"{RUN2_PATH} should contain a JSON array, got {type(run2_data).__name__}"

    assert len(run2_data) == len(
        expected
    ), f"{RUN2_PATH} should contain {len(expected)} objects, found {len(run2_data)}."

    got = run2_data[0]
    exp = expected[0]
    assert got == exp, (
        f"Content mismatch in {RUN2_PATH}.\n"
        f"Expected: {exp}\n"
        f"Got     : {got}"
    )


def test_schema_contents(schema_data):
    """
    Verify that the schema file is recognisably the Draft-07 schema
    described in the task.  We only check key properties so that the
    test is tolerant of formatting/style differences.
    """
    assert schema_data.get("$schema") == "http://json-schema.org/draft-07/schema#", (
        f"{SCHEMA_PATH} should declare Draft-07 JSON-Schema."
    )

    assert (
        schema_data.get("type") == "array"
    ), f"{SCHEMA_PATH} root 'type' must be 'array'."

    items = schema_data.get("items")
    assert isinstance(
        items, dict
    ), f"{SCHEMA_PATH} must define an 'items' object describing array elements."

    # Required keys inside item schema
    required_keys = {"process", "cpu_usage", "mem_usage"}
    assert set(items.get("required", [])) == required_keys, (
        f"{SCHEMA_PATH}: 'required' should be {sorted(required_keys)}."
    )

    props = items.get("properties", {})
    for key in required_keys:
        assert key in props, f"{SCHEMA_PATH}: missing property definition for '{key}'."

    # Ensure additionalProperties is explicitly false
    assert (
        items.get("additionalProperties") is False
    ), f"{SCHEMA_PATH}: 'additionalProperties' must be false."