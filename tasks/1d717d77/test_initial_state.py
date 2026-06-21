# test_initial_state.py
#
# This pytest suite validates that the operating-system state **before**
# the student begins the task is exactly as expected.
#
# It checks only the *pre-task* requirements:
#   • The project directory /home/user/myutil exists.
#   • The VERSION file exists and contains “1.2.3”.
#   • The CHANGELOG.md file exists and its first visible line is the
#     heading “## [1.2.3] – 2023-04-01”.
#
# It deliberately does NOT check for any of the files the student is
# supposed to create or modify as part of the task (e.g. bump.log or
# the updated version/changelog), in accordance with the grading rules.

import os
from pathlib import Path

import pytest

HOME_DIR = Path("/home/user")
PROJECT_DIR = HOME_DIR / "myutil"
VERSION_FILE = PROJECT_DIR / "VERSION"
CHANGELOG_FILE = PROJECT_DIR / "CHANGELOG.md"

EXPECTED_VERSION_TEXT = "1.2.3"
EXPECTED_CHANGELOG_HEADING = "## [1.2.3] – 2023-04-01"  # includes U+2013 en dash


def _read_first_visible_line(path: Path) -> str:
    """
    Return the first non-empty line from the given file,
    stripped of its trailing newline.
    """
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():            # skip blank lines
                return line.rstrip("\n").rstrip("\r")
    return ""  # file was empty / only blank lines


def test_project_directory_exists():
    assert PROJECT_DIR.exists() and PROJECT_DIR.is_dir(), (
        f"Expected project directory at {PROJECT_DIR} is missing."
    )


def test_version_file_content():
    assert VERSION_FILE.exists() and VERSION_FILE.is_file(), (
        f"Expected VERSION file at {VERSION_FILE} is missing."
    )

    content = VERSION_FILE.read_text(encoding="utf-8").strip()
    assert content == EXPECTED_VERSION_TEXT, (
        f"VERSION file should contain exactly '{EXPECTED_VERSION_TEXT}', "
        f"but found '{content}'."
    )


def test_changelog_initial_heading():
    assert CHANGELOG_FILE.exists() and CHANGELOG_FILE.is_file(), (
        f"Expected CHANGELOG.md at {CHANGELOG_FILE} is missing."
    )

    first_line = _read_first_visible_line(CHANGELOG_FILE)
    assert first_line == EXPECTED_CHANGELOG_HEADING, (
        "The first visible line of CHANGELOG.md is incorrect.\n"
        f"Expected: '{EXPECTED_CHANGELOG_HEADING}'\n"
        f"Found:    '{first_line}'"
    )