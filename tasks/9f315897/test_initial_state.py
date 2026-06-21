# test_initial_state.py
#
# This test-suite verifies that the repository is **still** in its original,
# pre-exercise state.  If any of these tests fail it means the student has
# already modified something or the exercise scaffold is broken.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
PROJECT_DIR = HOME / "projects" / "alpha-tool"

VERSION_FILE   = PROJECT_DIR / "VERSION"
CHANGELOG_FILE = PROJECT_DIR / "CHANGELOG.md"
TODO_FILE      = PROJECT_DIR / "TODO.md"
LOG_FILE       = HOME / "version_bump.log"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def read_text(path: Path) -> str:
    """Read *binary* then decode as UTF-8 without altering newlines."""
    data = path.read_bytes()
    return data.decode("utf-8")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_repository_structure():
    assert PROJECT_DIR.is_dir(), (
        f"Expected project directory {PROJECT_DIR} to exist and be a directory."
    )

    for f in (VERSION_FILE, CHANGELOG_FILE, TODO_FILE):
        assert f.exists(), f"Expected file {f} to exist."


def test_version_file_content():
    """
    The VERSION file must *still* contain the original version “1.2.3”.
    """
    content = read_text(VERSION_FILE)
    expected_line = "1.2.3\n"
    assert content == expected_line, (
        "VERSION file is not in the expected initial state.\n"
        f"Expected exact content:\n{expected_line!r}\n"
        f"Got:\n{content!r}"
    )


def test_changelog_initial_state():
    """
    CHANGELOG.md must have exactly the original 1.2.0 section and must *not*
    yet contain a 1.3.0 section.
    """
    text = read_text(CHANGELOG_FILE)

    # Basic structure checks
    assert text.startswith("# Changelog\n"), (
        "CHANGELOG.md should start with '# Changelog'"
    )

    assert "## [1.2.0] - 2023-07-07" in text, (
        "CHANGELOG.md is missing the 1.2.0 section."
    )

    # There should be NO 1.3.0 section yet
    assert "## [1.3.0]" not in text, (
        "Found a 1.3.0 section in CHANGELOG.md, but the student has "
        "not performed the bump yet."
    )

    # Exact expected initial content for 1.2.0 section
    expected_initial = (
        "# Changelog\n\n"
        "## [1.2.0] - 2023-07-07\n"
        "- Initial public release\n"
    )
    assert text == expected_initial, (
        "CHANGELOG.md does not match the expected initial content.\n\n"
        "Expected:\n"
        f"{expected_initial!r}\n\nGot:\n{text!r}"
    )


def test_todo_file_initial_state():
    """
    TODO.md must still contain the original three todo items.
    """
    content = read_text(TODO_FILE)

    expected = (
        "- Add support for YAML export\n"
        "- Refactor config parser\n"
        "- Improve CLI help text\n"
    )

    assert content == expected, (
        "TODO.md is not in the expected initial state.\n\n"
        "Expected:\n"
        f"{expected!r}\n\nGot:\n{content!r}"
    )


def test_no_version_bump_log_yet():
    """
    The version_bump.log file must NOT exist before the student starts the task.
    """
    assert not LOG_FILE.exists(), (
        f"File {LOG_FILE} already exists, but it should be created only after "
        "the version bump is performed."
    )