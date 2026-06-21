# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state for the
# “project-docs” repository before the student performs any action.
#
# It intentionally FAILS if anything from the desired *final* state already
# exists.  In other words, it enforces that the starting point matches the
# specification’s “Current repository state” verbatim.

import os
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project-docs")
VERSION_FILE = PROJECT_ROOT / "VERSION"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"
TOOLS_DIR = PROJECT_ROOT / "tools"
BUMP_SCRIPT = TOOLS_DIR / "bump_version.sh"
LOGS_DIR = PROJECT_ROOT / ".logs"
HISTORY_LOG = LOGS_DIR / "bump_history.log"


def test_project_root_exists_and_is_dir():
    assert PROJECT_ROOT.exists(), (
        f"Expected directory {PROJECT_ROOT} to exist in the initial state."
    )
    assert PROJECT_ROOT.is_dir(), (
        f"{PROJECT_ROOT} exists but is not a directory."
    )


def test_version_file_contents():
    assert VERSION_FILE.exists(), (
        f"Expected VERSION file at {VERSION_FILE} to exist in the initial state."
    )
    assert VERSION_FILE.is_file(), (
        f"{VERSION_FILE} exists but is not a regular file."
    )

    expected_content = "1.4.2\n"
    actual_content = VERSION_FILE.read_text()
    assert actual_content == expected_content, (
        "VERSION file content is incorrect for the initial state.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Found:    {repr(actual_content)}"
    )


def test_changelog_initial_contents():
    assert CHANGELOG_FILE.exists(), (
        f"Expected CHANGELOG.md at {CHANGELOG_FILE} to exist in the initial state."
    )
    assert CHANGELOG_FILE.is_file(), (
        f"{CHANGELOG_FILE} exists but is not a regular file."
    )

    expected_content = (
        "# Changelog\n\n"
        "All notable changes to this project will be documented in this file "
        "following Keep a Changelog principles.\n\n"
        "## [1.4.2] - 2024-01-10\n"
        "### Changed\n"
        "- Tweaked API docs.\n"
    )
    actual_content = CHANGELOG_FILE.read_text()
    assert actual_content == expected_content, (
        "CHANGELOG.md content does not match the expected initial state.\n"
        "---- Expected ----\n"
        f"{expected_content}\n"
        "---- Found ----\n"
        f"{actual_content}"
    )


def test_tools_directory_and_script_absent():
    assert not TOOLS_DIR.exists(), (
        f"Directory {TOOLS_DIR} should NOT exist in the initial state."
    )
    assert not BUMP_SCRIPT.exists(), (
        f"Script {BUMP_SCRIPT} should NOT exist in the initial state."
    )


def test_logs_directory_and_history_log_absent():
    assert not LOGS_DIR.exists(), (
        f"Directory {LOGS_DIR} should NOT exist in the initial state."
    )
    assert not HISTORY_LOG.exists(), (
        f"File {HISTORY_LOG} should NOT exist in the initial state."
    )