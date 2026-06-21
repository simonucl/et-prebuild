# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem is in the
# expected *initial* state before the student performs any actions for the
# “backup-integrity engineer” task.  Only pre-existing items are tested; we do
# NOT look for the output artefacts that the student must eventually create.

import os
from collections import Counter
import pytest

# Constants for paths used throughout the tests
BACKUP_DIR = "/home/user/backup"
RAW_DIR = "/home/user/backup/raw"
CHECKSUM_FILE = "/home/user/backup/raw/file_checksums.csv"


def test_backup_directory_exists():
    """
    The top-level backup directory must be present.
    """
    assert os.path.isdir(
        BACKUP_DIR
    ), f"Required directory missing: {BACKUP_DIR!r}"


def test_raw_subdirectory_exists():
    """
    The raw subdirectory (where the original CSV resides) must be present.
    """
    assert os.path.isdir(
        RAW_DIR
    ), f"Required directory missing: {RAW_DIR!r}"


def test_checksum_file_exists():
    """
    The checksum CSV file must already exist and be a regular file.
    """
    assert os.path.isfile(
        CHECKSUM_FILE
    ), f"Required checksum file missing: {CHECKSUM_FILE!r}"


@pytest.fixture(scope="module")
def checksum_lines():
    """
    Read the checksum file once for the remaining tests.
    """
    with open(CHECKSUM_FILE, "r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]
    return lines


def test_checksum_file_line_count(checksum_lines):
    """
    The manifest is expected to contain exactly 10 lines (records).
    """
    expected_line_count = 10
    assert (
        len(checksum_lines) == expected_line_count
    ), f"{CHECKSUM_FILE} should contain {expected_line_count} lines, found {len(checksum_lines)}"


def test_unique_checksum_count(checksum_lines):
    """
    Exactly six distinct checksums must be present in the initial file.
    """
    checksums = [ln.split(" ", 1)[0] for ln in checksum_lines]
    unique_count = len(set(checksums))
    expected_unique = 6
    assert (
        unique_count == expected_unique
    ), f"Expected {expected_unique} unique checksums, found {unique_count}"


def test_duplicate_checksum_counts(checksum_lines):
    """
    Only 'abc123' and 'def456' should appear more than once,
    each appearing exactly three times.  All other checksums must be unique.
    """
    checksums = [ln.split(" ", 1)[0] for ln in checksum_lines]
    counts = Counter(checksums)

    # Expected duplicate map
    expected_dupes = {"abc123": 3, "def456": 3}

    # Verify the counts for expected duplicates
    for chk, expected_cnt in expected_dupes.items():
        assert (
            counts.get(chk, 0) == expected_cnt
        ), f"Checksum {chk!r} should appear {expected_cnt} times, found {counts.get(chk, 0)}"

    # Verify no other checksum appears more than once
    unexpected = {chk: cnt for chk, cnt in counts.items() if cnt > 1 and chk not in expected_dupes}
    assert (
        not unexpected
    ), f"Unexpected duplicate checksums found: {unexpected}"