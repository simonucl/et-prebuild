# test_initial_state.py
#
# Pytest suite that validates the initial, pre-task filesystem state
# for the “web-api” build–release exercise.
#
# It asserts that:
#   • The expected base directories exist.
#   • The /home/user/cicd/builds directory contains exactly three JAR
#     artifacts with the correct versioned filenames.
#   • Each JAR file has the expected placeholder payload.
#
# NOTE:
#   * Per grading rules, this file intentionally does NOT inspect or
#     mention any of the objects the student is asked to create
#     later (e.g. /home/user/cicd/releases or /home/user/cicd/pipeline.log).
#   * Stdlib + pytest only.

import os
import pathlib

import pytest

BASE_DIR = pathlib.Path("/home/user/cicd")
BUILDS_DIR = BASE_DIR / "builds"

EXPECTED_ARTIFACTS = {
    "artifact-1.2.3.jar": "dummy jar payload v1.2.3\n",
    "artifact-1.2.4.jar": "dummy jar payload v1.2.4\n",
    "artifact-1.3.0.jar": "dummy jar payload v1.3.0\n",
}


def test_base_directories_exist():
    assert BASE_DIR.is_dir(), f"Directory missing: {BASE_DIR}"
    assert BUILDS_DIR.is_dir(), f"Directory missing: {BUILDS_DIR}"


def test_builds_contains_only_expected_artifacts():
    files = {p.name for p in BUILDS_DIR.iterdir() if p.is_file()}
    expected_files = set(EXPECTED_ARTIFACTS)

    # Check for missing artifacts
    missing = expected_files - files
    assert not missing, (
        "The following expected artifact(s) are missing from "
        f"{BUILDS_DIR}: {sorted(missing)}"
    )

    # Check for unexpected extra files
    extra = files - expected_files
    assert not extra, (
        "Unexpected file(s) found in "
        f"{BUILDS_DIR}: {sorted(extra)}"
    )


@pytest.mark.parametrize("filename, expected_payload", EXPECTED_ARTIFACTS.items())
def test_each_artifact_has_correct_payload(filename, expected_payload):
    file_path = BUILDS_DIR / filename
    assert file_path.is_file(), f"Expected artifact missing: {file_path}"

    data = file_path.read_text(encoding="utf-8")
    assert (
        data == expected_payload
    ), f"Artifact {filename} has unexpected content: {repr(data)}"