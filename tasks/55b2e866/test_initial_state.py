# test_initial_state.py
#
# This test-suite asserts the initial state of the operating system / file-system
# before the student runs any commands for the “missing translations” task.

import os
import re
from pathlib import Path

import pytest

ROOT_DIR = Path("/home/user/localization")
BUILD_LOG = ROOT_DIR / "build.log"

# ---------------------------------------------------------------------------
# Helper Regular Expression for the “missing translation” log lines
# ---------------------------------------------------------------------------

MISSING_RX = re.compile(
    r"""
    ^(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})     # full timestamp
    \s+WARN\s+\[i18n]\s+Missing\ key\s+'(?P<key>[A-Z0-9_]+)' # the key
    \s+in\s+locale\s+(?P<locale>[a-z]{2}_[A-Z]{2})           # locale code
    """,
    re.VERBOSE,
)

# ---------------------------------------------------------------------------
# Expected WARN lines shipped with the repository
# ---------------------------------------------------------------------------

EXPECTED_LINES = [
    ("2023-10-01 12:01:23", "WELCOME_MESSAGE", "es_ES"),
    ("2023-10-01 12:01:25", "GOODBYE_MESSAGE", "fr_FR"),
    ("2023-10-01 12:01:27", "LOGIN_BUTTON", "es_ES"),
]

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_localization_directory_exists():
    assert ROOT_DIR.exists(), (
        f"Required directory {ROOT_DIR!s} does not exist. "
        "The project’s localization files must be located here."
    )
    assert ROOT_DIR.is_dir(), f"{ROOT_DIR!s} exists but is not a directory."


def test_build_log_file_exists_and_is_file():
    assert BUILD_LOG.exists(), (
        f"The source build log {BUILD_LOG!s} is missing. "
        "It must be present before the exercise begins."
    )
    assert BUILD_LOG.is_file(), f"{BUILD_LOG!s} exists but is not a regular file."


def test_build_log_contains_expected_warn_lines():
    """The log must already contain the three reference WARN lines."""
    with BUILD_LOG.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Extract all matching WARN lines
    parsed = []
    for line in lines:
        m = MISSING_RX.match(line.rstrip("\n"))
        if m:
            parsed.append(
                (m.group("timestamp"), m.group("key"), m.group("locale"))
            )

    # Sanity check: there should be at least the reference three lines
    assert len(parsed) >= 3, (
        "The build log is expected to contain at least three "
        "'Missing key' WARN entries, but fewer were found."
    )

    # Verify that each expected line is present in the parsed output
    missing = [exp for exp in EXPECTED_LINES if exp not in parsed]
    assert not missing, (
        "The following expected WARN lines are not present in the build log:\n"
        + "\n".join(f"{ts} '{key}' {loc}" for ts, key, loc in missing)
    )


def test_no_output_file_preexisting():
    """The output file must not exist before the student runs their command."""
    output_file = ROOT_DIR / "missing_translations.log"
    assert not output_file.exists(), (
        f"{output_file!s} already exists, but it must be created "
        "only by the student’s solution."
    )