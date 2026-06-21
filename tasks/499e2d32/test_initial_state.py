# test_initial_state.py
#
# This test-suite validates that the initial operating-system / filesystem
# matches the expected “pre-task” state *before* the student executes any
# commands.  It checks:
#
# 1. The presence and exact contents of the INI configuration file located at
#      /home/user/build/config/app_release.ini
# 2. That the build-summary log file does **not** yet exist.
#
# Any deviation will cause a failing test with a clear, actionable message.

import os
import textwrap
import configparser
import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   
# --------------------------------------------------------------------------- #
CONFIG_PATH = "/home/user/build/config/app_release.ini"
LOGS_DIR = "/home/user/build/logs"
SUMMARY_LOG = os.path.join(LOGS_DIR, "build_summary.log")

EXPECTED_INI_CONTENT = textwrap.dedent("""\
    [App]
    versionCode=42
    versionName=2.3.1

    [Build]
    buildId=CI-5567
    target=release
""")

EXPECTED_VALUES = {
    ("App", "versionCode"): "42",
    ("App", "versionName"): "2.3.1",
    ("Build", "buildId"): "CI-5567",
}


# --------------------------------------------------------------------------- #
# Helper functions                                                            
# --------------------------------------------------------------------------- #
def read_raw_file(path: str) -> str:
    """Return the raw contents of *path*; fail if the file cannot be read."""
    if not os.path.isfile(path):
        pytest.fail(f"Expected file does not exist: {path!r}")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {path!r}: {exc}")


# --------------------------------------------------------------------------- #
# Tests                                                                       
# --------------------------------------------------------------------------- #
def test_config_ini_exists_with_exact_content():
    """
    The configuration file MUST exist and match the exact, canonical contents
    provided in the task description.  Any change (missing lines, spacing,
    etc.) indicates an invalid initial state.
    """
    raw = read_raw_file(CONFIG_PATH)

    assert raw == EXPECTED_INI_CONTENT, (
        "The file at {0} does not match the expected contents.\n\n"
        "Expected:\n{1!r}\n\nGot:\n{2!r}".format(
            CONFIG_PATH, EXPECTED_INI_CONTENT, raw
        )
    )


def test_config_ini_parses_and_contains_expected_values():
    """
    Sanity-check: verify that reading the INI with configparser yields the
    expected key–value pairs.  This supplements the exact-content test above
    and provides clearer failure messages if only the key values differ.
    """
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")

    for (section, key), expected_value in EXPECTED_VALUES.items():
        assert parser.has_section(section), (
            f"INI file is missing section [{section}]."
        )
        assert parser.has_option(section, key), (
            f"INI file is missing key '{key}' in section [{section}]."
        )
        actual_value = parser.get(section, key)
        assert actual_value == expected_value, (
            f"INI value mismatch for [{section}] {key!s} : "
            f"expected {expected_value!r}, got {actual_value!r}"
        )


def test_summary_log_does_not_yet_exist():
    """
    Before the student runs their single-line command, the summary log file
    must not exist.  Its presence would indicate that the action has already
    been performed or that the test environment is polluted.
    """
    assert not os.path.exists(SUMMARY_LOG), (
        f"The log file {SUMMARY_LOG!r} already exists, "
        "but it should not be present before the student performs the task."
    )