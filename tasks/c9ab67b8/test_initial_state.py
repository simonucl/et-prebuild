# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state for the
“checksum-frequency” task *before* the student performs any action.

It confirms:
1. The data directory exists and is writeable.
2. The raw checksum list is present and contains the exact expected 12 lines.
3. The target output file does **not** yet exist.

Any deviation will cause a clear, explanatory test failure.
"""

import os
from pathlib import Path

DATA_DIR = Path("/home/user/data")
RAW_FILE = DATA_DIR / "daily_checksums.txt"
OUTPUT_FILE = DATA_DIR / "checksum_frequency.log"

EXPECTED_LINES = [
    "a1b2c3d4e5f6g7h8i9j0\n",
    "11111111111111111111\n",
    "a1b2c3d4e5f6g7h8i9j0\n",
    "22222222222222222222\n",
    "33333333333333333333\n",
    "11111111111111111111\n",
    "22222222222222222222\n",
    "22222222222222222222\n",
    "44444444444444444444\n",
    "a1b2c3d4e5f6g7h8i9j0\n",
    "55555555555555555555\n",
    "11111111111111111111\n",
]


def test_data_directory_exists_and_is_writeable():
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."
    assert os.access(DATA_DIR, os.W_OK), f"Directory {DATA_DIR} is not writeable by the current user."


def test_raw_checksum_file_exact_contents():
    assert RAW_FILE.exists(), f"Required file {RAW_FILE} is missing."
    assert RAW_FILE.is_file(), f"{RAW_FILE} exists but is not a regular file."

    # Read in binary mode to ensure we do not accidentally translate newlines.
    raw_bytes = RAW_FILE.read_bytes()
    assert raw_bytes.endswith(b"\n"), (
        f"{RAW_FILE} must end with a single UNIX newline (\\n) after the last line."
    )

    # Decode using UTF-8 (ASCII subset) and split into lines including the newline chars.
    raw_text = raw_bytes.decode("utf-8")
    lines = [ln + "\n" for ln in raw_text.rstrip("\n").split("\n")]

    assert (
        lines == EXPECTED_LINES
    ), (
        f"{RAW_FILE} does not contain the expected lines.\n"
        f"Expected ({len(EXPECTED_LINES)} lines):\n{EXPECTED_LINES}\n\n"
        f"Found ({len(lines)} lines):\n{lines}"
    )


def test_output_file_not_present_yet():
    assert not OUTPUT_FILE.exists(), (
        f"Output file {OUTPUT_FILE} already exists. "
        "The student code should create it during execution, "
        "so it must NOT be present beforehand."
    )