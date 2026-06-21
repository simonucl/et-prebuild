# test_initial_state.py
#
# Pytest suite that validates the state of the operating system / filesystem
# BEFORE the student starts working on the compliance-log task.

import json
from pathlib import Path
import pytest

HOME = Path("/home/user")
SCHEMA_FILE = HOME / "data" / "schema" / "system_config.schema.json"
AUDIT_DIR = HOME / "data" / "audit"

REQUIRED_KEYS = ["hostname", "os_version", "patch_level", "encryption_enabled"]
EXPECTED_TYPES = {
    "hostname": str,
    "os_version": str,
    "patch_level": int,              # must be int and NOT bool
    "encryption_enabled": bool,
}

# --------------------------------------------------
# Helper utilities
# --------------------------------------------------
def validate_config(data):
    """
    Perform the minimal validation described in the task:
    - presence of all REQUIRED_KEYS
    - correct primitive JSON types
    Returns a tuple: (is_pass: bool, error_keys: list[str])
    """
    errors = []

    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(key)
            continue

        value = data[key]
        expected_type = EXPECTED_TYPES[key]
        # Special handling because `bool` is a subclass of `int` in Python
        if key == "patch_level":
            if isinstance(value, bool) or not isinstance(value, int):
                errors.append(key)
        elif not isinstance(value, expected_type):
            errors.append(key)

    return (len(errors) == 0), errors


# --------------------------------------------------
# Tests for filesystem structure
# --------------------------------------------------
def test_schema_file_exists():
    assert SCHEMA_FILE.exists(), f"Missing schema file at {SCHEMA_FILE}"
    assert SCHEMA_FILE.is_file(), f"{SCHEMA_FILE} exists but is not a regular file"


def test_schema_contents_min_requirements():
    with SCHEMA_FILE.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)

    # Validate that the schema at least lists the required keys correctly
    required = schema.get("required", [])
    assert required == REQUIRED_KEYS, (
        "Schema 'required' array does not match expected keys "
        f"(found {required}, expected {REQUIRED_KEYS})"
    )

    props = schema.get("properties", {})
    missing_props = [k for k in REQUIRED_KEYS if k not in props]
    assert not missing_props, (
        "Schema 'properties' section missing keys: " + ", ".join(missing_props)
    )

    # Type assertions for each property
    for key, py_type in EXPECTED_TYPES.items():
        prop_type = props[key].get("type")
        expected_json_type = (
            "integer" if py_type is int else
            "boolean" if py_type is bool else
            "string"
        )
        assert prop_type == expected_json_type, (
            f"Schema type mismatch for '{key}': expected '{expected_json_type}', "
            f"found '{prop_type}'"
        )


def test_audit_directory_exists():
    assert AUDIT_DIR.exists(), f"Missing audit directory at {AUDIT_DIR}"
    assert AUDIT_DIR.is_dir(), f"{AUDIT_DIR} exists but is not a directory"


def test_expected_json_files_exist():
    expected_files = ["system1.json", "system2.json", "system3.json"]
    for fname in expected_files:
        fpath = AUDIT_DIR / fname
        assert fpath.exists(), f"Expected audit file {fpath} is missing"
        assert fpath.is_file(), f"{fpath} exists but is not a regular file"


# --------------------------------------------------
# Tests for initial compliance status of each JSON file
# --------------------------------------------------
@pytest.mark.parametrize(
    "filename, should_pass, expected_error_keys",
    [
        ("system1.json", True,  []),
        ("system2.json", False, ["patch_level", "encryption_enabled"]),
        ("system3.json", False, ["hostname"]),
    ],
)
def test_individual_config_validation(filename, should_pass, expected_error_keys):
    """
    Ensures that the initial JSON files match the truth table provided
    in the task description.  This guards against accidental changes
    to the fixture data.
    """
    fpath = AUDIT_DIR / filename
    with fpath.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    is_pass, error_keys = validate_config(data)

    assert is_pass == should_pass, (
        f"{filename} validation mismatch: expected PASS={should_pass} but "
        f"got PASS={is_pass}. Errors: {error_keys}"
    )
    assert error_keys == expected_error_keys, (
        f"{filename} error-key list mismatch: expected {expected_error_keys} "
        f"but got {error_keys}"
    )