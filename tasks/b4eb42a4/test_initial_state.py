# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state *before*
# the student executes any commands for the “release-manager” task.
#
# Only the following facts must hold true:
#   • The two draft release descriptors exist exactly where expected and
#     are well-formed according to the high-level constraints in the spec.
#   • No deliverable output artefacts have been created yet.
#
# If any assertion fails, the accompanying message will tell the student
# precisely what is missing or malformed.
#
# NOTE: Uses only Python stdlib + pytest (no third-party deps).

import json
import os
import re
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
INPUT_DIR = HOME / "releases" / "input"
OUTPUT_DIR = HOME / "releases" / "output"

RELEASE_A = INPUT_DIR / "release-a.json"
RELEASE_B = INPUT_DIR / "release-b.json"

# Paths that must *not* exist yet (they will be produced by the student)
SCHEMA_PATH = HOME / "releases" / "release.schema.json"
VALIDATION_LOG = OUTPUT_DIR / "validation.log"
SERVICE_SUMMARY = OUTPUT_DIR / "service-summary.json"

VERSION_PATTERN = re.compile(r"^v[0-9]+$")


@pytest.fixture(scope="module", params=[INPUT_DIR])
def ensure_input_dir(request):
    """Ensure the input directory exists and is a directory."""
    dir_path = request.param
    assert dir_path.exists(), f"Required directory missing: {dir_path}"
    assert dir_path.is_dir(), f"Expected {dir_path} to be a directory."
    # also ensure it's readable
    mode = dir_path.stat().st_mode
    assert mode & stat.S_IROTH or mode & stat.S_IRUSR, f"Directory {dir_path} is not readable."
    return dir_path


def _load_json(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path} is not valid JSON: {exc}")
    except FileNotFoundError:
        pytest.fail(f"Expected file not found: {path}")


@pytest.mark.parametrize("file_path", [RELEASE_A, RELEASE_B])
def test_release_files_exist(ensure_input_dir, file_path):
    """Each draft release descriptor must exist."""
    assert file_path.exists(), f"Required file missing: {file_path}"
    assert file_path.is_file(), f"{file_path} should be a file, not a directory."


@pytest.mark.parametrize(
    "file_path,expected_version,expected_services",
    [
        (
            RELEASE_A,
            "v1",
            [
                {"name": "auth", "image": "registry.example.com/auth:1.2.3", "replicas": 2},
                {"name": "billing", "image": "registry.example.com/billing:3.4.5", "replicas": 1},
            ],
        ),
        (
            RELEASE_B,
            "v2",
            [
                {"name": "auth", "image": "registry.example.com/auth:1.2.4", "replicas": 3},
                {"name": "search", "image": "registry.example.com/search:2.1.0", "replicas": 2},
            ],
        ),
    ],
)
def test_release_json_structure(file_path, expected_version, expected_services):
    """Validate structure and content of each draft release descriptor."""
    data = _load_json(file_path)

    # -- Top-level validations -------------------------------------------------
    assert set(data.keys()) == {"version", "services"}, (
        f"{file_path} must contain only the keys 'version' and 'services'. "
        f"Found keys: {sorted(data.keys())}"
    )

    # version
    assert isinstance(data["version"], str), f"'version' in {file_path} must be a string."
    assert VERSION_PATTERN.fullmatch(data["version"]), (
        f"'version' value '{data['version']}' in {file_path} does not match pattern ^v[0-9]+$"
    )
    assert data["version"] == expected_version, (
        f"Unexpected version in {file_path}: expected '{expected_version}', "
        f"found '{data['version']}'"
    )

    # services
    services = data["services"]
    assert isinstance(services, list) and services, f"'services' in {file_path} must be a non-empty list."

    # Compare against expected services ignoring element order
    def _service_key(svc):
        return (svc["name"], svc["image"], svc["replicas"])

    expected_sorted = sorted(expected_services, key=_service_key)
    actual_sorted = sorted(services, key=_service_key)
    assert actual_sorted == expected_sorted, (
        f"'services' array in {file_path} differs from expected.\n"
        f"Expected: {expected_services}\nActual:   {services}"
    )

    # Per-service checks
    for svc in services:
        assert set(svc.keys()) == {"name", "image", "replicas"}, (
            f"Each service in {file_path} must contain exactly the keys "
            f"'name', 'image', and 'replicas'. Found: {sorted(svc.keys())}"
        )
        assert isinstance(svc["name"], str) and svc["name"], f"Service 'name' in {file_path} must be a non-empty string."
        assert isinstance(svc["image"], str) and svc["image"], f"Service 'image' in {file_path} must be a non-empty string."
        assert (
            isinstance(svc["replicas"], int) and svc["replicas"] >= 1
        ), f"Service 'replicas' in {file_path} must be an integer ≥ 1."


def test_output_artefacts_do_not_exist_yet():
    """No deliverable output files should exist before the student runs their commands."""
    for artefact in (OUTPUT_DIR, SCHEMA_PATH, VALIDATION_LOG, SERVICE_SUMMARY):
        assert not artefact.exists(), (
            f"Output artefact {artefact} should NOT exist before execution, "
            "but it is already present."
        )