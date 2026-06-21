# test_initial_state.py
#
# Pytest suite that validates the _initial_ repository / filesystem state
# before the student performs any actions for the “capacity-planner” task.
#
# The expected initial state is:
#   • VERSION  file contains exactly “1.3.4\n”.
#   • CHANGELOG.md contains only the 1.3.4 section (and must NOT mention 1.4.0).
#   • bump.log must not exist yet.
#
# Any deviation from this baseline will fail with an informative message.

import os
from pathlib import Path
import pytest

REPO_ROOT = Path("/home/user/projects/capacity-planner")
VERSION_FILE = REPO_ROOT / "VERSION"
CHANGELOG_FILE = REPO_ROOT / "CHANGELOG.md"
BUMP_LOG_FILE = REPO_ROOT / "bump.log"

EXPECTED_VERSION_CONTENT = "1.3.4\n"
EXPECTED_CHANGELOG_CONTENT = (
    "# Changelog\n"
    "\n"
    "## [1.3.4] - 2023-03-20\n"
    "### Added\n"
    "- Initial support for CPU burst predictions.\n"
)


def test_repository_directory_exists():
    assert REPO_ROOT.is_dir(), (
        f"Expected repository directory {REPO_ROOT} to exist, "
        "but it is missing."
    )


def test_version_file_content():
    assert VERSION_FILE.is_file(), (
        f"Expected VERSION file at {VERSION_FILE} to exist, "
        "but it is missing."
    )

    content = VERSION_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_VERSION_CONTENT, (
        "VERSION file content is incorrect.\n"
        f"Expected exactly: {repr(EXPECTED_VERSION_CONTENT)}\n"
        f"Got:              {repr(content)}"
    )


def test_changelog_file_content():
    assert CHANGELOG_FILE.is_file(), (
        f"Expected CHANGELOG.md at {CHANGELOG_FILE} to exist, "
        "but it is missing."
    )

    content = CHANGELOG_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_CHANGELOG_CONTENT, (
        "CHANGELOG.md does not match the expected initial state.\n"
        "---- Expected ----\n"
        f"{EXPECTED_CHANGELOG_CONTENT}\n"
        "---- Got ----\n"
        f"{content}"
    )

    assert "1.4.0" not in content, (
        "CHANGELOG.md already contains a 1.4.0 entry, "
        "but this should only be added by the student."
    )


def test_bump_log_does_not_exist():
    assert not BUMP_LOG_FILE.exists(), (
        f"Found unexpected file {BUMP_LOG_FILE}. "
        "The bump.log file should only be created after the version bump."
    )