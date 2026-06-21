# test_initial_state.py
"""
pytest suite that validates the *initial* operating-system / filesystem state
prior to the student running any commands.

The tests assert that:
1. /home/user/docs exists and is a directory.
2. Exactly three Markdown files are present directly inside that directory.
3. Each Markdown file contains the expected, line-accurate content.

NOTE:
* We deliberately do NOT look for the eventual output file
  (/home/user/docs/security-scan.log) as per the grading rules.
* Only stdlib and pytest are used.
"""
import pathlib
import pytest

DOCS_DIR = pathlib.Path("/home/user/docs").resolve()

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_lines(path):
    """
    Return a list of lines **without** their trailing newline characters.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh.readlines()]


# --------------------------------------------------------------------------- #
# Expected state description
# --------------------------------------------------------------------------- #
EXPECTED_FILES = {
    "setup.md": [
        "# Project Setup",
        "Please set the API_KEY environment variable before running.",
    ],
    "credentials.md": [
        "# Credentials",
        "Do not hardcode passwords in source code.",
        "Store secrets in environment variables.",
    ],
    "readme.md": [
        "# Welcome",
        "This project uses open data.",
    ],
}


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_docs_directory_exists():
    assert DOCS_DIR.exists(), f"Required directory '{DOCS_DIR}' is missing."
    assert DOCS_DIR.is_dir(), f"'{DOCS_DIR}' exists but is not a directory."


def test_markdown_files_present_and_only_expected():
    md_files = {p.name for p in DOCS_DIR.iterdir() if p.is_file() and p.suffix == ".md"}
    missing = set(EXPECTED_FILES) - md_files
    extra = md_files - set(EXPECTED_FILES)

    assert not missing, (
        "The following expected .md files are missing from "
        f"'{DOCS_DIR}': {', '.join(sorted(missing))}"
    )
    assert not extra, (
        "Unexpected .md files found in "
        f"'{DOCS_DIR}': {', '.join(sorted(extra))}"
    )


@pytest.mark.parametrize("filename, expected_lines", EXPECTED_FILES.items())
def test_markdown_file_contents(filename, expected_lines):
    file_path = DOCS_DIR / filename
    assert file_path.exists(), f"File '{file_path}' is missing."
    assert file_path.is_file(), f"'{file_path}' exists but is not a regular file."

    actual_lines = read_lines(file_path)
    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of '{file_path}' do not match the expected initial state.\n"
        f"Expected ({len(expected_lines)} lines):\n  "
        + "\n  ".join(expected_lines)
        + "\n\nActual ({len(actual_lines)} lines):\n  "
        + "\n  ".join(actual_lines)
    )