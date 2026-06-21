# test_initial_state.py
#
# Pytest suite that validates the **initial** OS / filesystem state
# before the student starts working on the deployment task.
#
# Rules enforced:
#   • Exactly two input CSV files must be present in /home/user/release.
#   • Their contents must match the specification byte-for-byte
#     (ignoring the final newline that all POSIX text files may have).
#   • They must use UNIX line endings (LF, no CR).
#   • No checks are made for the output artefacts that the student will
#     create later (production_summary.csv, production_summary.json,
#     deployment.log), per the instructions.

import os
from pathlib import Path
import pytest

BASE_DIR = Path("/home/user/release")
INV_PATH = BASE_DIR / "inventory.csv"
UPD_PATH = BASE_DIR / "updates.csv"

EXPECTED_INVENTORY_LINES = [
    "server_id,hostname,env,current_version",
    "1,web-1,production,2.4.10",
    "2,web-2,production,2.4.10",
    "3,db-1,staging,12.1.0",
    "4,cache-1,production,1.9.3",
    "5,api-1,staging,3.2.1",
]

EXPECTED_UPDATES_LINES = [
    "server_id,target_version,window",
    "1,2.4.11,2024-06-20",
    "2,2.4.11,2024-06-20",
    "3,12.1.1,2024-06-21",
    "4,1.9.4,2024-06-20",
    "5,3.2.2,2024-06-21",
]


def _read_file_lines(path: Path):
    """
    Helper that reads *all* bytes from the file, asserts it contains only LF
    line breaks (no CR), and returns a list produced by str.splitlines().
    """
    assert path.exists(), f"Expected file {path} is missing."
    assert path.is_file(), f"Expected {path} to be a regular file."
    raw = path.read_bytes()
    assert b"\r" not in raw, (
        f"{path} must use UNIX LF line endings only (found CR characters)."
    )
    text = raw.decode("utf-8")
    # Accept an optional final newline (common on UNIX systems),
    # but no *extra* blank line afterwards.
    if text.endswith("\n"):
        text = text[:-1]  # strip the single trailing LF
    return text.split("\n")


@pytest.mark.parametrize(
    "path,expected_lines",
    [
        (INV_PATH, EXPECTED_INVENTORY_LINES),
        (UPD_PATH, EXPECTED_UPDATES_LINES),
    ],
)
def test_input_files_exist_and_are_correct(path: Path, expected_lines):
    """
    Assert that the required CSV files exist with exactly the expected content.
    """
    actual_lines = _read_file_lines(path)
    assert (
        actual_lines == expected_lines
    ), f"File {path} does not match the expected contents.\n" \
       f"Expected:\n{expected_lines}\n\nGot:\n{actual_lines}"


def test_release_directory_structure():
    """
    Sanity-check that /home/user/release exists and is a directory.
    """
    assert BASE_DIR.exists(), f"Directory {BASE_DIR} is missing."
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


def test_no_unexpected_output_files_yet():
    """
    The student has not run their solution yet, so the output artefacts
    must NOT be present at this point.
    """
    for name in (
        "production_summary.csv",
        "production_summary.json",
        "deployment.log",
    ):
        path = BASE_DIR / name
        assert not path.exists(), (
            f"Output file {path} should not exist before the task is run."
        )