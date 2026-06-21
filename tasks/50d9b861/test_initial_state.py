# test_initial_state.py
"""
Pytest suite that validates the *initial* repository/OS state
for the “db-backup” project **before** the student performs any
changes.

If any of these tests fail it means the starting point is already
wrong and the subsequent tasks cannot be graded reliably.
"""
from pathlib import Path
import pytest

HOME = Path("/home/user")
REPO_ROOT = HOME / "db-backup"
VERSION_FILE = REPO_ROOT / "version.txt"
CHANGELOG_FILE = REPO_ROOT / "CHANGELOG.md"
AUDIT_LOG = HOME / "version_bump.log"


def test_repository_directory_exists():
    assert REPO_ROOT.is_dir(), (
        f"Expected repository directory {REPO_ROOT} to exist. "
        "It is missing or not a directory."
    )


def test_version_file_initial_state():
    assert VERSION_FILE.is_file(), (
        f"Expected version file {VERSION_FILE} to exist. It is missing."
    )

    content = VERSION_FILE.read_bytes()
    expected = b"1.2.3\n"
    assert (
        content == expected
    ), (
        f"{VERSION_FILE} should contain exactly {expected!r} "
        f"but contains {content!r}."
    )


def test_changelog_initial_state():
    assert CHANGELOG_FILE.is_file(), (
        f"Expected changelog file {CHANGELOG_FILE} to exist. It is missing."
    )

    text = CHANGELOG_FILE.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Expected first three non-empty lines of the changelog
    expected_start = [
        "## [1.2.3] - 2023-09-10",
        "### Fixed",
        "- Corrected cron schedule for nightly backups",
    ]

    # Filter out leading empty lines (should not be any, but be defensive)
    non_empty_lines = [ln for ln in lines if ln.strip()][:3]
    assert non_empty_lines == expected_start, (
        "The first lines of CHANGELOG.md do not match the expected "
        "initial content for version 1.2.3.\n"
        f"Expected: {expected_start}\n"
        f"Found:    {non_empty_lines}"
    )

    assert (
        "1.3.0" not in text
    ), "CHANGELOG.md already contains '1.3.0'; initial state must NOT have the new version."


def test_audit_log_not_present_yet():
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} should NOT exist in the initial state. "
        "It must be created by the student during the task."
    )