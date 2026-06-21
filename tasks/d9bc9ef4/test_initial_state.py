# test_initial_state.py
#
# This pytest suite validates the initial, on-disk state **before**
# the learner performs any actions for the “FinOps backup” exercise.
#
# It checks that:
#   • /home/user/finops/raw_cost_data/ exists.
#   • The files january.csv and february.csv are present in that directory.
#   • Each file is exactly 38 bytes.
#   • The file contents are an exact, byte-for-byte match to the truth data.
#   • The cumulative size of the two CSVs is 76 bytes.
#
# NOTE:  Per requirements, the tests intentionally do *not* reference or
#        assert anything about the eventual output paths under
#        /home/user/finops/backups/.

import os
import pytest

RAW_DIR = "/home/user/finops/raw_cost_data"
JAN_CSV = os.path.join(RAW_DIR, "january.csv")
FEB_CSV = os.path.join(RAW_DIR, "february.csv")

JAN_CONTENT = (
    "Date,Cost\n"
    "Compute,23.45\n"
    "Storage,12.00\n"
)
FEB_CONTENT = (
    "Date,Cost\n"
    "Compute,25.10\n"
    "Storage,11.50\n"
)

@pytest.fixture(scope="module")
def raw_files():
    """Return a dict mapping filename to its expected content."""
    return {
        JAN_CSV: JAN_CONTENT,
        FEB_CSV: FEB_CONTENT,
    }

def test_raw_cost_data_dir_exists():
    assert os.path.isdir(RAW_DIR), (
        f"Expected directory {RAW_DIR!r} to exist, but it is missing "
        "or is not a directory."
    )

def test_required_csv_files_exist(raw_files):
    missing = [path for path in raw_files if not os.path.isfile(path)]
    assert not missing, (
        "The following required CSV file(s) are missing under "
        f"{RAW_DIR!r}: {', '.join(missing)}"
    )

def test_csv_file_sizes_are_exact(raw_files):
    for path, expected_content in raw_files.items():
        size_on_disk = os.path.getsize(path)
        expected_size = len(expected_content.encode("utf-8"))
        assert size_on_disk == expected_size, (
            f"{os.path.basename(path)!r} size mismatch: expected "
            f"{expected_size} bytes, found {size_on_disk} bytes."
        )

def test_csv_file_contents_are_exact(raw_files):
    for path, expected_content in raw_files.items():
        with open(path, "r", encoding="utf-8") as fh:
            actual = fh.read()
        assert actual == expected_content, (
            f"Contents of {os.path.basename(path)!r} do not match the "
            "expected truth data."
        )

def test_total_bytes_is_76(raw_files):
    total_bytes = sum(os.path.getsize(p) for p in raw_files)
    assert total_bytes == 76, (
        f"Total byte count of CSV files should be 76, but is {total_bytes}."
    )