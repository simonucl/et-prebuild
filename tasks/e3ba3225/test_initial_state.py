# test_initial_state.py
#
# This pytest suite validates the initial filesystem state **before**
# the student performs any actions for the “patch-level bump” exercise.
#
# The tests assert that:
#   • /home/user/project exists as a directory
#   • /home/user/project/VERSION contains exactly "1.4.2\n"
#   • /home/user/project/CHANGELOG.md contains the expected contents for 1.4.2 only
#   • /home/user/audit/version_bump.log is absent (no audit trail yet)
#
# Any deviation from this baseline will raise a clear, actionable failure.

from pathlib import Path
import pytest

PROJECT_DIR = Path("/home/user/project")
VERSION_FILE = PROJECT_DIR / "VERSION"
CHANGELOG_FILE = PROJECT_DIR / "CHANGELOG.md"
AUDIT_LOG = Path("/home/user/audit/version_bump.log")


def test_project_directory_exists():
    assert PROJECT_DIR.exists(), f"Required directory {PROJECT_DIR} is missing."
    assert PROJECT_DIR.is_dir(), f"{PROJECT_DIR} exists but is not a directory."


def test_version_file_initial_content():
    assert VERSION_FILE.exists(), f"Required file {VERSION_FILE} is missing."
    assert VERSION_FILE.is_file(), f"{VERSION_FILE} exists but is not a regular file."

    content = VERSION_FILE.read_text(encoding="utf-8")
    expected_content = "1.4.2\n"
    assert (
        content == expected_content
    ), (
        f"{VERSION_FILE} should contain exactly one line with '1.4.2' "
        f"followed by a newline. Found:\n{repr(content)}"
    )


def test_changelog_initial_content():
    assert CHANGELOG_FILE.exists(), f"Required file {CHANGELOG_FILE} is missing."
    assert CHANGELOG_FILE.is_file(), f"{CHANGELOG_FILE} exists but is not a regular file."

    content = CHANGELOG_FILE.read_text(encoding="utf-8")
    expected_content = (
        "# Changelog\n"
        "\n"
        "All notable changes to this project will be documented in this file.\n"
        "\n"
        "## [1.4.2] - 2023-08-20\n"
        "- Fixed security minor bug\n"
    )
    assert (
        content == expected_content
    ), (
        f"{CHANGELOG_FILE} does not match the expected initial contents.\n\n"
        "Expected:\n"
        f"{repr(expected_content)}\n\nFound:\n{repr(content)}"
    )


def test_audit_log_absent():
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} should not exist before the student runs the task. "
        "Remove or rename it so the initial state is clean."
    )