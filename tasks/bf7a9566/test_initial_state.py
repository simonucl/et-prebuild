# test_initial_state.py
#
# This pytest suite validates that the *initial* filesystem state
# (before the student’s solution runs) matches the specification
# for the “tiny text-corpus preparation” task.
#
# It intentionally does NOT test for the presence of any output
# files or directories that the student is expected to create.
#
# Expected initial layout:
#
# /home/user/data/
# └── raw/
#     ├── sample1.txt
#     └── sample2.txt
#
# The raw files must contain the exact lines (each terminated by a
# single “\n”) as described in the task description.

import os
from pathlib import Path
import pytest


DATA_DIR = Path("/home/user/data")
RAW_DIR = DATA_DIR / "raw"

SAMPLE1_PATH = RAW_DIR / "sample1.txt"
SAMPLE2_PATH = RAW_DIR / "sample2.txt"

# Ground-truth contents.
EXPECTED_SAMPLE1_LINES = [
    "Hello world\n",
    "Machine learning is fun\n",
    "AI\n",
]

EXPECTED_SAMPLE2_LINES = [
    "AI\n",
    "Hello world\n",
    "Deep learning\n",
]


def read_file_lines(path: Path):
    """
    Read a file and return its list of lines, preserving newline
    characters so that we can assert exact matches and ensure the
    file terminates with a newline.
    """
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


def _format_missing(path: Path) -> str:
    return f"Expected to find {path} but it does not exist."


def _format_unexpected_lines(path: Path, expected, actual) -> str:
    return (
        f"Contents of {path} do not match the expected lines.\n"
        f"Expected ({len(expected)} lines):\n{''.join(expected)}\n"
        f"Actual   ({len(actual)} lines):\n{''.join(actual)}"
    )


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), _format_missing(DATA_DIR)


def test_raw_directory_exists():
    assert RAW_DIR.is_dir(), _format_missing(RAW_DIR)


@pytest.mark.parametrize(
    "file_path",
    [SAMPLE1_PATH, SAMPLE2_PATH],
)
def test_raw_files_exist(file_path: Path):
    assert file_path.is_file(), _format_missing(file_path)


@pytest.mark.parametrize(
    ("file_path", "expected_lines"),
    [
        (SAMPLE1_PATH, EXPECTED_SAMPLE1_LINES),
        (SAMPLE2_PATH, EXPECTED_SAMPLE2_LINES),
    ],
)
def test_raw_files_content(file_path: Path, expected_lines):
    assert file_path.is_file(), _format_missing(file_path)

    actual_lines = read_file_lines(file_path)

    # Check the entire list for exact match (content + order + newlines)
    assert (
        actual_lines == expected_lines
    ), _format_unexpected_lines(file_path, expected_lines, actual_lines)