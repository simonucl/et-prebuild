# test_initial_state.py
#
# Pytest suite that verifies the **initial** filesystem / data state
# for the “Validate Incident JSON Records” exercise.
#
# The tests deliberately *avoid* touching any of the paths that will be
# created by the student’s solution.  They only inspect the read-only
# source material that must already be present when the assignment begins.
#
# Allowed imports: stdlib + pytest only.

import json
from pathlib import Path

import pytest

# ---------- Static paths -----------------------------------------------------

BASE_DIR = Path("/home/user/incidents/2023-09-15")
REQUIRED_FILES = {
    "incident_schema.json",
    "event1.json",
    "event2.json",
    "event3.json",
}

# ---------- Helper functions -------------------------------------------------


def read_json(path: Path):
    """
    Load a JSON file and return the resulting Python object.

    The helper produces a clear pytest failure if parsing fails.
    """
    try:
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path} is not valid JSON: {exc}", pytrace=False)


# ---------- Tests ------------------------------------------------------------


def test_source_directory_exists():
    assert BASE_DIR.exists(), f"Required directory {BASE_DIR} is missing"
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory"


@pytest.mark.parametrize("filename", sorted(REQUIRED_FILES))
def test_required_files_present(filename):
    path = BASE_DIR / filename
    assert path.exists(), f"Required file {path} is missing"
    assert path.is_file(), f"{path} exists but is not a regular file"
    # Sanity-check that the file can be read as UTF-8 text
    try:
        _ = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"File {path} could not be decoded as UTF-8: {exc}", pytrace=False)


@pytest.mark.parametrize(
    "filename,should_have_source_ip",
    [
        ("event1.json", True),
        ("event2.json", True),
        ("event3.json", False),  # intentionally malformed; missing source_ip
    ],
)
def test_event_json_structure(filename, should_have_source_ip):
    """
    Basic structural checks on the three event JSON files.

    * Must be a JSON object.
    * Must have the keys required by the assignment.
    * event3.json is intentionally malformed (missing 'source_ip').
    """
    required_keys = {"event_id", "severity", "event_type", "timestamp"}
    path = BASE_DIR / filename
    data = read_json(path)

    assert isinstance(
        data, dict
    ), f"{filename} must contain a JSON object at the top level"

    # Check presence of the always-required subset
    missing = required_keys - data.keys()
    assert (
        not missing
    ), f"{filename} is missing expected key(s): {', '.join(sorted(missing))}"

    if should_have_source_ip:
        assert (
            "source_ip" in data
        ), f"{filename} should contain the key 'source_ip' but it is missing"
    else:
        assert (
            "source_ip" not in data
        ), f"{filename} should NOT contain 'source_ip' according to the exercise setup"

    # Additional sanity around severity values
    valid_severities = {"low", "medium", "high", "critical"}
    sev = data.get("severity")
    assert (
        sev in valid_severities
    ), f"{filename} has an unexpected severity value: {sev!r}"


def test_schema_is_valid_json_and_has_required_fields():
    """
    Very light sanity check on incident_schema.json so students are alerted
    early if the file became corrupted.
    """
    schema_path = BASE_DIR / "incident_schema.json"
    schema = read_json(schema_path)

    # Must itself be a JSON object
    assert isinstance(
        schema, dict
    ), "incident_schema.json must contain a JSON object at the top level"

    # Verify that the schema lists the required properties we expect
    for key in ["type", "required", "properties"]:
        assert (
            key in schema
        ), f"incident_schema.json is missing the '{key}' top-level key"

    expected_required_fields = [
        "event_id",
        "severity",
        "event_type",
        "timestamp",
        "source_ip",
    ]
    for field in expected_required_fields:
        assert (
            field in schema.get("required", [])
        ), f"incident_schema.json 'required' does not include '{field}'"