# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present **before** the student performs any version-bump actions.
#
# It checks:
#   1. The directory /home/user/sys-hardening/ exists.
#   2. The VERSION file exists and contains exactly the single line “2.1.9”.
#   3. The CHANGELOG.md file exists and its first ten lines are exactly those
#      specified in the task description.
#
# NOTE:  We deliberately do *not* look for the file “/home/user/version_bump.log”
#        nor do we check for any post-task versions of the files, in order to
#        comply with the rule “DO NOT test for any of the output files or
#        directories.”  We verify only the required *starting* state.

from pathlib import Path

import pytest

ROOT = Path("/home/user/sys-hardening")
VERSION_FILE = ROOT / "VERSION"
CHANGELOG_FILE = ROOT / "CHANGELOG.md"

# Expected contents for the initial CHANGELOG.md (first 10 lines, **exactly**)
_EXPECTED_CHANGELOG_LINES = [
    "# Change Log",
    "All notable changes to this project will be documented in this file.",
    "",
    "## [Unreleased]",
    "### Added",
    "- Implemented new SSL cipher suites.",
    "- Added automated backup rotation.",
    "",
    "### Fixed",
    "- Corrected typo in Nginx worker_connections directive.",
]


def _read_file_lines(path: Path):
    """Return the file’s lines without trailing newline characters."""
    with path.open("r", encoding="utf-8") as fp:
        return [line.rstrip("\n") for line in fp]


def test_repository_directory_exists():
    assert ROOT.exists(), (
        f"Required directory {ROOT} is missing. "
        "The sys-hardening repository must be present at this path."
    )
    assert ROOT.is_dir(), f"{ROOT} exists but is not a directory."


def test_version_file_initial_state():
    assert VERSION_FILE.exists(), (
        f"Expected VERSION file at {VERSION_FILE} is missing. "
        "It should contain the starting version number."
    )
    assert VERSION_FILE.is_file(), f"{VERSION_FILE} exists but is not a regular file."

    lines = _read_file_lines(VERSION_FILE)
    assert len(lines) == 1, (
        f"{VERSION_FILE} should contain exactly one line, found {len(lines)} lines."
    )
    assert lines[0] == "2.1.9", (
        f"{VERSION_FILE} should contain '2.1.9' as its sole line. "
        f"Found: {lines[0]!r}"
    )


def test_changelog_initial_state():
    assert CHANGELOG_FILE.exists(), (
        f"Expected CHANGELOG at {CHANGELOG_FILE} is missing."
    )
    assert CHANGELOG_FILE.is_file(), f"{CHANGELOG_FILE} exists but is not a regular file."

    lines = _read_file_lines(CHANGELOG_FILE)

    # Validate that we have at least the required 10 lines
    assert len(lines) >= len(
        _EXPECTED_CHANGELOG_LINES
    ), (
        f"{CHANGELOG_FILE} should have at least "
        f"{len(_EXPECTED_CHANGELOG_LINES)} lines, found only {len(lines)}."
    )

    first_ten = lines[: len(_EXPECTED_CHANGELOG_LINES)]
    assert (
        first_ten == _EXPECTED_CHANGELOG_LINES
    ), (
        f"The first {len(_EXPECTED_CHANGELOG_LINES)} lines of {CHANGELOG_FILE} "
        "do not match the expected initial content.\n\n"
        "Expected:\n"
        + "\n".join(_EXPECTED_CHANGELOG_LINES)
        + "\n\nFound:\n"
        + "\n".join(first_ten)
    )