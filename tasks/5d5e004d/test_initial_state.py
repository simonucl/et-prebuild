# test_initial_state.py
#
# This pytest suite verifies that the filesystem is in the **initial**
# state expected by the assignment *before* the student runs any commands.
#
# What is checked:
#   • Presence and type of the /home/user/datasets directory
#   • That /home/user/dataset_summary.log does NOT yet exist
#   • Exactly three experiment sub-directories: expA, expB, expC
#   • Each experiment directory contains only the expected regular files
#     with the exact byte sizes stated in the task description
#   • No extra files, sub-directories, or symlinks are present
#   • Permissions: 0755 for directories, 0644 for files
#
# If any assertion fails, the corresponding error message pinpoints
# precisely what is missing or incorrect.
#
# NOTE: Uses only Python stdlib + pytest.


import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
DATASETS_DIR = HOME / "datasets"
SUMMARY_LOG = HOME / "dataset_summary.log"

# Expected file structure and byte sizes
EXPECTED_DATA = {
    "expA": {"data1.txt": 1024, "data2.txt": 512, "notes.log": 1536},
    "expB": {"image1.jpg": 2048, "image2.jpg": 4096, "readme.md": 512},
    "expC": {"sample.dat": 1234, "more.dat": 321},
}

DIR_PERMS = 0o755
FILE_PERMS = 0o644


def _mode_bits(p: Path) -> int:
    """Return the permission bits of the file (e.g. 0o755)."""
    return stat.S_IMODE(p.stat().st_mode)


def test_datasets_directory_exists_and_is_dir():
    assert DATASETS_DIR.exists(), f"Required directory {DATASETS_DIR} is missing."
    assert DATASETS_DIR.is_dir(), f"{DATASETS_DIR} exists but is not a directory."
    assert (
        _mode_bits(DATASETS_DIR) == DIR_PERMS
    ), f"{DATASETS_DIR} should have permissions {oct(DIR_PERMS)}, " \
       f"found {oct(_mode_bits(DATASETS_DIR))}."


def test_summary_log_does_not_exist_yet():
    assert not SUMMARY_LOG.exists(), (
        f"{SUMMARY_LOG} should NOT exist yet; it will be created by the student's solution."
    )


def test_exact_experiment_subdirectories_present():
    expected_dirs = set(EXPECTED_DATA.keys())
    found_dirs = {p.name for p in DATASETS_DIR.iterdir() if p.is_dir()}
    extra = found_dirs - expected_dirs
    missing = expected_dirs - found_dirs

    assert not extra, (
        f"Unexpected extra directories inside {DATASETS_DIR}: {sorted(extra)}"
    )
    assert not missing, (
        f"Missing expected directories inside {DATASETS_DIR}: {sorted(missing)}"
    )

    # Ensure there are no non-directory entries in /home/user/datasets
    non_dirs = [p.name for p in DATASETS_DIR.iterdir() if not p.is_dir()]
    assert not non_dirs, (
        f"Only directories are expected inside {DATASETS_DIR}, "
        f"but found non-directory entries: {sorted(non_dirs)}"
    )


@pytest.mark.parametrize("exp_name,files", EXPECTED_DATA.items())
def test_files_and_sizes(exp_name, files):
    exp_path = DATASETS_DIR / exp_name
    # Directory sanity checks
    assert exp_path.is_dir(), f"Missing experiment directory: {exp_path}"
    assert (
        _mode_bits(exp_path) == DIR_PERMS
    ), f"{exp_path} should have permissions {oct(DIR_PERMS)}, " \
       f"found {oct(_mode_bits(exp_path))}."

    # Collect actual regular files (ignore anything else but fail if other types exist)
    actual_files = {p.name: p for p in exp_path.iterdir() if p.is_file()}
    actual_non_regular = [p.name for p in exp_path.iterdir() if not p.is_file()]
    assert (
        not actual_non_regular
    ), f"{exp_path} must contain only regular files; unexpected entries: {sorted(actual_non_regular)}"

    expected_names = set(files.keys())
    found_names = set(actual_files.keys())

    extra = found_names - expected_names
    missing = expected_names - found_names

    assert not extra, f"{exp_path} contains unexpected files: {sorted(extra)}"
    assert not missing, f"{exp_path} is missing files: {sorted(missing)}"

    # Verify each file's size and permissions
    for fname, expected_size in files.items():
        fpath = actual_files[fname]
        actual_size = fpath.stat().st_size
        assert (
            actual_size == expected_size
        ), f"Size mismatch for {fpath}: expected {expected_size} bytes, found {actual_size} bytes."
        assert (
            _mode_bits(fpath) == FILE_PERMS
        ), f"{fpath} should have permissions {oct(FILE_PERMS)}, " \
           f"found {oct(_mode_bits(fpath))}."


def test_global_totals():
    """Sanity-check the aggregate counts and sizes for all datasets."""
    total_bytes = 0
    total_files = 0
    for exp, files in EXPECTED_DATA.items():
        total_bytes += sum(files.values())
        total_files += len(files)

    assert total_bytes == 11283, (
        f"Aggregate byte total should be 11283, got {total_bytes}"
    )
    assert total_files == 8, (
        f"Aggregate file count should be 8, got {total_files}"
    )