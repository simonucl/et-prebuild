# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student performs any action.  It asserts that the
# terraform-module directory and its seed files are present and
# contain the exact, unmodified contents specified in the task
# description.

import os
from pathlib import Path

import pytest

# Base directory that must already exist
MODULE_DIR = Path("/home/user/terraform-module").resolve()

# Expected initial file paths
VERSION_FILE = MODULE_DIR / "VERSION"
CHANGELOG_FILE = MODULE_DIR / "CHANGELOG.md"

# Expected initial contents
EXPECTED_VERSION_CONTENT = "0.4.5\n"

EXPECTED_CHANGELOG_CONTENT = (
    "# Changelog\n"
    "All notable changes to this project will be documented in this file.\n"
    "\n"
    "## [0.4.5] - 2023-08-01\n"
    "### Added\n"
    "- Initial support for cross-region replication.\n"
)


def _read_text(path: Path) -> str:
    """
    Helper that reads a text file using UTF-8 and returns its contents.

    Parameters
    ----------
    path : Path
        The path to the file to read.

    Returns
    -------
    str
        The complete file contents.
    """
    with path.open("r", encoding="utf-8") as fp:
        return fp.read()


def test_module_directory_exists():
    """
    The terraform-module directory must exist before any work starts.
    """
    assert MODULE_DIR.is_dir(), (
        f"Required directory {MODULE_DIR} is missing. "
        "The exercise expects this directory to exist before the student runs any command."
    )


def test_version_file_exists_with_expected_content():
    """
    Validate that the VERSION file exists and contains exactly the
    single line '0.4.5' followed by a newline—nothing more, nothing less.
    """
    assert VERSION_FILE.is_file(), (
        f"Expected file {VERSION_FILE} is missing."
    )

    content = _read_text(VERSION_FILE)
    assert content == EXPECTED_VERSION_CONTENT, (
        f"{VERSION_FILE} must initially contain exactly:\n"
        f"{EXPECTED_VERSION_CONTENT!r}\n"
        f"but found:\n{content!r}"
    )


def test_changelog_file_exists_with_expected_content():
    """
    Validate that CHANGELOG.md exists and matches the pristine seed
    content provided in the task description, without the yet-to-be-added
    0.4.6 section.
    """
    assert CHANGELOG_FILE.is_file(), (
        f"Expected file {CHANGELOG_FILE} is missing."
    )

    content = _read_text(CHANGELOG_FILE)
    assert content == EXPECTED_CHANGELOG_CONTENT, (
        f"{CHANGELOG_FILE} does not match the expected initial content.\n\n"
        "If this file has already been modified (for example, the 0.4.6 "
        "section was added prematurely), reset it so it contains exactly:\n\n"
        f"{EXPECTED_CHANGELOG_CONTENT!r}\n\n"
        f"but found:\n{content!r}"
    )