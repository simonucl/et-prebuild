# test_initial_state.py
#
# Pytest suite that validates the filesystem **before** the student
# performs any action.  It checks only the items that are supposed to
# exist in the initial state; it intentionally avoids asserting anything
# about the yet-to-be-created output directories or files.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")

DOWNLOADS_DIR = HOME / "downloads"
RESEARCH_DIR = HOME / "research"

# ----------------------------------------------------------------------
# Helper data for the three climate data files and the one README file.
# ----------------------------------------------------------------------
EXPECTED_TEXT_FILES = {
    DOWNLOADS_DIR / "climate_temp_v1.txt": [
        "date,temp",
        "2024-01-01,23",
        "2024-01-02,22",
    ],
    DOWNLOADS_DIR / "climate_temp_v2.txt": [
        "date,temp",
        "2024-01-01,24",
        "2024-01-02,23",
        "2024-01-03,25",
    ],
    DOWNLOADS_DIR / "climate_precip_v1.txt": [
        "date,precip_mm",
        "2024-01-01,5",
        "2024-01-02,0",
    ],
}

README_FILE = DOWNLOADS_DIR / "readme.txt"
README_CONTENT = "Placeholder README – do not move."


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
def test_initial_directories_exist():
    """
    The two top-level directories that must already be present:
    /home/user/downloads/ and /home/user/research/
    """
    assert DOWNLOADS_DIR.is_dir(), (
        f"Expected directory {DOWNLOADS_DIR} to exist, "
        "but it was not found."
    )
    assert RESEARCH_DIR.is_dir(), (
        f"Expected directory {RESEARCH_DIR} to exist, "
        "but it was not found."
    )


@pytest.mark.parametrize("file_path,expected_lines", EXPECTED_TEXT_FILES.items())
def test_raw_climate_txt_files_exist_with_exact_content(file_path, expected_lines):
    """
    Each raw climate *.txt file must be present in /home/user/downloads/
    and its contents must match exactly (line-for-line, no extra spaces).
    """
    assert file_path.is_file(), f"Missing required file: {file_path}"
    with file_path.open("r", encoding="utf-8") as fh:
        actual_lines = [line.rstrip("\n") for line in fh.readlines()]

    assert actual_lines == expected_lines, (
        f"Content mismatch in {file_path}.\n"
        f"Expected:\n{expected_lines}\n\nActual:\n{actual_lines}"
    )


def test_readme_file_untouched():
    """
    The unrelated readme.txt must remain in /home/user/downloads/ with its
    original single-line content.
    """
    assert README_FILE.is_file(), f"Missing required file: {README_FILE}"
    with README_FILE.open("r", encoding="utf-8") as fh:
        content = fh.read().rstrip("\n")

    assert content == README_CONTENT, (
        f"Content in {README_FILE} has changed.\n"
        f"Expected: {README_CONTENT!r}\nActual:   {content!r}"
    )