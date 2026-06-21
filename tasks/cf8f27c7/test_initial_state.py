# test_initial_state.py
#
# Pytest suite that verifies the **initial** filesystem state _before_ the
# student begins any work.  It checks only the pre-existing raw data area and
# makes **no** assertions about any of the output paths requested in the task
# description (per grading rules).

import os
from pathlib import Path

import pytest

RAW_DATA_DIR = Path("/home/user/raw_data")

# Mapping of expected raw files to their exact byte content (including the
# trailing newline that is present on disk).
EXPECTED_RAW_FILES = {
    RAW_DATA_DIR / "raw1.json": (
        '{"id": "sensor-A", "timestamp": "2023-09-01T12:00:00Z", '
        '"value": 42.7, "tags": ["lab","temperature"]}\n'
    ),
    RAW_DATA_DIR / "raw2.json": (
        '{"id": 123, "timestamp": "2023-09-01T12:05:00Z", '
        '"value": "40.1", "tags": ["lab","temperature"]}\n'
    ),
    RAW_DATA_DIR / "raw3.json": (
        '{"id": "sensor-B", "timestamp": "BADDATE", '
        '"value": 37.2, "tags": "humidity"}\n'
    ),
}


def test_raw_data_directory_exists_and_is_dir():
    assert RAW_DATA_DIR.exists(), f"Expected directory '{RAW_DATA_DIR}' is missing."
    assert RAW_DATA_DIR.is_dir(), f"'{RAW_DATA_DIR}' exists but is not a directory."


@pytest.mark.parametrize("file_path,expected_content", list(EXPECTED_RAW_FILES.items()))
def test_each_expected_raw_file_exists_with_correct_content(file_path: Path, expected_content: str):
    assert file_path.exists(), f"Expected raw data file '{file_path}' is missing."
    assert file_path.is_file(), f"Path '{file_path}' exists but is not a regular file."

    # Read file as text with universal newlines disabled to preserve exact bytes.
    actual_content = file_path.read_text(encoding="utf-8")
    assert (
        actual_content == expected_content
    ), (
        f"Content mismatch in '{file_path}'.\n"
        "---- Expected ----\n"
        f"{expected_content!r}\n"
        "---- Actual ----\n"
        f"{actual_content!r}"
    )


def test_no_extra_files_in_raw_data_directory():
    """
    Ensure the raw_data directory contains **only** the three expected JSON files
    and nothing else (no extraneous files or sub-directories).
    """
    found_items = sorted(RAW_DATA_DIR.iterdir())
    expected_items = sorted(EXPECTED_RAW_FILES.keys())

    assert (
        found_items == expected_items
    ), (
        "The contents of /home/user/raw_data do not exactly match the expected "
        "set of files.\n\n"
        f"Expected ({len(expected_items)}):\n  " + "\n  ".join(map(str, expected_items)) +
        "\n\nFound ({len(found_items)}):\n  " + "\n  ".join(map(str, found_items))
    )