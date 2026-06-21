# test_initial_state.py
#
# Pytest suite to validate the initial filesystem state
# BEFORE the student runs their single-line shell command.
#
# Checks performed:
#   1. /home/user/cicd/config directory exists.
#   2. /home/user/cicd/config/build_settings.ini exists
#      and its byte-for-byte contents are exactly as specified.
#   3. /home/user/cicd/output directory does NOT yet exist.
#
# These tests deliberately avoid looking for any output files
# that the student is expected to create later.

import pathlib
import pytest

CONFIG_DIR = pathlib.Path("/home/user/cicd/config")
INI_FILE = CONFIG_DIR / "build_settings.ini"
OUTPUT_DIR = pathlib.Path("/home/user/cicd/output")

# Expected byte-exact contents of build_settings.ini, including
# all blank lines and trailing newline at EOF.
EXPECTED_INI_CONTENT = (
    "[pipeline]\n"
    "name = core-build\n"
    "version = 1.4.3-beta\n"
    "runner = docker\n"
    "\n"
    "[artifacts]\n"
    "bucket = ci-build-artifacts\n"
    "retention_days = 14\n"
    "\n"
)


def test_config_directory_exists():
    """The configuration directory must already exist."""
    assert CONFIG_DIR.is_dir(), (
        f"Required directory {CONFIG_DIR} is missing. "
        "The initial repository layout is not as expected."
    )


def test_ini_file_exists():
    """The INI configuration file must already exist."""
    assert INI_FILE.is_file(), (
        f"Expected INI file {INI_FILE} is missing. "
        "The student cannot proceed without this file."
    )


def test_ini_file_contents_exact():
    """The INI file must match the precise expected contents."""
    with INI_FILE.open("r", encoding="utf-8") as fp:
        actual = fp.read()

    # Show a helpful diff if contents differ
    if actual != EXPECTED_INI_CONTENT:
        import difflib

        diff = "\n".join(
            difflib.unified_diff(
                EXPECTED_INI_CONTENT.splitlines(keepends=True),
                actual.splitlines(keepends=True),
                fromfile="expected",
                tofile="actual",
            )
        )
        pytest.fail(
            "The contents of build_settings.ini do not match the expected "
            "initial state. Unified diff:\n" + diff
        )


def test_output_directory_absent():
    """The /home/user/cicd/output directory must not yet exist."""
    assert not OUTPUT_DIR.exists(), (
        f"Directory {OUTPUT_DIR} already exists, but it should be created "
        "by the student's command. Ensure the environment starts clean."
    )