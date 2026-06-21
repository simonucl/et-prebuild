# test_initial_state.py
#
# This pytest suite checks the *initial* state of the OS / filesystem
# before the student performs any action.  It ensures that the two JSON
# specification files required for the task are present, readable, valid
# JSON, and contain exactly the expected content.
#
# • /home/user/release/env_schema.json
# • /home/user/release/env_descriptor.json
#
# No assertions are made about the two *output* artefacts
# (validation.log, release_summary.csv) because they should not exist yet.
#
# The tests purposefully avoid any non-stdlib dependencies; everything is
# done with the Python Standard Library plus pytest only.

import json
import re
from pathlib import Path

import pytest

RELEASE_DIR = Path("/home/user/release")
SCHEMA_PATH = RELEASE_DIR / "env_schema.json"
DESCRIPTOR_PATH = RELEASE_DIR / "env_descriptor.json"


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def schema_json():
    """Load and return the JSON object from env_schema.json."""
    assert SCHEMA_PATH.is_file(), f"Missing required file: {SCHEMA_PATH}"
    with SCHEMA_PATH.open(encoding="utf-8") as fp:
        try:
            return json.load(fp)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{SCHEMA_PATH} is not valid JSON: {exc}")


@pytest.fixture(scope="session")
def descriptor_json():
    """Load and return the JSON object from env_descriptor.json."""
    assert DESCRIPTOR_PATH.is_file(), f"Missing required file: {DESCRIPTOR_PATH}"
    with DESCRIPTOR_PATH.open(encoding="utf-8") as fp:
        try:
            return json.load(fp)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{DESCRIPTOR_PATH} is not valid JSON: {exc}")


# ---------------------------------------------------------------------------
# Expected canonical content
# (taken directly from the task description, minified to avoid whitespace
#  ambiguity so that an object-level equality comparison can be made).
# ---------------------------------------------------------------------------

EXPECTED_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["version", "services"],
    "properties": {
        "version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"},
        "services": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["name", "image", "ports"],
                "properties": {
                    "name": {"type": "string"},
                    "image": {"type": "string"},
                    "ports": {
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "integer", "minimum": 1, "maximum": 65535},
                    },
                },
                "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
}

EXPECTED_DESCRIPTOR = {
    "version": "1.4.0",
    "services": [
        {
            "name": "auth-service",
            "image": "registry.example.com/auth:1.4.0",
            "ports": [8080],
        },
        {
            "name": "payments-service",
            "image": "registry.example.com/payments:2.1.3",
            "ports": [9000, 9001],
        },
    ],
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_release_directory_exists():
    assert RELEASE_DIR.is_dir(), f"Required directory does not exist: {RELEASE_DIR}"


def test_required_files_exist_and_are_readable():
    for path in (SCHEMA_PATH, DESCRIPTOR_PATH):
        assert path.exists(), f"Required file missing: {path}"
        assert path.is_file(), f"Path exists but is not a file: {path}"
        assert path.stat().st_size > 0, f"File is empty: {path}"


def test_schema_content_matches_expected(schema_json):
    assert (
        schema_json == EXPECTED_SCHEMA
    ), "env_schema.json content does not match the expected schema definition."


def test_descriptor_content_matches_expected(descriptor_json):
    assert (
        descriptor_json == EXPECTED_DESCRIPTOR
    ), "env_descriptor.json content does not match the expected descriptor."


def test_descriptor_version_format(descriptor_json):
    version = descriptor_json.get("version")
    pattern = r"^[0-9]+\.[0-9]+\.[0-9]+$"
    assert isinstance(
        version, str
    ), f"Descriptor 'version' should be a string, got {type(version).__name__}"
    assert re.match(
        pattern, version
    ), f"Descriptor version '{version}' does not match pattern {pattern!r}"


def test_descriptor_services_structure(descriptor_json):
    services = descriptor_json.get("services")
    assert isinstance(
        services, list
    ), f"Descriptor 'services' should be a list, got {type(services).__name__}"
    assert services, "Descriptor 'services' list must not be empty."

    allowed_service_keys = {"name", "image", "ports"}

    for idx, service in enumerate(services, start=1):
        assert isinstance(
            service, dict
        ), f"Service #{idx} should be an object, got {type(service).__name__}"
        extra_keys = set(service) - allowed_service_keys
        assert (
            extra_keys == set()
        ), f"Service #{idx} contains unexpected keys: {extra_keys}"
        for key in allowed_service_keys:
            assert key in service, f"Service #{idx} missing required key: {key}"

        # Validate ports
        ports = service["ports"]
        assert isinstance(
            ports, list
        ), f"Service #{idx} 'ports' should be a list, got {type(ports).__name__}"
        assert (
            ports
        ), f"Service #{idx} 'ports' list must contain at least one port number."
        for port in ports:
            assert isinstance(
                port, int
            ), f"Service #{idx} port '{port}' is not an integer."
            assert 1 <= port <= 65535, (
                f"Service #{idx} port '{port}' is outside valid TCP/UDP port range "
                "(1–65535)."
            )