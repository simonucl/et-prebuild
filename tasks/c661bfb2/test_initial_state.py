# test_initial_state.py
#
# This test-suite validates that the repository is in the **initial**
# state described in the assignment *before* the student performs any
# modifications.  It verifies the presence and exact content of the
# VERSION file and the CHANGELOG.md file.
#
# If any of these assertions fail, the starting point does **not** match
# the specification and the student should not begin the task.

import pathlib
import re
import pytest

PROJECT_ROOT = pathlib.Path("/home/user/project")
VERSION_FILE = PROJECT_ROOT / "VERSION"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"


def read_text(path: pathlib.Path) -> str:
    """Utility to read a file as UTF-8, raising a clear error if missing."""
    assert path.exists(), f"Expected file at {path} does not exist."
    assert path.is_file(), f"Expected {path} to be a regular file."
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"Could not decode {path} as UTF-8: {exc}")


def test_version_file_is_unchanged():
    """
    The VERSION file must exist and contain exactly one line: '1.4.2'
    followed by a single trailing newline.
    """
    content = read_text(VERSION_FILE)
    assert (
        content == "1.4.2\n"
    ), "VERSION file should contain exactly '1.4.2' followed by a newline."


def test_changelog_has_original_contents_only():
    """
    The CHANGELOG.md must contain the original 1.4.2 section and *must not*
    yet contain a 1.4.3 entry.  The original file is expected to look like
    this (blank lines matter):

        # Changelog
        All notable changes to this project will be documented in this file.

        ## [1.4.2] - 2023-12-14
        ### Changed
        * Switched default output from JSON to YAML.
    """
    text = read_text(CHANGELOG_FILE)

    # Verify header line.
    header_pattern = r"^# Changelog\s*$"
    assert re.match(
        header_pattern, text.splitlines()[0]
    ), "CHANGELOG.md must start with '# Changelog'."

    # Ensure the 1.4.2 section header is present.
    assert (
        "## [1.4.2] - 2023-12-14" in text
    ), "CHANGELOG.md does not contain the expected 1.4.2 section header."

    # Ensure the 'Switched default output...' bullet is present.
    assert (
        "* Switched default output from JSON to YAML." in text
    ), "CHANGELOG.md is missing the expected bullet for the 1.4.2 release."

    # The file should NOT yet mention 1.4.3 anywhere.
    forbidden_version = "## [1.4.3]"
    assert (
        forbidden_version not in text
    ), "CHANGELOG.md already contains a 1.4.3 section—initial state is incorrect."