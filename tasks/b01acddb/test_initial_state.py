# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state *before* the student performs any actions for the “API-gateway
# smoke-tests” task.
#
# The suite checks:
#   1. Presence and contents of the two configuration files.
#   2. Existence and emptiness of the /home/user/api-gateway/test_results/
#      directory.
#   3. Absence of the results file that the student will create later.
#
# Requirements:
#   • stdlib + pytest only.
#   • Clear assertion messages on failure.
#   • Absolute paths are used.

import os
import pathlib

import pytest

# Absolute paths used throughout the tests
YAML_PATH = pathlib.Path("/home/user/api-gateway/config.yaml")
TOML_PATH = pathlib.Path("/home/user/api-gateway/config.toml")
TEST_RESULTS_DIR = pathlib.Path("/home/user/api-gateway/test_results")
OUTPUT_TXT = TEST_RESULTS_DIR / "output.txt"

# Expected *initial* values
YAML_EXPECTED_BASE_URL = 'https://dev.example.com/v1'
TOML_EXPECTED_BASE_URL = 'https://dev.example.com/v1'
EXPECTED_LOG_LEVEL = 'info'


@pytest.fixture(scope="module")
def yaml_content():
    """Read the YAML file once per test session."""
    try:
        return YAML_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Missing file: {YAML_PATH}")


@pytest.fixture(scope="module")
def toml_content():
    """Read the TOML file once per test session."""
    try:
        return TOML_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Missing file: {TOML_PATH}")


def test_yaml_file_exists_and_contains_expected_values(yaml_content):
    # Basic sanity: file should not be empty
    assert yaml_content.strip(), f"{YAML_PATH} is empty."

    # Check for correct base_url
    assert (
        f'"{YAML_EXPECTED_BASE_URL}"' in yaml_content
    ), (
        f"{YAML_PATH} should contain base_url "
        f'"{YAML_EXPECTED_BASE_URL}" but does not.'
    )

    # Check for correct log level
    assert (
        f'level: "{EXPECTED_LOG_LEVEL}"' in yaml_content
    ), (
        f"{YAML_PATH} should contain logging level "
        f'"{EXPECTED_LOG_LEVEL}" but does not.'
    )

    # Ensure *new* values are NOT present yet
    assert (
        'https://sandbox.example.com/v2' not in yaml_content
    ), (
        f"{YAML_PATH} already contains sandbox base_url; "
        "the student has modified the file too early."
    )
    assert (
        'level: "debug"' not in yaml_content
    ), (
        f"{YAML_PATH} already contains logging level debug; "
        "the student has modified the file too early."
    )


def test_toml_file_exists_and_contains_expected_values(toml_content):
    # Basic sanity: file should not be empty
    assert toml_content.strip(), f"{TOML_PATH} is empty."

    # Check for correct base_url
    expected_line = f'base_url = "{TOML_EXPECTED_BASE_URL}"'
    assert (
        expected_line in toml_content
    ), (
        f"{TOML_PATH} should contain line: {expected_line!r} but does not."
    )

    # Check for correct log level
    expected_log_line = f'level = "{EXPECTED_LOG_LEVEL}"'
    assert (
        expected_log_line in toml_content
    ), (
        f"{TOML_PATH} should contain line: {expected_log_line!r} but does not."
    )

    # Ensure *new* values are NOT present yet
    assert (
        'https://sandbox.example.com/v2' not in toml_content
    ), (
        f"{TOML_PATH} already contains sandbox base_url; "
        "the student has modified the file too early."
    )
    assert (
        'level = "debug"' not in toml_content
    ), (
        f"{TOML_PATH} already contains logging level debug; "
        "the student has modified the file too early."
    )


def test_test_results_directory_exists_and_is_empty():
    # Directory must exist
    assert TEST_RESULTS_DIR.is_dir(), (
        f"Directory {TEST_RESULTS_DIR} is missing. It must exist before the "
        "student runs the task."
    )

    # Directory must be empty
    contents = list(TEST_RESULTS_DIR.iterdir())
    assert contents == [], (
        f"Directory {TEST_RESULTS_DIR} is expected to be empty initially, "
        f"but it contains: {[p.name for p in contents]}"
    )


def test_output_txt_does_not_exist_yet():
    # The verification file should not exist before the student creates it.
    assert not OUTPUT_TXT.exists(), (
        f"{OUTPUT_TXT} should not exist before the task is performed."
    )