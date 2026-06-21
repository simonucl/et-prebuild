# test_initial_state.py
#
# This test-suite verifies that the on-disk situation is EXACTLY as described
# in the task **before** the student starts their “disk-usage cleanup & report”
# session.  Any deviation will fail the test with a clear, actionable message.
#
# Allowed imports: only stdlib + pytest (per instructions).

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
WORKSHOP = HOME / "workshop"
DATA_DIR = WORKSHOP / "data"

# --- Expected file layout and exact byte sizes --------------------------------
EXPECTED_FILES = {
    DATA_DIR / "raw" / "big_dataset.csv": 2_097_152,       # 2 MiB
    DATA_DIR / "raw" / "medium_dataset.csv": 524_288,      # 512 KiB
    DATA_DIR / "processed" / "small_clean.csv": 10_240,    # 10 KiB
    DATA_DIR / "extra" / "tiny.txt": 512,                  # 512 B
}

# Paths that MUST NOT exist before the student starts.
MUST_NOT_EXIST = [
    WORKSHOP / "archive",
    WORKSHOP / "archive.tar.gz",
    WORKSHOP / "disk_usage_report.log",
]


def _human(path: Path) -> str:
    """Return a readable path for error messages."""
    return str(path)


@pytest.mark.parametrize("path,expected_size", EXPECTED_FILES.items())
def test_expected_files_exist_with_correct_size(path: Path, expected_size: int):
    # 1. Path must exist.
    assert path.exists(), f"Expected file {_human(path)} is missing."

    # 2. Must be a regular file (not dir, symlink, etc.).
    assert path.is_file(), f"{_human(path)} exists but is not a regular file."

    # 3. Size must match exactly.
    actual_size = path.stat().st_size
    assert (
        actual_size == expected_size
    ), (
        f"{_human(path)} size mismatch: expected {expected_size} bytes, "
        f"found {actual_size} bytes."
    )

    # 4. (Sanity) All files must live under /home/user/workshop/data.
    assert DATA_DIR in path.parents, f"{_human(path)} is outside the data tree."


def test_no_unexpected_entries_in_data_tree():
    """
    Ensure that NOTHING else (no extra files, no stray directories) exists
    under /home/user/workshop/data except the paths we explicitly listed
    and their parent directories.
    """
    allowed_paths = set(EXPECTED_FILES.keys())
    # Also allow the intermediate directories.
    for p in allowed_paths.copy():
        allowed_paths.update(p.parents)

    for found_path in DATA_DIR.rglob("*"):
        assert (
            found_path in allowed_paths
        ), f"Unexpected entry {_human(found_path)} present in data tree before the task begins."


@pytest.mark.parametrize("path", MUST_NOT_EXIST)
def test_artifacts_do_not_exist_yet(path: Path):
    """
    The archive directory, tarball, and report file must NOT exist *before*
    the student carries out the cleanup steps.
    """
    assert (
        not path.exists()
    ), f"Path {_human(path)} should NOT exist before the student starts, but it does."


def test_files_above_1_mib_are_present_as_expected():
    """
    Confirm that exactly one file larger than 1 MiB is present, matching the
    problem statement.
    """
    one_mib = 1_048_576
    large_files = [
        p for p, size in EXPECTED_FILES.items() if size > one_mib
    ]

    # There must be exactly one such file and it must be big_dataset.csv.
    assert len(large_files) == 1, (
        f"Expected exactly one file larger than 1 MiB before the task starts; "
        f"found {len(large_files)}."
    )
    big_file = large_files[0]
    assert (
        big_file.name == "big_dataset.csv"
    ), "The >1 MiB file should be 'big_dataset.csv' according to the spec."
    # Re-check its size relative to the threshold for clarity.
    assert (
        EXPECTED_FILES[big_file] > one_mib
    ), "big_dataset.csv must indeed be larger than 1 MiB."


def test_parent_directories_are_present_and_directories_only():
    """
    Final sanity-check: every parent directory up to /home/user/workshop/data
    must exist and be a directory.
    """
    for file_path in EXPECTED_FILES:
        for parent in file_path.parents:
            if parent == Path("/"):
                break
            assert parent.exists(), f"Expected parent directory {_human(parent)} is missing."
            assert parent.is_dir(), f"{_human(parent)} exists but is not a directory."