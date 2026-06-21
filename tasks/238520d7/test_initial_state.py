# test_initial_state.py
#
# This test-suite verifies that the system is in the **initial** state
# expected *before* the student starts working on the assignment.
#
# 1. The directory /home/user/configs must exist.
# 2. The three snapshot / schema JSON files must exist and contain the
#    exact data spelled out in the task description.
# 3. The helper tool `jq` must be available in the PATH (the task tells
#    the student to use it).
# 4. No result / output artefacts must be present yet.
#
# All checks are performed using only the Python standard library + pytest.

import json
import os
import stat
import subprocess
import shutil
from pathlib import Path

import pytest

CONFIG_DIR = Path("/home/user/configs")
PREVIOUS_FILE = CONFIG_DIR / "previous_config.json"
NEW_FILE = CONFIG_DIR / "new_config.json"
SCHEMA_FILE = CONFIG_DIR / "schema.json"
VALIDATION_RESULT = CONFIG_DIR / "validation_result.log"
CHANGE_SUMMARY = CONFIG_DIR / "change_summary.log"


@pytest.fixture(scope="module")
def previous_config():
    with PREVIOUS_FILE.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@pytest.fixture(scope="module")
def new_config():
    with NEW_FILE.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@pytest.fixture(scope="module")
def schema_json():
    with SCHEMA_FILE.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def _assert_file_mode_writeable(path: Path):
    """
    Ensure that the current user can write to the directory containing *path*.
    """
    parent = path if path.is_dir() else path.parent
    mode = parent.stat().st_mode
    assert mode & stat.S_IWUSR, f"Path {parent} is not writable by the owner."


def test_configs_directory_exists():
    assert CONFIG_DIR.exists(), (
        "The directory /home/user/configs is missing. "
        "Create it before starting the assignment."
    )
    assert CONFIG_DIR.is_dir(), "/home/user/configs exists but is not a directory."
    _assert_file_mode_writeable(CONFIG_DIR)


@pytest.mark.parametrize(
    "path_",
    [PREVIOUS_FILE, NEW_FILE, SCHEMA_FILE],
)
def test_required_json_files_exist(path_):
    assert path_.exists(), f"Required file {path_} is missing."
    assert path_.is_file(), f"{path_} exists but is not a regular file."
    # Basic JSON load to make sure file is valid JSON
    try:
        with path_.open("r", encoding="utf-8") as fp:
            json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path_} contains invalid JSON: {exc}")


def test_schema_contains_required_keys(schema_json):
    required = {"service", "logging", "version"}
    schema_required = set(schema_json.get("required", []))
    missing = required - schema_required
    assert not missing, (
        f"schema.json must list {sorted(required)} in its top-level 'required' "
        f"array. Missing: {sorted(missing)}"
    )


def test_previous_config_expected_values(previous_config):
    assert previous_config["service"]["enabled"] is True, (
        "previous_config.json: service.enabled should be true."
    )
    assert previous_config["service"]["port"] == 8080, (
        "previous_config.json: service.port should be 8080."
    )
    assert previous_config["logging"]["level"] == "info", (
        "previous_config.json: logging.level should be 'info'."
    )
    assert previous_config["logging"]["file"] == "/var/log/demo.log", (
        "previous_config.json: logging.file should be '/var/log/demo.log'."
    )
    assert previous_config["version"] == "1.0.0", (
        "previous_config.json: version should be '1.0.0'."
    )


def test_new_config_expected_values(new_config):
    assert new_config["service"]["enabled"] is False, (
        "new_config.json: service.enabled should be false."
    )
    assert new_config["service"]["port"] == 9090, (
        "new_config.json: service.port should be 9090."
    )
    assert new_config["logging"]["level"] == "debug", (
        "new_config.json: logging.level should be 'debug'."
    )
    assert new_config["logging"]["file"] == "/var/log/demo-debug.log", (
        "new_config.json: logging.file should be '/var/log/demo-debug.log'."
    )
    assert new_config["version"] == "1.1.0", (
        "new_config.json: version should be '1.1.0'."
    )


def test_jq_is_available():
    jq_path = shutil.which("jq")
    assert jq_path, (
        "The command-line tool 'jq' is not found in PATH. "
        "It must be installed for the student to complete the task."
    )
    # Additional sanity check: ensure jq can run
    try:
        subprocess.run([jq_path, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"'jq' is present but could not be executed: {exc}")


@pytest.mark.parametrize(
    "path_",
    [VALIDATION_RESULT, CHANGE_SUMMARY],
)
def test_no_output_files_yet(path_):
    assert not path_.exists(), (
        f"{path_} already exists. The student should create it during the task—"
        "remove the file so that the assignment starts from a clean state."
    )