# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the student performs any action for the “quarterly CSV
# staging-area” task.
#
# IMPORTANT:  These tests purposefully DO NOT look for any of the
#             “expected end-state” files (2023_Q1 links or manifest).
#             They only assert the *starting* conditions that the
#             student must clean up.

import os
from pathlib import Path

DATA_DIR = Path("/home/user/data")
ORIGINAL_DIR = DATA_DIR / "original"
CURRENT_DIR = DATA_DIR / "current"

# CSV files that must exist in ORIGINAL_DIR (regular files)
CSV_2023_Q1 = {
    "sales_2023_Q1.csv": [
        "month,units,revenue\n",
        "Jan,100,1200\n",
        "Feb,130,1500\n",
    ],
    "inventory_2023_Q1.csv": [
        "month,units,value\n",
        "Jan,45,720\n",
    ],
    "marketing_2023_Q1.csv": [
        "channel,impressions,spend\n",
        "Social,12000,350\n",
    ],
}
CSV_2022_Q4 = {
    "sales_2022_Q4.csv": [
        "month,units,revenue\n",
        "Dec,90,1100\n",
    ]
}

ALL_ORIGINAL_FILES = {**CSV_2023_Q1, **CSV_2022_Q4}


def _read_lines(path: Path):
    """Read a file and return its list of lines."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


def test_data_directory_structure():
    """/home/user/data must contain ONLY 'original' and 'current'."""
    assert DATA_DIR.is_dir(), f"Expected directory {DATA_DIR} is missing."

    children = {p.name for p in DATA_DIR.iterdir()}
    expected = {"original", "current"}
    extra = children - expected
    missing = expected - children

    if missing:
        raise AssertionError(
            f"Missing expected directory/directories under {DATA_DIR}: {', '.join(sorted(missing))}"
        )
    if extra:
        # Any extra (non-hidden) items are disallowed
        raise AssertionError(
            f"Found unexpected item(s) under {DATA_DIR}: {', '.join(sorted(extra))}"
        )


def test_original_directory_files_and_contents():
    """Verify the CSV files inside /home/user/data/original."""
    assert ORIGINAL_DIR.is_dir(), f"Directory {ORIGINAL_DIR} is missing."

    # 1. Check that ONLY the expected CSVs exist.
    present_files = {p.name for p in ORIGINAL_DIR.iterdir()}
    expected_files = set(ALL_ORIGINAL_FILES.keys())
    extra = present_files - expected_files
    missing = expected_files - present_files

    if missing:
        raise AssertionError(
            f"Missing CSV file(s) in {ORIGINAL_DIR}: {', '.join(sorted(missing))}"
        )
    if extra:
        raise AssertionError(
            f"Unexpected file(s) present in {ORIGINAL_DIR}: {', '.join(sorted(extra))}"
        )

    # 2. Validate file types and minimal content lines.
    for fname, expected_lines in ALL_ORIGINAL_FILES.items():
        path = ORIGINAL_DIR / fname
        assert path.is_file(), f"Expected regular file {path} is missing or not a regular file."
        lines = _read_lines(path)
        assert lines[: len(expected_lines)] == expected_lines, (
            f"File {path} does not contain the expected first {len(expected_lines)} line(s)."
        )


def test_current_directory_contains_only_outdated_symlink():
    """
    /home/user/data/current must contain exactly one symlink:
    sales_latest.csv -> ../original/sales_2022_Q4.csv
    """
    assert CURRENT_DIR.is_dir(), f"Directory {CURRENT_DIR} is missing."

    entries = list(CURRENT_DIR.iterdir())
    assert len(entries) == 1, (
        f"{CURRENT_DIR} should contain exactly 1 entry (the outdated symlink) "
        f"but contains {len(entries)}: {[p.name for p in entries]}"
    )

    link_path = CURRENT_DIR / "sales_latest.csv"
    assert link_path.exists(), (
        f"Expected symlink {link_path} is missing."
    )
    assert link_path.is_symlink(), (
        f"{link_path} exists but is not a symbolic link."
    )

    # The symlink target must be the relative path '../original/sales_2022_Q4.csv'
    target = os.readlink(link_path)
    expected_target = "../original/sales_2022_Q4.csv"
    assert target == expected_target, (
        f"Symlink {link_path} should point to '{expected_target}' "
        f"but points to '{target}'."
    )

    # The resolved absolute path must exist and be the correct file
    resolved_path = (link_path.parent / target).resolve()
    assert resolved_path == ORIGINAL_DIR / "sales_2022_Q4.csv", (
        f"Symlink {link_path} resolves to {resolved_path}, "
        f"expected {(ORIGINAL_DIR / 'sales_2022_Q4.csv')}"
    )
    assert resolved_path.is_file(), (
        f"Resolved path {resolved_path} does not point to a regular file."
    )