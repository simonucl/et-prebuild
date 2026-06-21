# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem
# is in the pristine, pre-task state expected by the grader _before_
# the student starts working.

import json
import re
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Paths used throughout the tests
# ---------------------------------------------------------------------------
BASE_DIR = Path("/home/user/configs")
CONFIG_FILE = BASE_DIR / "app_config.json"
SCHEMA_FILE = BASE_DIR / "app_schema.json"
CHANGELOG_FILE = BASE_DIR / "change.log"
SUMMARY_FILE = BASE_DIR / "app_summary.json"


# ---------------------------------------------------------------------------
# The exact initial contents that must be present
# ---------------------------------------------------------------------------
CONFIG_EXPECTED = {
    "version": "1.2.3",
    "environment": "staging",
    "services": [
        {
            "name": "web",
            "image": "example/web:latest",
            "enabled": True,
            "ports": [80, 443],
        },
        {
            "name": "db",
            "image": "postgres:13",
            "enabled": False,
            "ports": [5432],
        },
    ],
    "owner": "ops@example.com",
}

SCHEMA_EXPECTED = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["version", "services"],
    "properties": {
        "version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"},
        "environment": {"type": "string"},
        "owner": {"type": "string", "format": "email"},
        "services": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["name", "enabled"],
                "properties": {
                    "name": {"type": "string"},
                    "image": {"type": "string"},
                    "enabled": {"type": "boolean"},
                    "ports": {
                        "type": "array",
                        "items": {"type": "integer", "minimum": 1, "maximum": 65535},
                    },
                },
            },
        },
    },
    "additionalProperties": True,
}

CHANGELOG_LINE_EXPECTED = "2023-12-31T23:59:59Z initial_seed\n"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:  # pragma: no cover
        pytest.fail(f"{path} is not valid JSON: {e}")


# ---------------------------------------------------------------------------
# Individual tests
# ---------------------------------------------------------------------------
def test_directory_structure():
    assert BASE_DIR.is_dir(), f"Required directory {BASE_DIR} is missing."


@pytest.mark.parametrize(
    "path_obj",
    [
        pytest.param(CONFIG_FILE, id="app_config.json"),
        pytest.param(SCHEMA_FILE, id="app_schema.json"),
        pytest.param(CHANGELOG_FILE, id="change.log"),
    ],
)
def test_required_files_exist(path_obj):
    assert path_obj.is_file(), f"Required file {path_obj} is missing."


def test_no_summary_file_yet():
    assert not SUMMARY_FILE.exists(), (
        f"{SUMMARY_FILE} should NOT exist before the student starts the task. "
        "Found an unexpected summary file."
    )


def test_app_config_contents():
    actual = load_json(CONFIG_FILE)
    assert actual == CONFIG_EXPECTED, (
        f"{CONFIG_FILE} contents do not match the expected initial configuration."
    )

    # Additional lightweight validation that mimics parts of the schema
    # (done with stdlib only, _not_ full json-schema validation).
    version = actual.get("version")
    services = actual.get("services")
    assert re.match(r"^\d+\.\d+\.\d+$", version), (
        f"{CONFIG_FILE}: 'version' value {version!r} does not match x.y.z pattern."
    )
    assert isinstance(services, list) and services, (
        f"{CONFIG_FILE}: 'services' must be a non-empty list."
    )
    for idx, svc in enumerate(services):
        assert isinstance(svc.get("name"), str), (
            f"{CONFIG_FILE}: services[{idx}].name must be a string."
        )
        assert isinstance(svc.get("enabled"), bool), (
            f"{CONFIG_FILE}: services[{idx}].enabled must be a boolean."
        )


def test_app_schema_contents():
    actual = load_json(SCHEMA_FILE)
    assert actual == SCHEMA_EXPECTED, (
        f"{SCHEMA_FILE} contents do not match the expected initial schema."
    )


def test_changelog_initial_state():
    data = CHANGELOG_FILE.read_text()
    lines = data.splitlines(keepends=True)

    assert lines, f"{CHANGELOG_FILE} is empty; expected exactly one seed line."
    assert len(
        lines
    ) == 1, f"{CHANGELOG_FILE} should contain exactly one line initially, found {len(lines)}."
    assert (
        lines[0] == CHANGELOG_LINE_EXPECTED
    ), f"{CHANGELOG_FILE} first line is incorrect. Expected {CHANGELOG_LINE_EXPECTED!r}"