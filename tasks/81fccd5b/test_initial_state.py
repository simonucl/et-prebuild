# test_initial_state.py
#
# This test-suite validates that the starting filesystem state
# (BEFORE the student performs any actions) matches the specification
# for the “API-response filtering” task.
#
# What we assert here:
#   • /home/user/api_responses/orders.json exists and its *exact* text
#     matches the reference provided in the assignment.
#   • /home/user/output/ exists, is a directory, is writable and is empty.
#
# Nothing about the to-be-created artefacts (/home/user/order_schema.json,
# valid_orders.json, validation.log, …) is tested here, because they do
# not have to exist yet.
#
# The tests use only Python’s standard library and pytest.

import os
from pathlib import Path
import stat
import pytest

ORDERS_PATH = Path("/home/user/api_responses/orders.json")
OUTPUT_DIR  = Path("/home/user/output")


# --------------------------------------------------------------------------- #
# Reference content of orders.json exactly as given in the specification
# (including whitespace and the single trailing newline).
# --------------------------------------------------------------------------- #
EXPECTED_ORDERS_CONTENT = (
    '[\n'
    '  {\n'
    '    "id": 3,\n'
    '    "customer_name": "Alice Smith",\n'
    '    "total": 129.99,\n'
    '    "items": ["SKU_123", "SKU_456"]\n'
    '  },\n'
    '  {\n'
    '    "id": -7,\n'
    '    "customer_name": "Bob Jones",\n'
    '    "total": 59.00,\n'
    '    "items": ["SKU_789"]\n'
    '  },\n'
    '  {\n'
    '    "id": 2,\n'
    '    "customer_name": "Charlie Doe",\n'
    '    "items": ["SKU_111", "SKU_222"]\n'
    '  },\n'
    '  {\n'
    '    "id": 5,\n'
    '    "customer_name": "Dana Roe",\n'
    '    "total": 0,\n'
    '    "items": ["SKU_333"]\n'
    '  },\n'
    '  {\n'
    '    "id": 4,\n'
    '    "customer_name": "Evan Poe",\n'
    '    "total": -10.50,\n'
    '    "items": ["SKU_444", "SKU_555"]\n'
    '  }\n'
    ']\n'
)


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def is_writable(dir_path: Path) -> bool:
    """Return True if the current user can create a file in dir_path."""
    return os.access(dir_path, os.W_OK | os.X_OK)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_orders_json_exists_and_is_file():
    assert ORDERS_PATH.exists(), (
        f"Required file not found: {ORDERS_PATH}"
    )
    assert ORDERS_PATH.is_file(), (
        f"Expected a regular file at {ORDERS_PATH}, "
        f"but something else was found."
    )


def test_orders_json_content_exact():
    content = ORDERS_PATH.read_text(encoding="utf-8")
    assert content == EXPECTED_ORDERS_CONTENT, (
        "The contents of /home/user/api_responses/orders.json do not match "
        "the expected reference file. Ensure the file is unmodified and "
        "contains the exact whitespace and trailing newline specified."
    )


def test_output_directory_state():
    assert OUTPUT_DIR.exists(), (
        f"Output directory {OUTPUT_DIR} does not exist."
    )
    assert OUTPUT_DIR.is_dir(), (
        f"{OUTPUT_DIR} exists but is not a directory."
    )
    # The directory must be empty at task start.
    entries = list(OUTPUT_DIR.iterdir())
    assert not entries, (
        f"Output directory {OUTPUT_DIR} is expected to be empty before the "
        f"task begins, but contains: {[p.name for p in entries]}"
    )
    # And it must be writable by the current user.
    assert is_writable(OUTPUT_DIR), (
        f"Output directory {OUTPUT_DIR} is not writable by the current user."
    )