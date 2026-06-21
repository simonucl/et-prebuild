# test_initial_state.py
"""
Pytest suite to validate the initial on-disk state **before** the student
runs their one-liner.

The tests assert that:
1. The project directory /home/user/data_project exists.
2. /home/user/data_project/version.txt exists and contains exactly
   '1.3.5\\n'.
3. /home/user/data_project/CHANGELOG.md exists and matches the expected
   initial changelog (byte-for-byte).

Per the instructions we intentionally do **not** test for the presence or
absence of any output artifacts (e.g. bump_log.txt or the updated file
contents).
"""

import os
import pathlib
import re

import pytest

# Constants -------------------------------------------------------------------

PROJECT_DIR = pathlib.Path("/home/user/data_project")
VERSION_FILE = PROJECT_DIR / "version.txt"
CHANGELOG_FILE = PROJECT_DIR / "CHANGELOG.md"

EXPECTED_VERSION_LINE = "1.3.5\n"

EXPECTED_CHANGELOG = (
    "# Changelog\n"
    "\n"
    "## [1.3.5] - 2023-06-30\n"
    "- Added median calculation for quarterly_sales.csv\n"
)


# Helper ----------------------------------------------------------------------

def _read_text(path: pathlib.Path) -> str:
    """Read a text file using UTF-8 and return its contents."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


# Tests -----------------------------------------------------------------------

def test_project_directory_exists():
    """Ensure the main project directory exists and is a directory."""
    assert PROJECT_DIR.exists(), f"Required directory {PROJECT_DIR} is missing."
    assert PROJECT_DIR.is_dir(), f"{PROJECT_DIR} exists but is not a directory."


def test_version_file_initial_state():
    """
    version.txt must exist and contain exactly '1.3.5\\n'.
    Also validate that the line matches the semantic version pattern.
    """
    assert VERSION_FILE.exists(), f"Expected file {VERSION_FILE} is missing."
    assert VERSION_FILE.is_file(), f"{VERSION_FILE} exists but is not a file."

    contents = _read_text(VERSION_FILE)
    assert (
        contents == EXPECTED_VERSION_LINE
    ), (
        "version.txt does not contain the expected initial version.\n"
        f"Expected: {repr(EXPECTED_VERSION_LINE)}\n"
        f"Found:    {repr(contents)}"
    )

    semver_pattern = r"^\d+\.\d+\.\d+\n$"
    assert re.match(
        semver_pattern, contents
    ), "version.txt does not match the semantic version format 'MAJOR.MINOR.PATCH' followed by a newline."


def test_changelog_initial_state():
    """
    CHANGELOG.md must exist and match the exact initial content snapshot.
    """
    assert CHANGELOG_FILE.exists(), f"Expected file {CHANGELOG_FILE} is missing."
    assert CHANGELOG_FILE.is_file(), f"{CHANGELOG_FILE} exists but is not a file."

    contents = _read_text(CHANGELOG_FILE)
    assert (
        contents == EXPECTED_CHANGELOG
    ), (
        "CHANGELOG.md does not match the expected initial content.\n"
        "------ Expected (↓) ------\n"
        f"{EXPECTED_CHANGELOG}\n"
        "------ Found (↓) ------\n"
        f"{contents}"
    )