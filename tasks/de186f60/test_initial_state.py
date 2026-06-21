# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state for the
# “People → Department” ETL exercise.  It checks only what should be
# present **before** the student starts working on the subtasks.
#
# Rules respected:
# • Uses only stdlib + pytest.
# • Tests absolute paths.
# • Does NOT touch/validate any of the files that must be generated later
#   (validation.log, employees_dept2.json, employee_counts.json).
# • Keeps failure messages explicit so students immediately know what is
#   missing or incorrect.

from pathlib import Path
import json
import pytest

BASE_DIR = Path("/home/user/data_pipeline")
EMPLOYEES_JSON = BASE_DIR / "employees.json"
SCHEMA_JSON = BASE_DIR / "employees_schema.json"


@pytest.fixture(scope="session")
def employees_content():
    """Return the raw text of employees.json"""
    try:
        return EMPLOYEES_JSON.read_text(encoding="utf-8")
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Missing file: {EMPLOYEES_JSON}")


@pytest.fixture(scope="session")
def schema_content():
    """Return the raw text of employees_schema.json"""
    try:
        return SCHEMA_JSON.read_text(encoding="utf-8")
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Missing file: {SCHEMA_JSON}")


def test_base_directory_exists():
    assert BASE_DIR.is_dir(), f"Required directory does not exist: {BASE_DIR}"


def test_employees_file_exists():
    assert EMPLOYEES_JSON.is_file(), f"Required file does not exist: {EMPLOYEES_JSON}"


def test_schema_file_exists():
    assert SCHEMA_JSON.is_file(), f"Required file does not exist: {SCHEMA_JSON}"


def test_employees_file_exact_content(employees_content):
    """
    Ensures employees.json matches the canonical content *exactly*,
    including whitespace and trailing newline.
    """
    expected = (
        "[\n"
        "  {\"id\": 1, \"name\": \"Alice\", \"department_id\": 1},\n"
        "  {\"id\": 2, \"name\": \"Bob\", \"department_id\": 2},\n"
        "  {\"id\": 3, \"name\": \"Carol\", \"department_id\": 2},\n"
        "  {\"id\": 4, \"name\": \"Dave\", \"department_id\": 3}\n"
        "]\n"
    )
    assert (
        employees_content == expected
    ), "employees.json content differs from the expected initial state."


def test_schema_file_exact_content(schema_content):
    """
    Ensures employees_schema.json matches the canonical content *exactly*,
    including whitespace and trailing newline.
    """
    expected = (
        "{\n"
        '  "$schema": "http://json-schema.org/draft-07/schema#",\n'
        '  "type": "array",\n'
        '  "items": {\n'
        '    "type": "object",\n'
        '    "required": ["id", "name", "department_id"],\n'
        '    "properties": {\n'
        '      "id": { "type": "integer" },\n'
        '      "name": { "type": "string" },\n'
        '      "department_id": { "type": "integer" }\n'
        '    },\n'
        '    "additionalProperties": false\n'
        "  }\n"
        "}\n"
    )
    assert (
        schema_content == expected
    ), "employees_schema.json content differs from the expected initial state."


def test_employees_json_is_valid_json(employees_content):
    """
    As a sanity check, ensure the file contains valid JSON and is the expected structure.
    This is a supplemental structural check in addition to the byte-for-byte comparison.
    """
    try:
        data = json.loads(employees_content)
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(f"employees.json is not valid JSON: {exc}")

    # Expecting a list of 4 dictionaries with the required keys.
    assert isinstance(data, list), "employees.json should contain a JSON array."
    assert len(data) == 4, "employees.json should contain exactly 4 employee records."

    required_keys = {"id", "name", "department_id"}
    for idx, item in enumerate(data, start=1):
        assert isinstance(item, dict), f"Record {idx} is not a JSON object."
        assert required_keys.issubset(
            item.keys()
        ), f"Record {idx} missing one of required keys {required_keys!r}."


def test_schema_json_is_valid_json(schema_content):
    """
    Ensures the schema file is valid JSON.  This does *not* attempt full
    JSON-Schema validation—just that it's valid JSON text.
    """
    try:
        json.loads(schema_content)
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(f"employees_schema.json is not valid JSON: {exc}")