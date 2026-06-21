# test_initial_state.py
#
# Pytest suite that validates the initial state of the filesystem **before**
# the student runs any commands.  The tests make sure that the provided Markdown
# sources are present with the exact expected contents and that no lint output
# directory/file exists yet.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DOCS_DIR = HOME / "docs"

# --------------------------------------------------------------------------- #
# Helpers & fixtures
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def docs_path() -> Path:
    """Return the /home/user/docs path object."""
    return DOCS_DIR


def read_file_lines(path: Path):
    """Return the list of lines without their trailing newline characters."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read().splitlines()


# --------------------------------------------------------------------------- #
# Expected data
# --------------------------------------------------------------------------- #
EXPECTED_FILES_CONTENT = {
    "introduction.md": [
        "# Introduction to Our Deployment Process",
        "",
        "This document describes how to deploy the application.",
        "It covers prerequisites, environment variables, and step-by-step procedures that ensure a smooth rollout to production.",
    ],
    "deploy_guide.md": [
        "# Deployment Guide",
        "Make sure you have completed all unit tests, integration tests, and performance benchmarks before proceeding to deployment.",
    ],
    "changelog.md": [
        "# Changelog",
        "## [1.0.1] - 2023-04-21",
        "- Fixed bug in authentication.",
        "- Improved latency.",
        "- Added support for distributed tracing which lets the system gracefully handle and visualize end-to-end request flow, even under high load.",
    ],
    "README.md": [
        "# Project Documentation",
    ],
}

EXPECTED_FILENAMES = set(EXPECTED_FILES_CONTENT.keys())


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_docs_directory_exists(docs_path: Path):
    assert docs_path.exists(), f"Expected directory {docs_path} to exist."
    assert docs_path.is_dir(), f"Expected {docs_path} to be a directory."


def test_lint_directory_does_not_exist(docs_path: Path):
    lint_dir = docs_path / "lint"
    assert not lint_dir.exists(), (
        "The directory /home/user/docs/lint must NOT exist before the task is executed. "
        "Found an existing directory or file at that path."
    )


def test_expected_markdown_files_present(docs_path: Path):
    missing = [name for name in EXPECTED_FILENAMES if not (docs_path / name).is_file()]
    assert not missing, (
        "The following expected Markdown files are missing in /home/user/docs: "
        f"{', '.join(missing)}"
    )


def test_no_unexpected_entries_in_docs_directory(docs_path: Path):
    """Fail if there are extra files or any sub-directories in /home/user/docs."""
    unexpected_entries = []
    for entry in docs_path.iterdir():
        if entry.name not in EXPECTED_FILENAMES:
            unexpected_entries.append(entry.name)
    # Allow exactly the expected files; no extra files or directories are allowed.
    assert not unexpected_entries, (
        "Found unexpected files or directories in /home/user/docs: "
        f"{', '.join(sorted(unexpected_entries))}"
    )


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_FILES_CONTENT.items())
def test_markdown_file_contents(docs_path: Path, filename: str, expected_lines: list[str]):
    """Validate that each file's content matches the specification exactly."""
    file_path = docs_path / filename
    assert file_path.exists(), f"Expected file {file_path} to exist."
    assert file_path.is_file(), f"Expected {file_path} to be a regular file."

    actual_lines = read_file_lines(file_path)

    # Line count check
    assert (
        len(actual_lines) == len(expected_lines)
    ), f"File {filename} has {len(actual_lines)} lines but {len(expected_lines)} were expected."

    # Content check line by line for clear diff output
    for idx, (exp, act) in enumerate(zip(expected_lines, actual_lines), start=1):
        assert (
            act == exp
        ), f"Mismatch in {filename} on line {idx}.\nExpected: {exp!r}\nActual:   {act!r}"