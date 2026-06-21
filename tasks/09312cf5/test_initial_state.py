# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system / filesystem
# state for the “Investigate Expensive Running Cloud Instances via Curl” task.
#
# It purposefully checks ONLY the resources that must already exist **before**
# the student performs any action.  It **does not** check for the output files
# the student is expected to create later.
#
# What is validated:
#   1. /home/user/mock_api   must be an existing directory
#   2. /home/user/mock_api/costs.json   must exist and contain the exact,
#      expected JSON payload.
#   3. The JSON must parse correctly and follow the documented structure.
#   4. The “curl” executable must be available in $PATH (the student is asked
#      to use it, so it should exist).
#
# Only stdlib and pytest are used, per the instructions.

import json
import os
import shutil
from pathlib import Path

import pytest


MOCK_API_DIR = Path("/home/user/mock_api")
COSTS_JSON = MOCK_API_DIR / "costs.json"

# The canonical payload that must already be present in costs.json
EXPECTED_COSTS_PAYLOAD = {
    "instances": [
        {"id": "i-07bd", "state": "running", "hourly_cost": 0.12},
        {"id": "i-18ef", "state": "running", "hourly_cost": 0.45},
        {"id": "i-21aa", "state": "stopped", "hourly_cost": 0.37},
        {"id": "i-3cb2", "state": "running", "hourly_cost": 0.31},
        {"id": "i-4ddc", "state": "running", "hourly_cost": 0.29},
    ]
}


def test_mock_api_directory_exists():
    """The mock API directory must pre-exist."""
    assert MOCK_API_DIR.is_dir(), (
        f"Required directory {MOCK_API_DIR} is missing. "
        "The task assumes this directory already exists."
    )


def test_costs_json_exists():
    """The costs.json file must be present."""
    assert COSTS_JSON.is_file(), (
        f"Required file {COSTS_JSON} is missing. "
        "The task cannot proceed without this mock endpoint payload."
    )


@pytest.fixture(scope="module")
def parsed_costs_json():
    """Load and return the JSON content of costs.json."""
    try:
        with COSTS_JSON.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{COSTS_JSON} is not valid JSON: {exc}")


def test_costs_json_structure(parsed_costs_json):
    """Ensure the JSON structure matches the documented schema."""
    assert isinstance(
        parsed_costs_json, dict
    ), f"Expected a JSON object at top level in {COSTS_JSON}"
    assert "instances" in parsed_costs_json, (
        f"Key 'instances' missing from {COSTS_JSON}. "
        "The grader expects this exact key."
    )
    assert isinstance(
        parsed_costs_json["instances"], list
    ), f"Key 'instances' must map to a JSON array in {COSTS_JSON}"


def test_costs_json_exact_payload(parsed_costs_json):
    """The payload must be byte-for-byte identical to the specification."""
    assert parsed_costs_json == EXPECTED_COSTS_PAYLOAD, (
        f"The contents of {COSTS_JSON} differ from the expected fixture. "
        "Ensure the file has not been modified."
    )


def test_curl_available():
    """The curl executable must be available in PATH."""
    curl_path = shutil.which("curl")
    assert curl_path is not None, (
        "'curl' is required for this exercise but was not found in $PATH."
    )