# test_initial_state.py
#
# This test-suite verifies that the *initial* filesystem state needed for the
# Markdown-heading aggregation task is present.  It intentionally performs
# NO checks on any output directory or file that the student is expected to
# create later (/home/user/docs/summary/HEADINGS.md).
#
# The suite fails early and with clear, actionable messages if something
# necessary is missing or malformed.

import os
from pathlib import Path

import pytest

# Constants -------------------------------------------------------------------

SOURCE_DIR = Path("/home/user/docs/source")

# Mapping of <filename>  -->  <expected first-level heading line>
EXPECTED_FILES = {
    "intro.md": "# Introduction",
    "setup.md": "# Setup",
    "usage.md": "# Usage",
    "duplicateHeading.md": "# Introduction",
}


# Helper ----------------------------------------------------------------------

def _read_first_nonempty_line(path: Path) -> str:
    """
    Return the first non-empty line (stripped of its trailing newline) from *path*.
    Raises AssertionError if the file is empty or only contains blank lines.
    """
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            stripped = line.rstrip("\n")
            if stripped.strip():        # at least one non-whitespace char
                return stripped
    raise AssertionError(f"{path} exists but does not contain any non-empty lines.")


# Tests -----------------------------------------------------------------------

def test_source_directory_exists():
    assert SOURCE_DIR.exists(), (
        f"Required directory {SOURCE_DIR} is missing. "
        "It must contain the Markdown source files."
    )
    assert SOURCE_DIR.is_dir(), f"{SOURCE_DIR} exists but is not a directory."


@pytest.mark.parametrize("filename,expected_heading", EXPECTED_FILES.items())
def test_each_required_markdown_file_exists_and_starts_with_correct_heading(filename, expected_heading):
    file_path = SOURCE_DIR / filename
    assert file_path.exists(), f"Expected file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    first_line = _read_first_nonempty_line(file_path)
    assert first_line == expected_heading, (
        f"{file_path} does not start with the expected first-level heading.\n"
        f"Expected: {expected_heading!r}\nFound:    {first_line!r}"
    )


def test_no_missing_expected_files():
    """
    Ensure that *at least* the expected Markdown files are present.
    Having additional .md files is allowed, but the expected core files
    must be there.
    """
    present_files = {p.name for p in SOURCE_DIR.glob("*.md")}
    missing = set(EXPECTED_FILES) - present_files
    assert not missing, (
        "The following required Markdown files are missing from "
        f"{SOURCE_DIR}: {', '.join(sorted(missing))}"
    )