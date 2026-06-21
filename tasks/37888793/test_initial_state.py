# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem
state for the “disk-usage audit” task.

It asserts that ONLY the expected data files are present under
/home/user/data and that their byte-sizes sum to the documented ground-
truth values.  It intentionally ignores (does not look for) any paths
under /home/user/audit because those are output artefacts that must
be created by the student’s solution.

All checks use absolute paths and rely solely on stdlib + pytest.
"""

import os
from pathlib import Path

import pytest

# ---------- CONSTANTS ---------------------------------------------------------

DATA_DIR = Path("/home/user/data")

EXPECTED_FILES = {
    DATA_DIR / "fileA.txt": 17,
    DATA_DIR / "fileB.log": 24,
    DATA_DIR / "subdir1" / "fileC.bin": 1024,
    DATA_DIR / "subdir2" / "nested.txt": 23,
}

TOTAL_SIZE_BYTES = 1088
FILE_COUNT = 4


# ---------- TESTS -------------------------------------------------------------


def test_data_directory_exists():
    assert DATA_DIR.exists(), (
        f"Required data directory {DATA_DIR} is missing. "
        "It must exist before the audit script runs."
    )
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."


@pytest.mark.parametrize("file_path,expected_size", EXPECTED_FILES.items())
def test_expected_file_present_with_correct_size(file_path: Path, expected_size: int):
    assert file_path.exists(), f"Expected file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."
    actual_size = file_path.stat().st_size
    assert (
        actual_size == expected_size
    ), f"{file_path} size mismatch: expected {expected_size} B, found {actual_size} B."


def test_no_extra_regular_files_and_totals_match():
    """
    Walk the entire /home/user/data tree and ensure:
    1. Exactly the EXPECTED_FILES are present (no more, no less).
    2. Aggregate byte size and count match ground truth.
    """
    discovered_files = {}
    for root, _, files in os.walk(DATA_DIR):
        for f in files:
            abs_path = Path(root) / f
            # Follow the assignment rule: count only *regular* files.
            if abs_path.is_file():
                discovered_files[abs_path] = abs_path.stat().st_size

    # ---- Check for unexpected or missing files --------------------------------
    missing = set(EXPECTED_FILES) - set(discovered_files)
    extra = set(discovered_files) - set(EXPECTED_FILES)
    assert not missing, (
        "The following expected files are missing from the data directory:\n"
        + "\n".join(str(p) for p in sorted(missing))
    )
    assert not extra, (
        "Unexpected extra regular files found under /home/user/data. "
        "The audit must only include the documented files.\n"
        + "\n".join(str(p) for p in sorted(extra))
    )

    # ---- Check aggregate size and count ---------------------------------------
    total_size = sum(discovered_files.values())
    file_count = len(discovered_files)

    assert (
        file_count == FILE_COUNT
    ), f"FILE_COUNT mismatch: expected {FILE_COUNT}, found {file_count}."
    assert (
        total_size == TOTAL_SIZE_BYTES
    ), f"TOTAL_SIZE_BYTES mismatch: expected {TOTAL_SIZE_BYTES}, found {total_size}."