# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state for the
# “storage audit” exercise.  It checks only the data that should be
# present **before** the learner writes any solution code.  Nothing
# related to the expected *output* (/home/user/storage_audit/…)
# is tested here.

import os
from pathlib import Path

import pytest

ROOT = Path("/home/user/storage_samples").resolve()

# ----------------------------------------------------------------------
# Helper data derived from the exercise description
# ----------------------------------------------------------------------

EXPECTED_FILES = {
    ROOT / "large_video.bin":        5 * 1024 * 1024,      # 5 242 880
    ROOT / "archive.tar.gz":         3 * 1024 * 1024,      # 3 145 728
    ROOT / "docs" / "report.txt":    10 * 1024,            # 10 240
    ROOT / "docs" / "data.csv":      15 * 1024,            # 15 360
    ROOT / "images" / "photo1.jpg":  1 * 1024 * 1024,      # 1 048 576
    ROOT / "images" / "photo2.jpg":  int(1.5 * 1024 * 1024),  # 1 572 864
    ROOT / "README.md":              512,
}

TOTAL_BYTES_EXPECTED = 11_036_160

LARGE_FILE_THRESHOLD = 1_048_576  # 1 MiB *strictly greater* required
EXPECTED_LARGE_FILES_ORDERED = [
    ("large_video.bin", 5 * 1024 * 1024),
    ("archive.tar.gz", 3 * 1024 * 1024),
    ("images/photo2.jpg", int(1.5 * 1024 * 1024)),
]


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_root_directory_exists():
    assert ROOT.is_dir(), (
        f"Directory {ROOT} is missing — the initial data tree must be in place."
    )


@pytest.mark.parametrize("path,expected_size", EXPECTED_FILES.items())
def test_each_expected_file_exists_with_correct_size(path: Path, expected_size: int):
    assert path.is_file(), f"Expected file {path} does not exist."
    actual_size = path.stat().st_size
    assert actual_size == expected_size, (
        f"File {path} has size {actual_size} bytes, "
        f"but {expected_size} bytes were expected."
    )


def test_total_bytes_of_tree():
    total = 0
    for p in ROOT.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    assert total == TOTAL_BYTES_EXPECTED, (
        f"Total byte count of {ROOT} is {total}, "
        f"but {TOTAL_BYTES_EXPECTED} was expected."
    )


def test_large_files_list_and_order():
    # Gather every *regular* file > 1 048 576 bytes
    large_files = []
    for p in ROOT.rglob("*"):
        if p.is_file():
            size = p.stat().st_size
            if size > LARGE_FILE_THRESHOLD:
                rel_path = p.relative_to(ROOT).as_posix()
                large_files.append((rel_path, size))

    # Sort by size DESC, matching exercise requirement
    large_files.sort(key=lambda t: t[1], reverse=True)

    assert large_files, "No files larger than 1 MiB were found, but some were expected."
    assert large_files == EXPECTED_LARGE_FILES_ORDERED, (
        "The set (or ordering) of files larger than 1 MiB does not match the "
        "expected initial data.\n"
        f"Expected: {EXPECTED_LARGE_FILES_ORDERED}\n"
        f"Found:    {large_files}"
    )