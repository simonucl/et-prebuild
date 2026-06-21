# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state for the
# “mock_api_data” exercise.  It purposefully avoids checking for any
# output artefacts (e.g. the report file) so that it can be executed
# before the student begins the task.
#
# Requirements verified:
#   • Presence of the expected directory tree.
#   • Presence of the four JSON payload / response files.
#   • Exact file sizes in bytes.
#   • Correct aggregate byte-counts for the raw, processed and total
#     sub-trees.
#
# Only stdlib + pytest are used.

import os
from pathlib import Path
import stat

import pytest

HOME = Path("/home/user")
ROOT_DIR = HOME / "mock_api_data"
RAW_DIR = ROOT_DIR / "raw"
PROCESSED_DIR = ROOT_DIR / "processed"

EXPECTED_FILES = {
    RAW_DIR / "payload_01.json": 512,
    RAW_DIR / "payload_02.json": 256,
    PROCESSED_DIR / "response_01.json": 128,
    PROCESSED_DIR / "response_02.json": 256,
}

EXPECTED_RAW_BYTES = 512 + 256  # 768
EXPECTED_PROCESSED_BYTES = 128 + 256  # 384
EXPECTED_TOTAL_BYTES = EXPECTED_RAW_BYTES + EXPECTED_PROCESSED_BYTES  # 1152


def _file_size(path: Path) -> int:
    """Return file size in bytes using os.stat(…)[stat.ST_SIZE]."""
    return path.stat().st_size


def test_directories_exist():
    """Ensure the root, raw, and processed directories exist and are directories."""
    for directory in (ROOT_DIR, RAW_DIR, PROCESSED_DIR):
        assert directory.exists(), f"Expected directory {directory} is missing."
        assert directory.is_dir(), f"{directory} exists but is not a directory."


@pytest.mark.parametrize("path, expected_size", EXPECTED_FILES.items())
def test_files_exist_with_correct_size(path: Path, expected_size: int):
    """Each expected JSON file must exist with the exact byte size."""
    assert path.exists(), f"Required file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."
    actual_size = _file_size(path)
    assert (
        actual_size == expected_size
    ), f"File {path} has {actual_size} bytes; expected {expected_size}."


def test_aggregate_byte_counts():
    """Validate raw_bytes, processed_bytes, and total_bytes aggregates."""
    raw_sum = sum(
        _file_size(p) for p in EXPECTED_FILES if p.parent == RAW_DIR
    )
    processed_sum = sum(
        _file_size(p) for p in EXPECTED_FILES if p.parent == PROCESSED_DIR
    )
    total_sum = raw_sum + processed_sum

    assert raw_sum == EXPECTED_RAW_BYTES, (
        f"Sum of raw bytes is {raw_sum}; expected {EXPECTED_RAW_BYTES}."
    )
    assert processed_sum == EXPECTED_PROCESSED_BYTES, (
        f"Sum of processed bytes is {processed_sum}; expected {EXPECTED_PROCESSED_BYTES}."
    )
    assert total_sum == EXPECTED_TOTAL_BYTES, (
        f"Total bytes is {total_sum}; expected {EXPECTED_TOTAL_BYTES}."
    )