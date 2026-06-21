# test_initial_state.py
#
# Pytest suite that asserts the *initial* filesystem state for the
# “performance-metric” assignment.  These tests must pass **before**
# the student performs any actions.  They guarantee that the autograder
# starts from a known good baseline.

import json
import os
import stat
from pathlib import Path

import pytest

# ----------------------------------------------------------------------
# Constant paths
# ----------------------------------------------------------------------
HOME = Path("/home/user")
BASE_DIR = HOME / "app" / "metrics"
RAW_DIR = BASE_DIR / "raw"
SCHEMA_FILE = BASE_DIR / "schema.json"
PROCESSED_DIR = BASE_DIR / "processed"

EXPECTED_RAW_FILES = {
    "metric1.json",
    "metric2.json",
    "metric3_bad.json",
}

# Expected JSON payloads in the raw files
EXPECTED_METRIC_CONTENT = {
    "metric1.json": {
        "timestamp": 1680000000,
        "cpu": 45.5,
        "mem": 62.3,
        "req_per_sec": 850,
    },
    "metric2.json": {
        "timestamp": 1680000600,
        "cpu": 52.0,
        "mem": 70.1,
        "req_per_sec": 920,
    },
    "metric3_bad.json": {
        "timestamp": "1680001200",
        "cpu": 47.2,
        "mem": 65.0,
    },
}


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _load_json(p: Path):
    with p.open(encoding="utf-8") as fh:
        return json.load(fh)


def _assert_writeable(p: Path):
    """Ensure the file/dir is writeable by its owner (no super-user needed)."""
    st_mode = p.stat().st_mode
    assert st_mode & stat.S_IWUSR, f"{p} is not writeable by its owner."


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
def test_directory_layout_exists():
    """Required top-level directories must exist."""
    assert BASE_DIR.is_dir(), f"Missing directory: {BASE_DIR}"
    assert RAW_DIR.is_dir(), f"Missing directory: {RAW_DIR}"
    assert SCHEMA_FILE.is_file(), f"Missing schema file: {SCHEMA_FILE}"


def test_processed_directory_absent_initially():
    """The ‘processed/’ directory must NOT exist before the student runs their solution."""
    assert not PROCESSED_DIR.exists(), (
        f"Directory {PROCESSED_DIR} should not exist yet; "
        "the student must create it."
    )


def test_raw_directory_file_set():
    """No more and no fewer than the three expected metric files must be present."""
    found = {p.name for p in RAW_DIR.iterdir() if p.is_file()}
    assert (
        found == EXPECTED_RAW_FILES
    ), f"Files in {RAW_DIR} differ from expected.\nExpected: {EXPECTED_RAW_FILES}\nFound   : {found}"


def test_schema_file_content():
    """Verify that schema.json contains the expected structure."""
    data = _load_json(SCHEMA_FILE)

    # Top-level keys
    expected_keys = {
        "$schema",
        "title",
        "type",
        "required",
        "properties",
        "additionalProperties",
    }
    assert set(data.keys()) == expected_keys, (
        f"{SCHEMA_FILE} top-level keys differ from expected.\n"
        f"Expected: {expected_keys}\nFound   : {set(data.keys())}"
    )

    # Property names
    expected_props = {"timestamp", "cpu", "mem", "req_per_sec"}
    props = data["properties"]
    assert set(props.keys()) == expected_props, (
        f"Schema ‘properties’ keys are wrong.\nExpected: {expected_props}\nFound   : {set(props.keys())}"
    )

    # Basic type checks inside properties (light touch, not full schema validation)
    assert props["timestamp"]["type"] == "integer"
    assert props["cpu"]["type"] == "number"
    assert props["mem"]["type"] == "number"
    assert props["req_per_sec"]["type"] == "integer"
    # Ensure additionalProperties is explicitly disabled
    assert data["additionalProperties"] is False, "Schema must disallow additional properties."


def test_raw_file_contents_exact():
    """Ensure each raw metric file is byte-for-byte as described in the spec."""
    for filename, expected_json in EXPECTED_METRIC_CONTENT.items():
        path = RAW_DIR / filename
        assert path.is_file(), f"Expected file {path} to exist."
        found_json = _load_json(path)
        assert (
            found_json == expected_json
        ), f"Contents of {path} differ from what the spec describes."


def test_files_are_owner_writeable():
    """Every pre-created file should be owner-writeable (no sudo required)."""
    # Check schema.json + every raw file
    paths = [SCHEMA_FILE] + [RAW_DIR / fn for fn in EXPECTED_RAW_FILES]
    for p in paths:
        _assert_writeable(p)