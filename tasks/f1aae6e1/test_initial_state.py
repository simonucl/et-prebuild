# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem and data state
# that must be present **before** the learner performs any actions.
#
# It intentionally does NOT check for the existence (or absence) of
# the artefacts the learner is required to create later on.
#
# Only the Python standard library and pytest are used.

import json
from pathlib import Path

RAW_DIR = Path("/home/user/cloud_costs/raw")
SCHEMA_DIR = Path("/home/user/cloud_costs/schema")

RAW_FILE = RAW_DIR / "weekly_costs.json"
SCHEMA_FILE = SCHEMA_DIR / "cloud_cost_report.schema.json"


def test_raw_directory_exists():
    assert RAW_DIR.is_dir(), (
        f"Required directory {RAW_DIR} is missing. "
        "The raw cost data must be placed here."
    )


def test_schema_directory_exists():
    assert SCHEMA_DIR.is_dir(), (
        f"Required directory {SCHEMA_DIR} is missing. "
        "The JSON-Schema must be placed here."
    )


def test_weekly_costs_json_file_exists_and_is_readable():
    assert RAW_FILE.is_file(), (
        f"Expected raw cost report file {RAW_FILE} is missing."
    )
    try:
        RAW_FILE.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        assert False, (
            f"Could not read {RAW_FILE}: {exc}"
        )


def test_cloud_cost_schema_file_exists_and_is_readable():
    assert SCHEMA_FILE.is_file(), (
        f"Expected JSON-Schema file {SCHEMA_FILE} is missing."
    )
    try:
        SCHEMA_FILE.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        assert False, (
            f"Could not read {SCHEMA_FILE}: {exc}"
        )


def test_weekly_costs_json_structure():
    """
    The raw file must be a JSON array of objects.  Each object must have at
    least the keys required by the downstream tooling.  Additionally, ensure
    there is at least one item whose cost is > 1000 and currency == 'USD'
    so that the learner can actually filter something.
    """
    data = json.loads(RAW_FILE.read_text(encoding="utf-8"))

    assert isinstance(data, list), (
        f"{RAW_FILE} must contain a JSON array at the top level."
    )
    assert data, f"{RAW_FILE} contains an empty array; need at least one record."

    required_keys = {"account_id", "service", "cost", "currency", "week"}

    for idx, item in enumerate(data):
        assert isinstance(item, dict), (
            f"Element {idx} in {RAW_FILE} is not a JSON object."
        )
        missing = required_keys - item.keys()
        assert not missing, (
            f"Element {idx} in {RAW_FILE} is missing keys: {', '.join(sorted(missing))}"
        )

    qualifying = [
        item for item in data
        if isinstance(item.get("cost"), (int, float))
        and item["cost"] > 1000
        and item["currency"] == "USD"
    ]
    assert qualifying, (
        f"{RAW_FILE} must contain at least one line-item with cost > 1000 "
        "and currency == 'USD' so that filtering produces output."
    )


def test_schema_json_is_valid_json():
    """
    The schema file must parse as valid JSON.  We do NOT validate the schema
    itself (that would require non-stdlib packages), only that it is well-formed
    JSON and has basic characteristics expected by downstream tooling.
    """
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    assert isinstance(schema, dict), (
        f"{SCHEMA_FILE} must contain a JSON object at the top level."
    )
    # A minimal sanity check on common JSON-Schema properties
    assert schema.get("type") == "array", (
        f"{SCHEMA_FILE} should declare 'type': 'array' at top level."
    )