# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student runs any command.  It asserts that:
#
# 1. The source files that already exist (/home/user/build/artifacts.json and
#    /home/user/build/artifact_schema.json) are present and contain the exact
#    data described in the task statement.
# 2. The target output files (/home/user/build/filtered_artifacts.json and
#    /home/user/build/filter.log) are **not** present yet.
#
# Any failure message should clearly indicate what is wrong so that the
# student can fix the workspace before proceeding.

import json
import os
from pathlib import Path

import pytest

BUILD_DIR = Path("/home/user/build")
ARTIFACTS_JSON = BUILD_DIR / "artifacts.json"
SCHEMA_JSON = BUILD_DIR / "artifact_schema.json"
FILTERED_JSON = BUILD_DIR / "filtered_artifacts.json"
FILTER_LOG = BUILD_DIR / "filter.log"


@pytest.fixture(scope="module")
def artifacts_content():
    """Return the parsed JSON content of artifacts.json."""
    if not ARTIFACTS_JSON.exists():
        pytest.skip(f"{ARTIFACTS_JSON} is missing")
    try:
        return json.loads(ARTIFACTS_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        pytest.fail(f"{ARTIFACTS_JSON} is not valid JSON: {exc}")


@pytest.fixture(scope="module")
def schema_content():
    """Return the parsed JSON content of artifact_schema.json."""
    if not SCHEMA_JSON.exists():
        pytest.skip(f"{SCHEMA_JSON} is missing")
    try:
        return json.loads(SCHEMA_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        pytest.fail(f"{SCHEMA_JSON} is not valid JSON: {exc}")


def test_artifacts_json_exists_and_matches_expected(artifacts_content):
    """
    Ensure /home/user/build/artifacts.json exists and contains exactly the
    three artifacts described in the task (order and values matter).
    """
    expected = [
        {
            "name": "core-lib",
            "version": "1.2.3",
            "sha256": (
                "abc123def456abc123def456abc123def456"
                "abc123def456abc123def456"
            ),
        },
        {
            "name": "ui-lib",
            "version": "2.0.1",
            "sha256": (
                "fedcba654321fedcba654321fedcba654321"
                "fedcba654321fedcba654321"
            ),
        },
        {
            "name": "cli-tool",
            "version": "1.2.0",
            "sha256": (
                "789ghi789ghi789ghi789ghi789ghi789ghi"
                "789ghi789ghi789ghi789ghi"
            ),
        },
    ]

    assert isinstance(
        artifacts_content, list
    ), f"{ARTIFACTS_JSON} must contain a JSON array"
    assert (
        artifacts_content == expected
    ), f"{ARTIFACTS_JSON} content does not match the expected initial state"


def test_schema_json_exists_and_contains_required_keys(schema_content):
    """
    The schema file should have the required keys and reference draft-07.
    Exact byte-for-byte equality is not enforced, but critical fields must
    be present so that later validation can succeed.
    """
    required_top_keys = {"$schema", "title", "type", "required", "properties"}
    missing = required_top_keys.difference(schema_content)
    assert (
        not missing
    ), f"{SCHEMA_JSON} is missing top-level keys: {', '.join(sorted(missing))}"

    assert (
        schema_content["$schema"] == "http://json-schema.org/draft-07/schema#"
    ), f"{SCHEMA_JSON} must declare draft-07 compatibility"

    # Ensure required property names
    required_fields = {"name", "version", "sha256"}
    assert set(schema_content.get("required", [])) == required_fields, (
        f"{SCHEMA_JSON} 'required' section must list "
        "'name', 'version', and 'sha256'"
    )


def test_output_files_do_not_exist_yet():
    """
    The student has not produced any output yet, so the filtered JSON and
    log file must be absent.
    """
    assert not FILTERED_JSON.exists(), (
        f"{FILTERED_JSON} should NOT exist before running the solution"
    )
    assert not FILTER_LOG.exists(), (
        f"{FILTER_LOG} should NOT exist before running the solution"
    )