# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state **before**
# the student performs any actions described in the task.
#
# The checks intentionally *fail* if the starting state is not exactly
# as required, so that the student gets clear feedback before attempting
# the task itself.
#
# Requirements verified:
#   1. /home/user/work_in_progress   exists and is a directory.
#   2. It contains *exactly* the three markdown files:
#        - overview.md
#        - install.md
#        - faq.md
#      (no more, no fewer; they must be regular files, not dirs/symlinks)
#   3. The contents of those files match the specification.
#   4. /home/user/doc_publication   must *not* exist yet.
#
# Only pytest and the standard library are used.

import os
from pathlib import Path

WORK_DIR = Path("/home/user/work_in_progress")
PUB_DIR = Path("/home/user/doc_publication")

EXPECTED_FILES = {
    "overview.md": [
        "# Project Overview",
        "This document provides an overview of the project.",
        "TODO: expand details.",
    ],
    "install.md": [
        "# Installation Guide",
        "Follow these steps to install the application.",
        "Step 1: ...",
        "TODO: add screenshots.",
    ],
    "faq.md": [
        "# FAQ",
        "Frequently asked questions will go here.",
    ],
}


def test_work_dir_exists_and_is_dir():
    assert WORK_DIR.exists(), f"Required directory {WORK_DIR} does not exist."
    assert WORK_DIR.is_dir(), f"{WORK_DIR} exists but is not a directory."


def test_markdown_files_present_and_only_expected():
    # Collect actual markdown files (case-sensitive) inside work dir
    actual_files = sorted(
        f.name for f in WORK_DIR.iterdir() if f.is_file() and f.suffix == ".md"
    )

    expected_files_sorted = sorted(EXPECTED_FILES.keys())

    assert actual_files == expected_files_sorted, (
        "The Markdown files present in "
        f"{WORK_DIR} are {actual_files!r} but expected exactly "
        f"{expected_files_sorted!r}. Ensure no files are missing or extraneous."
    )


def test_each_expected_file_is_regular_file():
    for filename in EXPECTED_FILES:
        path = WORK_DIR / filename
        assert path.exists(), f"Expected file {path} is missing."
        assert path.is_file(), f"{path} exists but is not a regular file."


def _read_file_lines(path: Path):
    # Read file, strip trailing newline characters, but keep internal content.
    with path.open(encoding="utf-8") as fh:
        return [line.rstrip("\n\r") for line in fh.readlines()]


def test_contents_of_markdown_files():
    """
    Verify that the initial contents of each Markdown file match the spec.
    This guards against accidental modification of the starting data set.
    """
    for filename, expected_lines in EXPECTED_FILES.items():
        path = WORK_DIR / filename
        actual_lines = _read_file_lines(path)
        assert (
            actual_lines == expected_lines
        ), f"Contents of {path} differ from expected.\nExpected: {expected_lines!r}\nActual:   {actual_lines!r}"


def test_doc_publication_dir_does_not_yet_exist():
    assert not PUB_DIR.exists(), (
        f"Directory {PUB_DIR} should *not* exist before the task starts. "
        "It must be created by the student's solution."
    )