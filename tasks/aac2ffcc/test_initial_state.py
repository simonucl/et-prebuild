# test_initial_state.py
#
# Pytest suite that verifies the expected *initial* state of the
# filesystem before the student performs any actions.
#
# The checks focus exclusively on the pre-existing input data under
# /home/user/project_data.  No assertions are made about any of the
# required output paths such as /home/user/backup, in compliance with
# the specification.

import os
import stat
from pathlib import Path

import pytest

PROJECT_DIR = Path("/home/user/project_data")
EXPECTED_FILES = {
    "data1.txt": "The quick brown fox jumps over the lazy dog\n",
    "data2.txt": "Sphinx of black quartz, judge my vow\n",
    "config.cfg": "mode=production\n",
}


def test_project_directory_exists_and_is_dir():
    assert PROJECT_DIR.exists(), (
        f"Expected directory {PROJECT_DIR} to exist, but it does not."
    )
    assert PROJECT_DIR.is_dir(), (
        f"Expected {PROJECT_DIR} to be a directory, but it is not."
    )


def test_project_directory_contains_only_expected_files():
    present_files = sorted(
        p.name for p in PROJECT_DIR.iterdir() if p.is_file()
    )
    expected_files_sorted = sorted(EXPECTED_FILES.keys())
    assert present_files == expected_files_sorted, (
        "The directory /home/user/project_data should contain exactly "
        f"the files {expected_files_sorted}, but it currently contains "
        f"{present_files}."
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_each_file_exists_is_regular_and_has_expected_content(filename, expected_content):
    file_path = PROJECT_DIR / filename

    # 1. Path exists and is a regular file
    assert file_path.exists(), f"Expected file {file_path} to exist, but it does not."
    assert file_path.is_file(), f"Expected {file_path} to be a regular file."
    mode = file_path.stat().st_mode
    assert stat.S_IMODE(mode) & 0o444, (
        f"{file_path} is not world-readable (expected permission bits to include r--r--r--)."
    )

    # 2. Contents match exactly (including trailing newline)
    with file_path.open("r", encoding="utf-8") as fh:
        content = fh.read()
    assert content == expected_content, (
        f"Contents of {file_path} do not match the expected value.\n"
        "Expected:\n"
        f"{expected_content!r}\n"
        "Found:\n"
        f"{content!r}"
    )