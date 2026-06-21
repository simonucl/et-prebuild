# test_initial_state.py
#
# Pytest suite that validates the initial, pre-task state of the OS / file-system
# for the “documentation version bump” exercise.  These tests **must** pass
# before the student performs any actions.  Failures clearly report what is
# missing or incorrect.
#
# Requirements checked:
#   1. /home/user/project            — directory exists
#   2. /home/user/project/VERSION    — file exists and contains “1.2.3\n”
#   3. /home/user/project/CHANGELOG.md
#        — file exists and contains the exact, pre-task contents
#   4. /home/user/project/update.log — file must *not* exist yet
#
# Only the Python stdlib and pytest are used.

import os
import pytest

PROJECT_DIR = "/home/user/project"
VERSION_FILE = os.path.join(PROJECT_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(PROJECT_DIR, "CHANGELOG.md")
UPDATE_LOG_FILE = os.path.join(PROJECT_DIR, "update.log")

EXPECTED_VERSION_CONTENT = "1.2.3\n"

# Keep the exact text (including blank lines and trailing newline) of the
# initial CHANGELOG.md so that spacing-sensitive tests can compare verbatim.
EXPECTED_CHANGELOG_CONTENT = (
    "# Changelog\n"
    "\n"
    "## [1.2.3] - 2023-06-15\n"
    "### Added\n"
    "- Initial release of the documentation set.\n"
)


def _read_file(path):
    """Utility that reads a file in text-mode using UTF-8."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Required directory {PROJECT_DIR!r} is missing. "
        "The initial repository must already be present."
    )


def test_version_file_exists_and_content():
    assert os.path.isfile(VERSION_FILE), (
        f"File {VERSION_FILE!r} is missing. "
        "It must exist before the task begins."
    )
    content = _read_file(VERSION_FILE)
    assert content == EXPECTED_VERSION_CONTENT, (
        f"{VERSION_FILE} has unexpected contents.\n"
        f"Expected: {EXPECTED_VERSION_CONTENT!r}\n"
        f"Found:    {content!r}"
    )


def test_changelog_file_exists_and_content():
    assert os.path.isfile(CHANGELOG_FILE), (
        f"File {CHANGELOG_FILE!r} is missing. "
        "It must exist before the task begins."
    )
    content = _read_file(CHANGELOG_FILE)
    assert content == EXPECTED_CHANGELOG_CONTENT, (
        f"{CHANGELOG_FILE} contents do not match the expected initial state.\n"
        "If you have already modified this file, restore it before running the task."
    )


def test_update_log_does_not_exist_yet():
    assert not os.path.exists(UPDATE_LOG_FILE), (
        f"{UPDATE_LOG_FILE!r} should *not* exist before the student performs "
        "the update. Its presence indicates premature modifications."
    )