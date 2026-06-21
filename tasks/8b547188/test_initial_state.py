# test_initial_state.py
#
# Pytest suite to assert the correctness of the starting filesystem / OS
# state for the “Filter High-Priority Open Tickets with jq and Validate JSON
# Schema” exercise.
#
# DO NOT MODIFY THIS FILE DURING GRADING.
#
# ‑ Uses only Python’s stdlib + pytest.
# ‑ Verifies that all prerequisite files, directories and tools exist.
# ‑ Confirms that support_tickets.json already satisfies ticket_schema.json,
#   so the expected grader verdict in part A is “VALID”.

import json
import os
import pathlib
import shutil
import stat

import pytest

HOME = pathlib.Path("/home/user")
DATA_DIR = HOME / "data"
TICKETS_FILE = DATA_DIR / "support_tickets.json"
SCHEMA_FILE = DATA_DIR / "ticket_schema.json"


# --------------------------------------------------------------------------- #
# Helper functions                                                             #
# --------------------------------------------------------------------------- #
def load_json(path: pathlib.Path):
    """Load JSON from *path* and raise a helpful assertion message on failure."""
    try:
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Required file not found: {path}")
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(f"File '{path}' is not valid JSON: {exc}")


def validate_against_schema(data, schema):
    """
    A minimal, purpose-built validator that enforces exactly the constraints
    present in ticket_schema.json shipped with the task.  No external
    libraries are used so that the test remains stdlib-only.
    """
    # 1. Root must be a list
    assert isinstance(data, list), "Top-level JSON must be an array"

    # Extract schema rules
    item_schema = schema.get("items", {})
    required_keys = set(item_schema.get("required", []))
    props = item_schema.get("properties", {})
    allowed_keys = set(props)

    # Enumerations
    status_enum = set(props.get("status", {}).get("enum", []))
    priority_enum = set(props.get("priority", {}).get("enum", []))

    for idx, ticket in enumerate(data):
        assert isinstance(
            ticket, dict
        ), f"Item at position {idx} is not an object (dict)"

        # Required keys present?
        missing = required_keys - ticket.keys()
        assert (
            not missing
        ), f"Ticket at index {idx} missing required keys: {sorted(missing)}"

        # No additional properties?
        extra = set(ticket) - allowed_keys
        assert (
            not extra
        ), f"Ticket at index {idx} contains unknown keys: {sorted(extra)}"

        # Validate types
        for key in required_keys:
            assert isinstance(
                ticket[key], str
            ), f"Ticket at index {idx}: key '{key}' must be a string"

        # Enum checks
        status = ticket["status"]
        priority = ticket["priority"]

        assert (
            status in status_enum
        ), f"Ticket at index {idx}: status '{status}' not in {sorted(status_enum)}"
        assert (
            priority in priority_enum
        ), f"Ticket at index {idx}: priority '{priority}' not in {sorted(priority_enum)}"


# --------------------------------------------------------------------------- #
# Tests                                                                        #
# --------------------------------------------------------------------------- #
def test_data_directory_exists():
    assert DATA_DIR.is_dir(), f"Expected directory missing: {DATA_DIR}"


@pytest.mark.parametrize(
    "path_desc, path",
    [
        ("support tickets JSON", TICKETS_FILE),
        ("ticket schema JSON", SCHEMA_FILE),
    ],
)
def test_required_files_exist_and_are_readable(path_desc, path):
    assert path.exists(), f"Missing required {path_desc} file: {path}"
    # Basic read permission check
    st = path.stat()
    assert bool(
        st.st_mode & stat.S_IRUSR
    ), f"{path} is not readable; permissions are {oct(st.st_mode)}"


def test_jq_is_installed_and_on_path():
    jq_path = shutil.which("jq")
    assert jq_path is not None, (
        "The 'jq' executable is required but was not found on PATH. "
        "Ensure it is installed and PATH is correctly set."
    )


def test_support_tickets_are_valid_against_schema():
    """
    Confirms that /home/user/data/support_tickets.json already complies with
    /home/user/data/ticket_schema.json.  The student should therefore write
    'VALID' to the schema_validation.txt file.
    """
    data = load_json(TICKETS_FILE)
    schema = load_json(SCHEMA_FILE)
    # Will raise an assertion (failing the test) if invalid:
    validate_against_schema(data, schema)