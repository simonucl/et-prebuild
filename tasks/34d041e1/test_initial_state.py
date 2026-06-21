# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem before the
# student makes any changes.  These checks guarantee that the project starts
# from the known, expected baseline described in the assignment.
#
# NOTE:
#   • We purposely do NOT test for any of the files the student is asked to
#     create or modify (other than verifying the *pre-change* contents of
#     service.conf).  In particular, we make no mention of
#     “logs/debug_summary.log”.
#   • Only the Python standard library and pytest are used.

import os
import pathlib
import textwrap

import pytest

# Canonical project root for all tests
PROJECT_ROOT = pathlib.Path("/home/user/devops-demo").resolve()

CONFIG_FILE = PROJECT_ROOT / "config" / "service.conf"
APP_LOG_FILE = PROJECT_ROOT / "logs" / "app.log"


def _read_file(path: pathlib.Path) -> str:
    """Return the full contents of *path* decoded as UTF-8."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def service_conf_contents():
    """Fixture that returns the raw text inside service.conf."""
    return _read_file(CONFIG_FILE)


def test_directory_structure_exists():
    """
    Validate that the project directory layout is present and correct.

    We only test for items that must already exist *before* the student’s work
    begins.
    """
    expected_dirs = [
        PROJECT_ROOT,
        PROJECT_ROOT / "bin",
        PROJECT_ROOT / "config",
        PROJECT_ROOT / "logs",
    ]
    for d in expected_dirs:
        assert d.is_dir(), f"Required directory is missing: {d}"


def test_required_files_exist():
    """
    Ensure that the files that should be present initially really exist.
    """
    assert CONFIG_FILE.is_file(), f"Missing configuration file: {CONFIG_FILE}"
    assert APP_LOG_FILE.is_file(), f"Missing application log file: {APP_LOG_FILE}"


def test_service_conf_initial_contents(service_conf_contents):
    """
    The INITIAL configuration must contain the original settings:

        [logging]
        log_level = INFO
        log_file  = ./logs/app.log

    • We do NOT want to see 'DEBUG' in the log_level yet.
    • We do NOT want an absolute path in 'log_file' yet.
    """
    # Normalise newlines to simplify multi-platform comparisons
    conf_text = service_conf_contents.replace("\r\n", "\n")

    #
    # Basic semantics: section header and two expected keys
    #
    assert "[logging]" in conf_text, (
        "The [logging] section header is missing from service.conf."
    )

    # Check that the expected key/value pairs are present.
    required_lines = {
        "log_level": "INFO",
        "log_file": "./logs/app.log",
    }

    for key, expected_value in required_lines.items():
        matches = [
            line
            for line in conf_text.splitlines()
            if line.strip().startswith(f"{key}")
        ]
        assert matches, (
            f"Key '{key}' is missing from service.conf; "
            f"expected '{key} = {expected_value}'."
        )
        # Take the first match and verify its value
        actual_value = matches[0].split("=", 1)[1].strip()
        assert (
            actual_value == expected_value
        ), f"Key '{key}' has value '{actual_value}', expected '{expected_value}'."

    #
    # Defensive check: make sure DEBUG was not already set accidentally.
    #
    assert "log_level = DEBUG" not in conf_text, (
        "service.conf already contains 'log_level = DEBUG'—"
        "it should still be 'INFO' at this point."
    )
    assert "/home/user/devops-demo/logs/app.log" not in conf_text, (
        "service.conf already uses an absolute log_file path—"
        "it should still be './logs/app.log' at this point."
    )


def test_app_log_has_expected_counts():
    """
    Confirm that the shipping log file contains exactly:

      • 3 lines with the substring 'DEBUG'
      • 2 lines with the substring 'ERROR'

    These numbers form the ground truth that the student's future summary file
    must report.
    """
    log_text = _read_file(APP_LOG_FILE)

    debug_count = sum(1 for line in log_text.splitlines() if "DEBUG" in line)
    error_count = sum(1 for line in log_text.splitlines() if "ERROR" in line)

    assert debug_count == 3, (
        f"app.log should initially contain 3 DEBUG lines, found {debug_count}."
    )
    assert error_count == 2, (
        f"app.log should initially contain 2 ERROR lines, found {error_count}."
    )