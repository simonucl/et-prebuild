# test_initial_state.py
#
# Pytest suite to validate the operating‐system / filesystem state
# BEFORE the student starts working on the “image/label data
# preparation” task.
#
# These tests assert that:
#   • All prerequisite source directories and files exist.
#   • No artefacts that the student is expected to create
#     (archives, logs, extracted folders, …) are present yet.
#
# Any failure message should give a clear indication of what is
# missing or unexpectedly present.

import os
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helper constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")

# Source data paths
DATASETS_DIR = HOME / "datasets"
RAW_IMAGES_DIR = DATASETS_DIR / "raw_images"
RAW_LABELS_DIR = DATASETS_DIR / "raw_labels"

# Directory that must already exist but be EMPTY
COMPRESSION_LOGS_DIR = HOME / "compression_logs"

# Artefacts that MUST *NOT* exist yet (to be created by the student)
ARCHIVE_PATH = DATASETS_DIR / "training_data.tar.gz"
EXTRACTED_DIR = DATASETS_DIR / "training_data_extracted"
ARCHIVE_CONTENTS_LOG = COMPRESSION_LOGS_DIR / "archive_contents.log"
VERIFICATION_LOG = COMPRESSION_LOGS_DIR / "verification.log"

# Expected file lists
RAW_IMAGES_FILES = {
    "cat_01.jpg",
    "cat_02.jpg",
    "dog_01.jpg",
    "dog_02.jpg",
    "LICENSE.txt",
    "ignore_me.tmp",
}

RAW_LABELS_FILES = {
    "cat_01.txt",
    "cat_02.txt",
    "dog_01.txt",
    "dog_02.txt",
    "notes.tmp",
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def _assert_dir_exists_and_only_contains(dir_path: Path, expected_filenames: set[str]) -> None:
    """
    Helper: ensure *dir_path* exists, is a directory, and its direct children
    match exactly the *expected_filenames* set (no missing, no extra).
    """
    assert dir_path.exists(), f"Required directory not found: {dir_path}"
    assert dir_path.is_dir(), f"Expected {dir_path} to be a directory."

    actual_filenames = {p.name for p in dir_path.iterdir()}
    missing = expected_filenames - actual_filenames
    extra = actual_filenames - expected_filenames

    assert not missing, (
        f"Directory {dir_path} is missing expected file(s): {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"Directory {dir_path} contains unexpected file(s): {', '.join(sorted(extra))}"
    )


def test_raw_images_directory_structure() -> None:
    """
    raw_images must exist and contain exactly the six predefined files
    (including the *.tmp file that will later be excluded from the archive).
    """
    _assert_dir_exists_and_only_contains(RAW_IMAGES_DIR, RAW_IMAGES_FILES)


def test_raw_labels_directory_structure() -> None:
    """
    raw_labels must exist and contain exactly the five predefined files
    (including the *.tmp file that will later be excluded from the archive).
    """
    _assert_dir_exists_and_only_contains(RAW_LABELS_DIR, RAW_LABELS_FILES)


def test_compression_logs_dir_is_present_and_empty() -> None:
    """
    The /home/user/compression_logs directory must exist so that the student
    can write logs into it, but it should be completely empty at the start.
    """
    assert COMPRESSION_LOGS_DIR.exists(), (
        f"Required directory not found: {COMPRESSION_LOGS_DIR}"
    )
    assert COMPRESSION_LOGS_DIR.is_dir(), (
        f"Expected {COMPRESSION_LOGS_DIR} to be a directory."
    )

    # Filter out hidden files (e.g., .DS_Store) just in case—only visible files matter.
    visible_entries = [p for p in COMPRESSION_LOGS_DIR.iterdir() if not p.name.startswith(".")]
    assert not visible_entries, (
        f"{COMPRESSION_LOGS_DIR} should be empty but contains: "
        f"{', '.join(sorted(p.name for p in visible_entries))}"
    )


@pytest.mark.parametrize(
    "path",
    [
        ARCHIVE_PATH,
        EXTRACTED_DIR,
        ARCHIVE_CONTENTS_LOG,
        VERIFICATION_LOG,
    ],
)
def test_output_artefacts_do_not_exist_yet(path: Path) -> None:
    """
    None of the artefacts that the student is supposed to create should exist
    before they start. If any of these paths are present, the initial state is
    incorrect.
    """
    assert not path.exists(), (
        f"Path {path} already exists, but it should be created by the student "
        "as part of the task."
    )