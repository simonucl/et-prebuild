# test_initial_state.py
#
# Pytest suite that validates the expected starting conditions
# before the learner’s solution is executed.

import os
import stat
import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")
SALES_CSV = os.path.join(DATA_DIR, "sales.csv")
OUTPUT_DIR = os.path.join(HOME, "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "total_revenue.txt")

EXPECTED_CSV_CONTENT = (
    "Date,Region,Product,Quantity,Price,Revenue\n"
    "2023-01-01,North,Widget,10,2.50,25.00\n"
    "2023-01-02,South,Gadget,5,5.00,25.00\n"
    "2023-01-03,East,Widget,7,2.50,17.50\n"
    "2023-01-04,West,Doohickey,2,12.00,24.00\n"
    "2023-01-05,North,Gadget,1,5.00,5.00\n"
)

def _mode(path):
    """Return the permission bits (e.g. 0o755, 0o644) of a file/dir."""
    return stat.S_IMODE(os.lstat(path).st_mode)


def test_data_directory_exists():
    assert os.path.isdir(DATA_DIR), f"Required directory {DATA_DIR!r} is missing."
    expected_mode = 0o755
    actual_mode = _mode(DATA_DIR)
    assert actual_mode == expected_mode, (
        f"Directory {DATA_DIR!r} should have permissions {oct(expected_mode)}, "
        f"but has {oct(actual_mode)}."
    )


def test_sales_csv_exists_and_is_regular_file():
    assert os.path.isfile(SALES_CSV), f"Required file {SALES_CSV!r} is missing."
    expected_mode = 0o644
    actual_mode = _mode(SALES_CSV)
    assert actual_mode == expected_mode, (
        f"File {SALES_CSV!r} should have permissions {oct(expected_mode)}, "
        f"but has {oct(actual_mode)}."
    )


def test_sales_csv_content_is_exact():
    with open(SALES_CSV, "r", encoding="utf-8") as fp:
        content = fp.read()
    assert content == EXPECTED_CSV_CONTENT, (
        f"The contents of {SALES_CSV!r} do not match the expected 6-line dataset.\n"
        "If you have modified the file or it was missing lines, restore it to exactly:\n"
        f"{EXPECTED_CSV_CONTENT!r}"
    )


def test_output_directory_does_not_exist_yet():
    assert not os.path.exists(OUTPUT_DIR), (
        f"Output directory {OUTPUT_DIR!r} already exists. "
        "The exercise expects the learner to create it."
    )


def test_output_file_does_not_exist_yet():
    assert not os.path.exists(OUTPUT_FILE), (
        f"Output file {OUTPUT_FILE!r} already exists. "
        "The exercise expects the learner to generate this file."
    )