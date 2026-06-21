# test_initial_state.py
#
# This pytest suite validates the initial operating-system / filesystem state
# **before** the learner begins the exercise.  It asserts only those conditions
# that must already be true and does NOT reference any files or directories
# that are supposed to be created by the learner’s solution.

import json
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the expected initial state
# --------------------------------------------------------------------------- #

API_RESPONSES_DIR = Path("/home/user/api_responses")
ORDERS_JSON_PATH = API_RESPONSES_DIR / "orders.json"

# The exact data structure we expect once the JSON is parsed.
EXPECTED_ORDERS = [
    {"order_id": 1001, "customer_id": "C001", "total": 123.45, "status": "shipped"},
    {"order_id": 1002, "customer_id": "C002", "total": 67.89, "status": "processing"},
    {"order_id": 1003, "customer_id": "C003", "total": 250.0,  "status": "delivered"},
]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_api_responses_directory_exists():
    """
    The directory /home/user/api_responses must already exist.
    """
    assert API_RESPONSES_DIR.exists(), (
        f"Required directory missing: {API_RESPONSES_DIR}. "
        "It should contain the JSON payload used for the exercise."
    )
    assert API_RESPONSES_DIR.is_dir(), (
        f"{API_RESPONSES_DIR} exists but is not a directory."
    )


def test_orders_json_exists_and_valid():
    """
    The JSON file with sample order data must exist *before* the task starts and
    must contain exactly the expected records (order & field values).
    """
    # --- File presence checks ------------------------------------------------
    assert ORDERS_JSON_PATH.exists(), (
        f"Required file missing: {ORDERS_JSON_PATH}. "
        "The exercise cannot proceed without this sample response payload."
    )
    assert ORDERS_JSON_PATH.is_file(), (
        f"{ORDERS_JSON_PATH} exists but is not a regular file."
    )

    # --- Content checks ------------------------------------------------------
    try:
        with ORDERS_JSON_PATH.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{ORDERS_JSON_PATH} is not valid JSON: {exc}")

    # Ensure the parsed JSON is exactly what we expect.
    assert data == EXPECTED_ORDERS, (
        f"The contents of {ORDERS_JSON_PATH} do not match the expected data.\n"
        "Expected:\n"
        f"{json.dumps(EXPECTED_ORDERS, indent=2)}\n\n"
        "Found:\n"
        f"{json.dumps(data, indent=2)}"
    )