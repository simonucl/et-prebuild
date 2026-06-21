# test_initial_state.py
#
# This pytest file verifies the **initial** operating-system / filesystem
# state that must exist *before* the student starts working on the exercise.
#
# It purposely does **not** test for any of the deliverable files that the
# student is expected to create (`high_severity_incidents.json`,
# `processing.log`, etc.).  Instead it focuses only on the files and content
# that are supposed to be present at the very beginning of the session.

import json
import os
from pathlib import Path

# Absolute paths that must exist beforehand
BASE_DIR = Path("/home/user/incident_responder")
INCIDENTS_FILE = BASE_DIR / "incidents.json"
SCHEMA_FILE = BASE_DIR / "incident_schema.json"


def test_directory_exists():
    """The incident_responder directory must exist."""
    assert BASE_DIR.is_dir(), (
        f"Required directory {BASE_DIR} is missing. "
        "The exercise cannot proceed without it."
    )


def test_required_files_exist():
    """Both the incidents data file and the schema file must be present."""
    missing = [str(p) for p in (INCIDENTS_FILE, SCHEMA_FILE) if not p.is_file()]
    assert not missing, (
        "The following required file(s) are missing: " + ", ".join(missing)
    )


def _load_json(path: Path):
    """Load JSON, raising an explicit assertion if parsing fails."""
    try:
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        assert False, f"File {path} is not valid JSON: {exc}"


def test_incidents_json_structure_and_content():
    """
    incidents.json must:
      * be an array of exactly four objects
      * each object must have the required keys with correct basic types
      * contain exactly two items with severity == 'high'
    """
    data = _load_json(INCIDENTS_FILE)

    assert isinstance(data, list), "incidents.json must be a JSON array."
    assert len(data) == 4, (
        f"Expected 4 incident records, found {len(data)} in {INCIDENTS_FILE}."
    )

    required_keys = {"id": int, "timestamp": str, "severity": str, "message": str}
    high_severity_count = 0
    ids_seen = set()

    for idx, item in enumerate(data, start=1):
        assert isinstance(item, dict), (
            f"Item #{idx} in incidents.json is not an object."
        )

        # Check presence of all required keys
        for key, expected_type in required_keys.items():
            assert key in item, (
                f"Item #{idx} missing required key '{key}'. "
                f"Current keys: {list(item.keys())}"
            )
            assert isinstance(item[key], expected_type), (
                f"Key '{key}' in item #{idx} should be of type "
                f"{expected_type.__name__}, got {type(item[key]).__name__}."
            )

        # Basic domain validations
        ids_seen.add(item["id"])
        assert item["severity"] in {"low", "medium", "high"}, (
            f"Item #{idx} has invalid severity '{item['severity']}'."
        )
        if item["severity"] == "high":
            high_severity_count += 1

    assert high_severity_count == 2, (
        f"Expected exactly 2 high-severity incidents, found {high_severity_count}."
    )
    assert len(ids_seen) == 4, "Incident IDs must be unique."


def test_schema_file_is_valid_json_and_draft_07():
    """
    incident_schema.json must be valid JSON and advertise Draft-07.
    We don't perform full schema validation (would need extra deps),
    but we ensure the root keys look correct.
    """
    schema = _load_json(SCHEMA_FILE)

    assert isinstance(schema, dict), "incident_schema.json must be a JSON object."
    assert schema.get("$schema", "").endswith("draft-07/schema#"), (
        "incident_schema.json must declare Draft-07 via the '$schema' key."
    )
    assert schema.get("type") == "array", (
        "Top-level 'type' in incident_schema.json should be 'array'."
    )