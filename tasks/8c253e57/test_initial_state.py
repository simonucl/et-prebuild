# test_initial_state.py
#
# This test-suite validates the *initial* on-disk state that must exist
# BEFORE the student begins working on the exercise “Profiling hot-spots”.
#
# It checks that:
#   • The directory /home/user/app_profiling exists.
#   • Exactly the two source files (and no outputs) are present.
#   • profile_schema.json contains the expected JSON-Schema draft-07 document.
#   • raw_profile.json contains the expected profiling payload.
#
# If any assertion fails the test output will clearly describe what is
# missing or differs from the required initial state.
#
# NOTE: Only Python’s stdlib and pytest are used – no third-party deps.

import json
from pathlib import Path
import pytest

APP_DIR = Path("/home/user/app_profiling")
SCHEMA_FILE = APP_DIR / "profile_schema.json"
RAW_FILE = APP_DIR / "raw_profile.json"
VALIDATION_LOG = APP_DIR / "validation.log"
HOTSPOTS_FILE = APP_DIR / "hotspots.json"


@pytest.fixture(scope="module")
def dir_listing():
    """Return a list of the entries (names only) in the profiling directory."""
    assert APP_DIR.exists() and APP_DIR.is_dir(), (
        f"Directory {APP_DIR} must exist and be a directory."
    )
    return sorted(p.name for p in APP_DIR.iterdir())


def test_expected_files_present(dir_listing):
    """The directory must contain exactly the two initial JSON files."""
    expected = {"profile_schema.json", "raw_profile.json"}
    assert set(dir_listing) == expected, (
        f"{APP_DIR} must contain only {sorted(expected)}, "
        f"but currently has: {dir_listing}"
    )


def test_no_result_files_yet():
    """validation.log and hotspots.json must NOT exist yet."""
    assert not VALIDATION_LOG.exists(), (
        f"{VALIDATION_LOG} should NOT exist before the student runs any command."
    )
    assert not HOTSPOTS_FILE.exists(), (
        f"{HOTSPOTS_FILE} should NOT exist before the student runs any command."
    )


def test_profile_schema_contents():
    """Verify that the JSON-Schema file matches the spec given in the task statement."""
    try:
        data = json.loads(SCHEMA_FILE.read_text())
    except FileNotFoundError:
        pytest.fail(f"Required file {SCHEMA_FILE} not found.")
    except json.JSONDecodeError as exc:
        pytest.fail(f"{SCHEMA_FILE} is not valid JSON: {exc}")

    # Check top-level keys
    assert data.get("$schema") == "http://json-schema.org/draft-07/schema#", (
        "profile_schema.json must declare draft-07 schema."
    )
    assert data.get("type") == "array", "Top-level type must be 'array'."

    # Check item definition
    items = data.get("items")
    assert isinstance(items, dict) and items.get("type") == "object", (
        "'items' must be an object schema describing each element."
    )

    required = set(items.get("required", []))
    assert required == {"function", "calls", "avg_ms"}, (
        "'required' must exactly list 'function', 'calls', 'avg_ms'."
    )

    props = items.get("properties", {})
    for key, expected_type in {
        "function": "string",
        "calls": "integer",
        "avg_ms": "number",
    }.items():
        assert props.get(key, {}).get("type") == expected_type, (
            f"Property '{key}' must have type '{expected_type}'."
        )

    assert items.get("additionalProperties") is False, (
        "'additionalProperties' must be false."
    )
    assert data.get("minItems") == 1, "'minItems' must be 1."


def test_raw_profile_json_contents():
    """Verify that raw_profile.json contains the exact 5 profiling entries."""
    try:
        entries = json.loads(RAW_FILE.read_text())
    except FileNotFoundError:
        pytest.fail(f"Required file {RAW_FILE} not found.")
    except json.JSONDecodeError as exc:
        pytest.fail(f"{RAW_FILE} is not valid JSON: {exc}")

    assert isinstance(entries, list), "raw_profile.json must be a JSON array."
    assert len(entries) == 5, "raw_profile.json must contain exactly 5 elements."

    expected_entries = [
        {"function": "core.init",      "calls": 1,  "avg_ms": 5.0},
        {"function": "engine.render",  "calls": 90, "avg_ms": 12.4},
        {"function": "engine.update",  "calls": 90, "avg_ms": 15.8},
        {"function": "engine.physics", "calls": 90, "avg_ms": 7.1},
        {"function": "core.cleanup",   "calls": 1,  "avg_ms": 3.2},
    ]

    # We compare dictionaries disregarding key order but preserving
    # multiset semantics (same elements, possibly different order).
    def normalize(lst):
        """Return list of dicts sorted by 'function' for deterministic compare."""
        return sorted(lst, key=lambda d: d["function"])

    assert normalize(entries) == normalize(expected_entries), (
        "raw_profile.json contents do not match the expected initial payload."
    )