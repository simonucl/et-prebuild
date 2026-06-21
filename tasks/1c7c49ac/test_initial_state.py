# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# prior to the student making any modifications.  If any test fails,
# it means the starting point is already incorrect and the exercise
# cannot be completed as described.

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants describing the expected initial project layout and file contents
# ---------------------------------------------------------------------------

PROJECT_DIR = Path("/home/user/db-query-opt")

VERSION_PATH = PROJECT_DIR / "version.txt"
EXPECTED_VERSION_CONTENT = "2.4.0\n"  # single line, trailing newline

CHANGELOG_PATH = PROJECT_DIR / "CHANGELOG.md"
EXPECTED_CHANGELOG_CONTENT = (
    "# Changelog\n"
    "\n"
    "## [2.4.0] - 2023-04-10\n"
    "### Added\n"
    "- Support for composite indexes in query planner\n"
    "\n"
)

RELEASE_LOG_PATH = PROJECT_DIR / "release_actions.log"  # must NOT exist yet


# ---------------------------------------------------------------------------
# Helper assertions
# ---------------------------------------------------------------------------

def assert_file_exists(path: Path):
    assert path.exists(), f"Expected file {path} to exist but it does not."


def assert_file_not_exists(path: Path):
    assert not path.exists(), f"File {path} should NOT exist at the start."


def read_file(path: Path) -> str:
    with path.open("rt", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), (
        f"Directory {PROJECT_DIR} is missing. The project must start with this "
        "directory already present."
    )


def test_version_file_initial_contents():
    assert_file_exists(VERSION_PATH)
    actual = read_file(VERSION_PATH)
    assert (
        actual == EXPECTED_VERSION_CONTENT
    ), (
        f"{VERSION_PATH} has unexpected content.\n"
        f"Expected (repr): {EXPECTED_VERSION_CONTENT!r}\n"
        f"Actual   (repr): {actual!r}"
    )


def test_changelog_initial_contents():
    assert_file_exists(CHANGELOG_PATH)
    actual = read_file(CHANGELOG_PATH)
    assert (
        actual == EXPECTED_CHANGELOG_CONTENT
    ), (
        f"{CHANGELOG_PATH} has unexpected content.\n"
        "If this file is incorrect at the start, subsequent instructions will "
        "not match.\n"
        f"Expected (repr): {EXPECTED_CHANGELOG_CONTENT!r}\n"
        f"Actual   (repr): {actual!r}"
    )


def test_release_log_not_present_yet():
    assert_file_not_exists(RELEASE_LOG_PATH)