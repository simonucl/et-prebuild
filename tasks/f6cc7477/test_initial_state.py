# test_initial_state.py
#
# This pytest suite validates the INITIAL filesystem state
# before the student executes any commands.  It intentionally
# fails fast and with clear error messages if anything in the
# starting environment is not exactly as described in the task.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
RAW_DIR = HOME / "raw_data"
PROC_DIR = HOME / "processed_data"

Q1 = RAW_DIR / "inventory_q1.csv"
Q2 = RAW_DIR / "inventory_q2.csv"

EXPECTED_Q1_LINES = [
    "id,product,quantity",
    "1,Apples,50",
    "2,Bananas,75",
    "3,Carrots,40",
]

EXPECTED_Q2_LINES = [
    "id,product,quantity",
    "4,Dates,60",
    "5,Eggplants,30",
    "6,Flour,90",
]


def read_lines(path: Path):
    """
    Return the file content split on '\n' **without** preserving the newline
    characters. A terminal newline (common on Unix) produces an empty final
    element, which we strip to ensure exact line count.
    """
    text = path.read_text(encoding="utf-8")
    # Assert Unix line-endings only
    assert "\r" not in text, f"File {path} must use UNIX (LF) line endings only."
    lines = text.split("\n")
    # Remove the empty element caused by a trailing LF (if present)
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def assert_exact_file_content(path: Path, expected_lines: list[str]):
    """Helper: verify byte-for-byte textual content except for the final LF."""
    lines = read_lines(path)
    assert lines == expected_lines, (
        f"Content mismatch in {path}.\n"
        f"Expected:\n{expected_lines!r}\n\nActual:\n{lines!r}"
    )


def test_raw_data_directory_exists():
    assert RAW_DIR.is_dir(), (
        f"Required directory {RAW_DIR} is missing. "
        "The starting VM must contain /home/user/raw_data/."
    )


def test_processed_data_directory_absent_initially():
    assert not PROC_DIR.exists(), (
        f"Directory {PROC_DIR} should NOT exist before the student runs the task."
    )


def test_raw_data_contains_exactly_two_csv_files():
    entries = sorted(p.name for p in RAW_DIR.iterdir() if p.is_file())
    expected = sorted([Q1.name, Q2.name])
    assert entries == expected, (
        f"{RAW_DIR} should contain ONLY {expected} (found: {entries})."
    )


@pytest.mark.parametrize(
    "csv_path,expected_lines",
    [(Q1, EXPECTED_Q1_LINES), (Q2, EXPECTED_Q2_LINES)],
)
def test_csv_files_have_correct_content(csv_path: Path, expected_lines: list[str]):
    assert csv_path.is_file(), f"Expected file {csv_path} is missing."
    assert_exact_file_content(csv_path, expected_lines)


def test_no_extra_items_in_raw_data_directory():
    # Ensure no subdirectories or unexpected items are present.
    extra = [p for p in RAW_DIR.iterdir() if p.name not in {Q1.name, Q2.name}]
    assert not extra, f"Unexpected items in {RAW_DIR}: {[p.name for p in extra]}"