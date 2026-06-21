# test_initial_state.py
#
# This test-suite verifies the filesystem *before* the student runs any
# commands.  It confirms that the raw data file is present and correct, and
# that the output directory / file the student is expected to create does
# NOT yet exist.
#
# Any failure message should make it immediately obvious what is wrong.

import os
import stat
import pytest

RAW_PATH = "/home/user/data/server_capacity.raw"
OUTPUT_DIR = "/home/user/capacity"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "current_capacity.csv")

EXPECTED_RAW_LINES = [
    "MemTotal: 16384\n",
    "MemFree: 8192\n",
    "DiskTotal: 200G\n",
    "DiskUsed: 120G\n",
]


def test_raw_file_exists_with_correct_permissions():
    """Ensure the metrics file is present, readable, and has mode 0644."""
    assert os.path.isfile(RAW_PATH), (
        f"Required file '{RAW_PATH}' is missing."
    )

    st = os.stat(RAW_PATH)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o644, (
        f"File '{RAW_PATH}' must have permissions 0644, found {oct(mode)}."
    )


def test_raw_file_contents_are_exact():
    """Validate that the raw file contains exactly the four expected lines."""
    with open(RAW_PATH, "r", encoding="utf-8") as fp:
        lines = fp.readlines()

    assert lines == EXPECTED_RAW_LINES, (
        f"Contents of '{RAW_PATH}' do not match the expected template.\n"
        f"Expected:\n{''.join(EXPECTED_RAW_LINES)!r}\n"
        f"Got:\n{''.join(lines)!r}"
    )


def test_output_file_and_directory_do_not_yet_exist():
    """
    The student must create /home/user/capacity/current_capacity.csv.
    Confirm that neither the directory nor the file pre-exist.
    """
    assert not os.path.exists(OUTPUT_FILE), (
        f"Output file '{OUTPUT_FILE}' already exists — it should be created "
        "by the student’s solution, not provided beforehand."
    )

    # Having the directory absent is ideal; if it exists, ensure it's empty.
    if os.path.exists(OUTPUT_DIR):
        assert os.path.isdir(OUTPUT_DIR), (
            f"'{OUTPUT_DIR}' exists but is not a directory."
        )
        existing = os.listdir(OUTPUT_DIR)
        assert OUTPUT_FILE.split("/")[-1] not in existing, (
            f"Directory '{OUTPUT_DIR}' already contains '{existing}', "
            "but it should be empty at this stage."
        )