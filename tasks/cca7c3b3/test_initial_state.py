# test_initial_state.py
#
# Pytest suite to validate the initial, pre-exercise state of the file system.
# These tests confirm that the legacy CI/CD configuration file needed for the
# exercise is present and contains the expected values.  They intentionally do
# NOT check for any output artefacts that the student is supposed to create.

import os
import configparser
import pytest
from pathlib import Path


CONFIG_PATH = Path("/home/user/projects/ci_cd/config/build_settings.ini")


@pytest.fixture(scope="module")
def config_parser():
    """
    Return a ConfigParser object loaded with the INI file content.

    The fixture will skip all dependent tests if the file is missing so that
    subsequent assertions do not raise secondary errors that obscure the root
    cause.
    """
    if not CONFIG_PATH.exists():
        pytest.skip(
            f"Required configuration file not found at {CONFIG_PATH}. "
            "The exercise expects this file to be pre-placed."
        )
    if not CONFIG_PATH.is_file():
        pytest.skip(
            f"Expected a regular file at {CONFIG_PATH}, "
            "but found something else."
        )

    parser = configparser.ConfigParser(interpolation=None)
    with CONFIG_PATH.open("r", encoding="utf-8") as fp:
        parser.read_file(fp)
    return parser


def test_config_file_exists_and_readable():
    """Ensure the configuration file exists and is readable."""
    assert CONFIG_PATH.exists(), (
        f"The configuration file should exist at {CONFIG_PATH}, "
        "but it is missing."
    )
    assert CONFIG_PATH.is_file(), (
        f"Expected {CONFIG_PATH} to be a regular file, "
        "but it is not."
    )
    # Attempt to open the file to verify readability.
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as fp:
            fp.read(1)  # Read a single byte/char to confirm readability.
    except Exception as exc:  # noqa: BLE001
        pytest.fail(f"Unable to read {CONFIG_PATH}: {exc}")


def test_ini_sections_present(config_parser):
    """Verify that required sections are present in the INI file."""
    missing = [s for s in ("build", "runtime") if s not in config_parser]
    assert not missing, (
        f"The INI file {CONFIG_PATH} is missing the following required "
        f"section(s): {', '.join(missing)}"
    )


def test_runtime_python_version(config_parser):
    """Confirm [runtime].python_version has the expected value."""
    expected = "3.10"
    try:
        actual = config_parser["runtime"]["python_version"]
    except KeyError:
        pytest.fail(
            f"'python_version' key missing in the [runtime] section "
            f"of {CONFIG_PATH}."
        )
    assert actual == expected, (
        f"Expected [runtime].python_version to be '{expected}', "
        f"but found '{actual}'."
    )


def test_build_timeout_value(config_parser):
    """Confirm [build].timeout has the expected value."""
    expected = "420"
    try:
        actual = config_parser["build"]["timeout"]
    except KeyError:
        pytest.fail(
            f"'timeout' key missing in the [build] section "
            f"of {CONFIG_PATH}."
        )
    assert actual == expected, (
        f"Expected [build].timeout to be '{expected}', "
        f"but found '{actual}'."
    )