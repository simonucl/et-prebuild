# test_initial_state.py
#
# Pytest suite that validates the INITIAL state of the filesystem
# **before** the student runs her/his sync-solution.  The checks make
# sure that the source files exist with the correct contents, that the
# destination directory exists but is completely EMPTY, and that no
# pre-existing log or summary files are present.
#
# Only the standard library and pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user").resolve()

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def read_text(path: Path) -> str:
    """Read a UTF-8 text file and return its content."""
    return path.read_text(encoding="utf-8")


def list_relative(dir_path: Path):
    """Return a sorted list of relative paths (str) below dir_path."""
    return sorted(
        str(p.relative_to(dir_path)) for p in dir_path.rglob("*") if p.is_file()
    )


# ----------------------------------------------------------------------
# Expected SOURCE state
# ----------------------------------------------------------------------
SRC_ROOT = HOME / "datasets" / "raw_data"

EXPECTED_SOURCE_FILES = {
    "exp1/results.csv": (
        "gene,expression\n"
        "BRCA1,5.6\n"
        "TP53,7.1\n"
    ),
    "exp1/notes.txt": (
        "Reminder: remove outliers before publication.\n"
    ),
    "exp1/.temp/cache.tmp": None,  # binary; we only test existence/size
    "exp2/data_part1.csv": (
        "sample_id,value\n"
        "S1,3.1\n"
        "S2,2.9\n"
    ),
    "exp2/data_part2.csv": (
        "sample_id,value\n"
        "S3,4.2\n"
        "S4,3.8\n"
    ),
    "exp2/.ignore": "",  # zero-length placeholder
}

# Destination and log paths
DEST_ROOT = HOME / "remote" / "mirror" / "data"
LOG_DIR = HOME / "sync_logs"
RSYNC_LOG = LOG_DIR / "rsync_latest.log"
TRANSFER_SUMMARY = DEST_ROOT / "TRANSFER_SUMMARY.txt"


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
def test_source_root_exists_and_is_directory():
    assert SRC_ROOT.is_dir(), (
        f"Expected source root directory {SRC_ROOT} to exist, "
        "but it is missing."
    )


@pytest.mark.parametrize("relpath, expected_content", EXPECTED_SOURCE_FILES.items())
def test_each_expected_source_file_exists_and_has_correct_content(relpath, expected_content):
    file_path = SRC_ROOT / relpath
    assert file_path.is_file(), f"Missing expected source file: {file_path}"

    # For text files we check exact content; for binary we just ensure size > 0.
    if expected_content is None:
        # Binary placeholder (cache.tmp)
        assert file_path.stat().st_size > 0, f"Binary file {file_path} is empty."
    else:
        actual_content = read_text(file_path)
        assert actual_content == expected_content, (
            f"Content mismatch in {file_path}.\n"
            "---- expected ----\n"
            f"{expected_content!r}\n"
            "---- got ----\n"
            f"{actual_content!r}"
        )


def test_no_unexpected_files_in_source():
    expected_paths_set = set(EXPECTED_SOURCE_FILES.keys())
    actual_paths_set = set(list_relative(SRC_ROOT))
    unexpected = actual_paths_set - expected_paths_set
    missing = expected_paths_set - actual_paths_set

    assert not missing, f"Missing expected files in {SRC_ROOT}: {sorted(missing)}"
    assert not unexpected, f"Found unexpected files in {SRC_ROOT}: {sorted(unexpected)}"


def test_destination_directory_exists_and_is_empty():
    assert DEST_ROOT.is_dir(), (
        f"Destination directory {DEST_ROOT} should exist but is missing."
    )

    contents = [p for p in DEST_ROOT.rglob("*") if p.is_file() or p.is_dir()]
    assert not contents, (
        f"Destination directory {DEST_ROOT} must be EMPTY before sync, "
        f"but it already contains: {sorted(str(p) for p in contents)}"
    )


def test_no_preexisting_log_or_summary_files():
    assert not RSYNC_LOG.exists(), (
        f"Log file {RSYNC_LOG} should NOT exist before the sync starts."
    )
    assert not TRANSFER_SUMMARY.exists(), (
        f"Summary file {TRANSFER_SUMMARY} should NOT exist before the sync starts."
    )