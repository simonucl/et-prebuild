# test_initial_state.py
#
# Pytest suite that verifies the *initial* filesystem state for the
# “API regression-test” exercise.  These tests **must** pass *before*
# the student starts working on the task.  Any failure indicates that
# the provided starting point is incorrect or has been modified.

import json
import os
from pathlib import Path

# ---- constants ----------------------------------------------------------------

BASE_DIR           = Path("/home/user/projects/api-test").resolve()
INPUT_DIR          = BASE_DIR / "input"
OUTPUT_DIR         = BASE_DIR / "output"
SCHEMA_DIR         = BASE_DIR / "schema"
SCHEMA_FILE        = SCHEMA_DIR / "user.schema.json"

INPUT_FILES        = {
    "user1.json": {
        "id": 101,
        "name": "Alice Smith",
        "email": "alice@example.com",
        "isActive": True,
    },
    "user2.json": {
        "id": 102,
        "name": "Bob Jones",
        "isActive": False,
    },
}

OUTPUT_ARTIFACTS   = {
    "validation.log",
    "valid_users.json",
    "summary.txt",
}

# ------------------------------------------------------------------------------
# helper
# ------------------------------------------------------------------------------

def read_json(path: Path):
    """Load JSON file *exactly* as a Python object."""
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)

# ------------------------------------------------------------------------------
# tests
# ------------------------------------------------------------------------------

def test_base_directories_exist_and_are_directories():
    assert BASE_DIR.is_dir(), (
        f"Expected base directory {BASE_DIR} to exist and be a directory."
    )
    assert INPUT_DIR.is_dir(), (
        f"Expected input directory {INPUT_DIR} to exist and be a directory."
    )
    assert OUTPUT_DIR.is_dir(), (
        f"Expected output directory {OUTPUT_DIR} to exist and be a directory."
    )
    assert SCHEMA_DIR.is_dir(), (
        f"Expected schema directory {SCHEMA_DIR} to exist and be a directory."
    )


def test_output_directory_is_empty():
    entries = [p for p in OUTPUT_DIR.iterdir() if not p.name.startswith(".")]
    assert not entries, (
        f"Output directory {OUTPUT_DIR} is expected to be empty before the "
        f"student starts, but contains: {', '.join(e.name for e in entries)}"
    )


def test_expected_input_files_exist_and_no_extras():
    actual_files   = sorted(p.name for p in INPUT_DIR.glob("*.json"))
    expected_files = sorted(INPUT_FILES.keys())

    assert actual_files == expected_files, (
        "Mismatch in input JSON files.\n"
        f"  Expected: {expected_files}\n"
        f"  Found   : {actual_files}"
    )


def test_input_file_contents_are_exact():
    for filename, expected_obj in INPUT_FILES.items():
        path = INPUT_DIR / filename
        assert path.is_file(), f"Missing required input file: {path}"
        try:
            actual_obj = read_json(path)
        except json.JSONDecodeError as e:
            raise AssertionError(
                f"File {path} contains invalid JSON: {e}"
            ) from e

        assert actual_obj == expected_obj, (
            f"JSON content mismatch in {path}.\n"
            f"  Expected object: {expected_obj}\n"
            f"  Actual object  : {actual_obj}"
        )


def test_schema_file_does_not_exist_yet():
    assert not SCHEMA_FILE.exists(), (
        f"The schema file {SCHEMA_FILE} should NOT exist before the student "
        f"creates it, but it is already present."
    )


def test_no_output_artifacts_exist_yet():
    for artifact in OUTPUT_ARTIFACTS:
        path = OUTPUT_DIR / artifact
        assert not path.exists(), (
            f"Artifact {path} should NOT exist yet.  The directory {OUTPUT_DIR} "
            f"must be empty before the student runs their solution."
        )