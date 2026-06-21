# test_initial_state.py
#
# Pytest test-suite that validates the *initial* filesystem/OS state
# before the student starts working on the task.  All checks are
# limited to the resources that must already exist; we purposely do
# NOT look for any of the files that the student will create later
# (e.g. build_validation.log, artifact_names.txt).
#
# Only the Python standard-library and pytest are used.

import json
import os
import re
from pathlib import Path

BUILD_DIR = Path("/home/user/build")
ARTIFACTS_JSON = BUILD_DIR / "artifacts.json"
SCHEMA_JSON = BUILD_DIR / "artifact_schema.json"

# ----------------------------------------------------------------------
# Helper data expected to be found on disk
# ----------------------------------------------------------------------

EXPECTED_ARTIFACTS = [
    {
        "name": "libwidget",
        "version": "1.2.3",
        "sha256": "1" * 64,
    },
    {
        "name": "libgizmo",
        "version": "4.5.6",
        "sha256": "2" * 64,
    },
    {
        "name": "app-thing",
        "version": "0.9.1",
        "sha256": "3" * 64,
    },
]

EXPECTED_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "required": ["name", "version", "sha256"],
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"},
            "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        },
        "additionalProperties": False,
    },
}


# ----------------------------------------------------------------------
# Generic, reusable helpers
# ----------------------------------------------------------------------
def _read_json(path: Path):
    """Read *path* and return parsed JSON, raising an informative error
    if anything goes wrong."""
    assert path.exists(), f"Expected file {path} is missing."
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{path} is not valid JSON: {exc}") from exc


# ----------------------------------------------------------------------
# Actual tests
# ----------------------------------------------------------------------
def test_build_directory_exists():
    assert BUILD_DIR.exists(), f"Directory {BUILD_DIR} does not exist."
    assert BUILD_DIR.is_dir(), f"{BUILD_DIR} exists but is not a directory."
    assert os.access(BUILD_DIR, os.W_OK), f"Directory {BUILD_DIR} is not writable."


def test_artifacts_json_initial_state():
    data = _read_json(ARTIFACTS_JSON)

    # 1) Basic shape
    assert isinstance(
        data, list
    ), f"{ARTIFACTS_JSON} should contain a JSON array, got {type(data).__name__}."

    # 2) Exact length
    assert (
        len(data) == 3
    ), f"{ARTIFACTS_JSON} should list exactly 3 artifacts, found {len(data)}."

    # 3) Content & order must match exactly what the assignment describes
    assert (
        data == EXPECTED_ARTIFACTS
    ), f"{ARTIFACTS_JSON} contents differ from the expected initial state."

    # 4) Quick schema-like validation to ensure the data is sane
    #    (students rely on the data to pass later steps).
    version_regex = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
    sha_regex = re.compile(r"^[a-f0-9]{64}$")
    for idx, item in enumerate(data, 1):
        for key in ("name", "version", "sha256"):
            assert key in item, f"Artifact #{idx} is missing required key '{key}'."
        assert isinstance(item["name"], str) and item["name"], (
            f"Artifact #{idx} 'name' must be a non-empty string."
        )
        assert version_regex.match(
            item["version"]
        ), f"Artifact #{idx} 'version' is not in MAJOR.MINOR.PATCH form."
        assert sha_regex.match(
            item["sha256"]
        ), f"Artifact #{idx} 'sha256' must be a 64-char lowercase hex string."


def test_artifact_schema_json_initial_state():
    schema = _read_json(SCHEMA_JSON)

    # Check that the schema structure matches what the assignment says.
    # We compare the *dict* directly so ordering of keys is irrelevant.
    assert (
        schema == EXPECTED_SCHEMA
    ), f"{SCHEMA_JSON} contents do not match the expected initial schema."