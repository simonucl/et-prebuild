# test_initial_state.py
# Pytest suite to verify the initial filesystem state
# before the student runs any commands.

import os
import stat
from pathlib import Path

RAW_DIR = Path("/home/user/data/raw")
EXPECTED_CSV_FILES = {
    "sales_north.csv",
    "sales_south.csv",
    "sales_west.csv",
}


def _is_regular_file(path: Path) -> bool:
    """
    Return True if `path` exists and is a regular file (not a symlink, fifo, etc.).
    """
    try:
        st = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISREG(st.st_mode)


def test_raw_directory_exists_and_is_directory():
    """
    /home/user/data/raw must exist and be a directory.
    """
    assert RAW_DIR.exists(), f"Directory {RAW_DIR} is missing."
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."


def test_expected_csv_files_exist_and_are_regular():
    """
    Each expected CSV must exist and be a regular file.
    """
    for fname in EXPECTED_CSV_FILES:
        fpath = RAW_DIR / fname
        assert _is_regular_file(
            fpath
        ), f"Expected regular file {fpath} is missing or not a regular file."


def test_no_extra_csv_files_present():
    """
    There must be exactly the expected CSV files—no more, no fewer—
    in the raw directory (non-CSV files are ignored).
    """
    actual_csvs = {
        entry.name
        for entry in RAW_DIR.iterdir()
        if entry.is_file() and entry.name.lower().endswith(".csv")
    }

    missing = EXPECTED_CSV_FILES - actual_csvs
    extras = actual_csvs - EXPECTED_CSV_FILES

    msg_parts = []
    if missing:
        msg_parts.append(f"missing CSV files: {sorted(missing)}")
    if extras:
        msg_parts.append(f"unexpected CSV files present: {sorted(extras)}")

    assert not (missing or extras), (
        "CSV file set mismatch in /home/user/data/raw. " + "; ".join(msg_parts)
    )