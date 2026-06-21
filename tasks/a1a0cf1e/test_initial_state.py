# test_initial_state.py
"""
Pytest suite that validates the initial, pre-task state of the filesystem.

It verifies that:
1. Mandatory data files exist and contain the expected contents.
2. The JSON data actually match the numbers the grader will later assert.
3. The output directory exists and is completely empty.
4. Essential CLI tools (`jq` and at least one JSON-schema validator) are present
   somewhere on the PATH.

Failure messages are written to be explicit so that any deviation from the
required starting state is immediately obvious.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
OUTPUT_DIR = HOME / "output"
CHECKS_FILE = DATA_DIR / "uptime_checks.json"
SCHEMA_FILE = DATA_DIR / "uptime_schema.json"

# ---------- Helper functions -------------------------------------------------


def _load_json(path: Path):
    """Load and return JSON from *path*, raising with a helpful message if it fails."""
    try:
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        pytest.fail(f"Expected JSON file not found: {path}")
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path} is not valid JSON: {exc}")


def _which(cmd: str) -> bool:
    """Return True if *cmd* is resolvable on the PATH."""
    from shutil import which

    return which(cmd) is not None


# ---------- Tests ------------------------------------------------------------


def test_data_files_exist():
    """Both source JSON files must be present."""
    assert CHECKS_FILE.is_file(), f"Missing data file: {CHECKS_FILE}"
    assert SCHEMA_FILE.is_file(), f"Missing schema file: {SCHEMA_FILE}"


def test_output_directory_is_empty():
    """/home/user/output must exist and be empty before the student runs anything."""
    assert OUTPUT_DIR.is_dir(), f"Output directory missing: {OUTPUT_DIR}"
    contents = list(OUTPUT_DIR.iterdir())
    assert (
        not contents
    ), f"Output directory is expected to be empty, but contains: {contents}"


def test_uptime_checks_contents_and_stats():
    """
    The JSON data must be exactly the 5-element array described in the task.
    Additionally, the pre-computed statistics that the grader relies on
    (total_checks=5, failed_checks=2, average_response_time_ms=202) must match.
    """
    data = _load_json(CHECKS_FILE)

    # The root must be a list of exactly 5 items.
    assert isinstance(
        data, list
    ), f"{CHECKS_FILE} must contain a JSON array, got {type(data).__name__}"
    assert (
        len(data) == 5
    ), f"{CHECKS_FILE} must contain exactly 5 check objects, found {len(data)}"

    required_keys = {"service_name", "status", "response_time_ms"}
    statuses_allowed = {"OK", "FAIL"}

    for idx, item in enumerate(data):
        assert isinstance(
            item, dict
        ), f"Element #{idx} in {CHECKS_FILE} is not a JSON object"
        missing = required_keys - item.keys()
        assert (
            not missing
        ), f"Element #{idx} is missing properties: {sorted(missing)}"
        extra = set(item.keys()) - required_keys
        assert (
            not extra
        ), f"Element #{idx} has unexpected properties: {sorted(extra)}"

        status = item["status"]
        assert status in statuses_allowed, (
            f'Element #{idx} has invalid "status": {status!r}; '
            f"allowed: {sorted(statuses_allowed)}"
        )

        rt = item["response_time_ms"]
        assert isinstance(
            rt, (int, float)
        ), f'Element #{idx} "response_time_ms" must be a number, got {type(rt).__name__}'
        assert (
            rt >= 0
        ), f'Element #{idx} "response_time_ms" must be non-negative, got {rt}'

    # Calculate statistics and verify against the truth values.
    total_checks = len(data)
    failed_checks = sum(1 for item in data if item["status"] != "OK")
    avg_rt = round(sum(item["response_time_ms"] for item in data) / total_checks)

    assert (
        total_checks == 5
    ), f"Expected total_checks=5, got {total_checks}"
    assert (
        failed_checks == 2
    ), f"Expected failed_checks=2, got {failed_checks}"
    assert (
        avg_rt == 202
    ), f"Expected average_response_time_ms=202, got {avg_rt}"


@pytest.mark.parametrize(
    "binary",
    [
        "jq",  # mandatory per the task
        # at least one of these JSON-schema validators must be available
        "jsonschema",
        "check-jsonschema",
        "ajv",
    ],
)
def test_required_cli_tools(binary):
    """Verify that `jq` and at least one JSON-schema validator are on PATH."""
    if binary == "jq":
        assert _which("jq"), "`jq` executable is required but not found on PATH"
    else:
        # We need *any* validator; collect hits.
        if not hasattr(test_required_cli_tools, "_validator_found"):
            test_required_cli_tools._validator_found = False  # type: ignore
        if _which(binary):
            test_required_cli_tools._validator_found = True  # type: ignore

    # After parametrization ends, assert that we found at least one validator.
    if binary == "ajv":
        assert getattr(
            test_required_cli_tools, "_validator_found", False  # type: ignore
        ), (
            "None of the expected CLI JSON-schema validators "
            "(`jsonschema`, `check-jsonschema`, or `ajv`) was found on PATH"
        )