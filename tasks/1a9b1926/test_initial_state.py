# test_initial_state.py
#
# This test-suite verifies the pristine state of the filesystem **before**
# the student begins working on the task.  It intentionally checks *only*
# for the resources that must already exist; it does **not** reference any
# files the student is expected to create later (Makefile, bundle.tar.gz,
# build.log, …).

import os
from pathlib import Path

import pytest

ARTIFACTS_DIR = Path("/home/user/artifacts")

EXPECTED_FILES = {
    "notes.txt": "Meeting notes for Q1.\n",
    "changelog.txt": "v1.0 – initial release.\n",
    "license.txt": "MIT License\n",
}


def test_artifacts_directory_exists():
    assert ARTIFACTS_DIR.exists(), f"Required directory {ARTIFACTS_DIR} is missing."
    assert ARTIFACTS_DIR.is_dir(), f"{ARTIFACTS_DIR} exists but is not a directory."


def test_expected_files_present_and_unique():
    """Ensure exactly the expected three text files are present—nothing more, nothing less."""
    found = {p.name for p in ARTIFACTS_DIR.iterdir() if p.is_file()}

    # Compare set equality so we flag both missing and unexpected files.
    missing = set(EXPECTED_FILES) - found
    unexpected = found - set(EXPECTED_FILES)

    message_parts = []
    if missing:
        message_parts.append(f"Missing files: {', '.join(sorted(missing))}")
    if unexpected:
        message_parts.append(
            f"Unexpected extra files present: {', '.join(sorted(unexpected))}"
        )

    assert not message_parts, " | ".join(message_parts)


@pytest.mark.parametrize("filename, expected_line1", EXPECTED_FILES.items())
def test_file_contents_first_line(filename, expected_line1):
    """Verify that each expected text file has the correct first line."""
    file_path = ARTIFACTS_DIR / filename
    assert file_path.exists(), f"Expected file {file_path} is missing."

    with file_path.open("r", encoding="utf-8") as fp:
        first_line = fp.readline()
    assert (
        first_line == expected_line1
    ), f"File {file_path} has unexpected first line:\n  Expected: {expected_line1!r}\n  Found:    {first_line!r}"