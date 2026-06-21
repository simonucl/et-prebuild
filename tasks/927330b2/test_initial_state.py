# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system /
# filesystem **before** the student performs any action for the “environment-
# configuration” task of the `react-auth` project.
#
# It asserts everything that *must* already be present as well as the absence
# of files that the student is expected to create.  Clear assertion messages
# are provided so that failures explicitly state what is missing or should not
# be there.
#
# NOTE:  These tests purposefully do **not** look for any of the artefacts the
#        student is tasked with creating (.env* files, logs directory, added
#        scripts, etc.).  They confirm only the pre-existing baseline.

import json
import os
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/home/user/projects/react-auth")
PACKAGE_JSON = PROJECT_ROOT / "package.json"
SRC_DIR = PROJECT_ROOT / "src"
ENV_DEVELOPMENT = PROJECT_ROOT / ".env.development"
ENV_PRODUCTION = PROJECT_ROOT / ".env.production"
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / "env_setup.log"


# ---------- helper -----------------------------------------------------------


def _load_package_json():
    """Return the contents of package.json as a dict, raising an assertion
    with helpful output if the file is missing or invalid JSON."""
    assert PACKAGE_JSON.exists(), f"Expected {PACKAGE_JSON} to exist."
    try:
        return json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(f"{PACKAGE_JSON} contains invalid JSON:\n{exc}")


# ---------- tests ------------------------------------------------------------


def test_project_root_exists_and_is_directory():
    assert PROJECT_ROOT.exists(), f"Directory {PROJECT_ROOT} is missing."
    assert PROJECT_ROOT.is_dir(), f"{PROJECT_ROOT} exists but is not a directory."


def test_required_files_and_directories_exist():
    assert PACKAGE_JSON.is_file(), f"Required file {PACKAGE_JSON} is missing."
    assert SRC_DIR.is_dir(), f"Required directory {SRC_DIR} is missing."


def test_src_directory_is_initially_empty():
    # It may contain a __init__.py or other placeholders in some repos, but
    # spec says “empty directory”, so assert no regular files are present.
    contents = [p for p in SRC_DIR.rglob("*") if p.is_file()]
    assert not contents, f"{SRC_DIR} should be empty, found files: {contents}"


def test_env_files_do_not_exist_yet():
    assert not ENV_DEVELOPMENT.exists(), f"{ENV_DEVELOPMENT} already exists; it should be created by the student."
    assert not ENV_PRODUCTION.exists(), f"{ENV_PRODUCTION} already exists; it should be created by the student."


def test_logs_directory_and_file_do_not_exist_yet():
    assert not LOGS_DIR.exists(), f"{LOGS_DIR} already exists; it should be created by the student."
    assert not LOG_FILE.exists(), f"{LOG_FILE} already exists; it should be created by the student."


def test_package_json_base_contents_before_modification():
    data = _load_package_json()

    # Top-level keys we expect at minimum
    expected_top_keys = {
        "name": "react-auth",
        "version": "0.1.0",
        "private": True,
    }
    for key, expected_val in expected_top_keys.items():
        assert data.get(key) == expected_val, (
            f"{PACKAGE_JSON}: expected key '{key}' to be {expected_val!r}, "
            f"found {data.get(key)!r}"
        )

    # Dependencies
    deps = data.get("dependencies", {})
    assert deps.get("react") == "^18.2.0", "Missing or incorrect react dependency."
    assert deps.get("react-dom") == "^18.2.0", "Missing or incorrect react-dom dependency."

    # Dev-dependencies
    dev_deps = data.get("devDependencies", {})
    assert dev_deps.get("env-cmd") == "^10.1.0", "Missing or incorrect env-cmd devDependency."
    assert dev_deps.get("react-scripts") == "5.0.1", "Missing or incorrect react-scripts devDependency."

    # Scripts section – only the default 'test' should exist initially
    scripts = data.get("scripts", {})
    assert "test" in scripts, "'test' script is missing from package.json."
    expected_test_script = 'echo "Error: no test specified" && exit 1'
    assert scripts["test"] == expected_test_script, (
        f"Unexpected value for 'test' script: {scripts['test']!r}"
    )

    # Ensure new scripts ('start:dev', 'start:prod') are NOT present yet.
    unexpected_scripts = {"start:dev", "start:prod"}
    existing_unexpected = unexpected_scripts.intersection(scripts.keys())
    assert not existing_unexpected, (
        f"{PACKAGE_JSON} should not yet contain scripts {sorted(existing_unexpected)}; "
        "they must be added by the student."
    )