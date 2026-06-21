# test_initial_state.py
#
# Pytest suite that verifies the **initial** OS / filesystem state for the
# “user-accounts” micro-service *before* the student runs any command.
#
# DO NOT MODIFY THIS FILE.
# It purposefully asserts that the current version is 1.5.2 and that no
# artefacts for version 1.5.3 exist yet.

import pytest
from pathlib import Path

BASE_DIR = Path("/home/user/user-accounts")
VERSION_FILE = BASE_DIR / "VERSION"
CHANGELOG_FILE = BASE_DIR / "CHANGELOG.md"
UPGRADE_LOG_FILE = BASE_DIR / "upgrade.log"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _read_lines(path: Path):
    "Return file lines without trailing LF characters."
    return path.read_text(encoding="utf-8").splitlines()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_repository_directory_exists():
    assert BASE_DIR.exists(), (
        f"Required directory {BASE_DIR} is missing. "
        "The project repository must already be cloned here."
    )
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


def test_version_file_is_present_and_contains_1_5_2():
    assert VERSION_FILE.exists(), f"Version file {VERSION_FILE} is missing."
    assert VERSION_FILE.is_file(), f"{VERSION_FILE} exists but is not a regular file."

    lines = _read_lines(VERSION_FILE)
    assert lines == ["1.5.2"], (
        f"{VERSION_FILE} must contain exactly one line '1.5.2' (found: {lines!r})."
    )


def test_changelog_contains_expected_entries_and_no_1_5_3_yet():
    assert CHANGELOG_FILE.exists(), f"Changelog {CHANGELOG_FILE} is missing."
    assert CHANGELOG_FILE.is_file(), f"{CHANGELOG_FILE} exists but is not a regular file."

    lines = _read_lines(CHANGELOG_FILE)

    expected_block = [
        "## [1.5.2] - 2023-09-28",
        "- Improve password hashing",
        "",
        "## [1.5.1] - 2023-09-20",
        "- Add MFA enrolment command",
        "",
        "## [1.5.0] - 2023-09-15",
        "- Initial public release",
    ]

    # Ensure the beginning of the changelog matches the expected 1.5.2 block
    assert lines[: len(expected_block)] == expected_block, (
        f"The beginning of {CHANGELOG_FILE} does not match the expected "
        "1.5.2→1.5.0 history. Make sure the file has not been modified."
    )

    # Ensure *no* 1.5.3 entry is present yet
    full_text = "\n".join(lines)
    assert "## [1.5.3]" not in full_text, (
        f"{CHANGELOG_FILE} already contains a 1.5.3 section; "
        "this should not be present before the task is executed."
    )


def test_upgrade_log_does_not_yet_contain_1_5_3_entry():
    if not UPGRADE_LOG_FILE.exists():
        # It is acceptable for upgrade.log to be absent at the start.
        return

    assert UPGRADE_LOG_FILE.is_file(), (
        f"{UPGRADE_LOG_FILE} exists but is not a regular file."
    )

    contents = UPGRADE_LOG_FILE.read_text(encoding="utf-8")
    forbidden_line = "Bumped to 1.5.3 - Fix typo in account deletion confirmation"
    assert forbidden_line not in contents, (
        f"{UPGRADE_LOG_FILE} already contains the 1.5.3 upgrade note; "
        "it should only be added by the solution command."
    )