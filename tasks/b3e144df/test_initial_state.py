# test_initial_state.py
#
# Pytest suite that validates the initial, **pre-task** state of the filesystem
# for the “CONFIDENTIAL file-copy” workflow exercise.
#
# The tests assert that:
#   • The source directory /home/user/project/data/raw exists.
#   • The five expected files exist inside that directory.
#   • The word “CONFIDENTIAL” appears exactly where the specification says it
#     should (and does NOT appear where it should not).
#   • The target directory /home/user/project/data/processed does NOT exist yet
#     (no work has been done).
#
# Any failure message pinpoints precisely what is wrong so the student can fix
# the environment before starting the assignment.

import os
from pathlib import Path

# Base paths
HOME = Path("/home/user")
PROJECT_ROOT = HOME / "project" / "data"
RAW_DIR = PROJECT_ROOT / "raw"
PROCESSED_DIR = PROJECT_ROOT / "processed"

# Expected files inside RAW_DIR
EXPECTED_RAW_FILES = {
    "report1.txt",
    "report2.txt",
    "secret_notes.txt",
    "analysis.txt",
    "draft.log",
}


def read_file_text(path: Path) -> str:
    """
    Helper to read text from a file using UTF-8 while falling back to locale
    default if necessary.
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text()  # Fallback to system default


def test_raw_directory_exists():
    assert RAW_DIR.is_dir(), (
        f"Required source directory {RAW_DIR} is missing. "
        "Create it and populate it with the specified files."
    )


def test_expected_files_present_in_raw_dir():
    actual_files = {p.name for p in RAW_DIR.iterdir() if p.is_file()}
    missing = EXPECTED_RAW_FILES - actual_files
    unexpected = actual_files - EXPECTED_RAW_FILES

    assert not missing, (
        f"The following required file(s) are missing from {RAW_DIR}: "
        f"{', '.join(sorted(missing))}"
    )

    # The presence of extra files is tolerated EXCEPT for any that would belong
    # to the yet-to-be-created processed directory.  This keeps the check strict
    # without being brittle.
    forbidden_extras = {f for f in unexpected if f.endswith("_secured.txt")}
    assert not forbidden_extras, (
        "Found file(s) that look like post-processing artefacts inside the raw "
        f"directory: {', '.join(sorted(forbidden_extras))}. "
        "The workspace should be untouched before running the task."
    )


def test_confidential_content_flags():
    """
    Verify which files do / do not contain the exact uppercase string
    'CONFIDENTIAL', according to the specification.
    """
    # Files that MUST contain the string
    must_contain = {
        RAW_DIR / "report1.txt",
        RAW_DIR / "secret_notes.txt",
        RAW_DIR / "analysis.txt",
    }

    # Files that MUST NOT contain the string
    must_not_contain = {
        RAW_DIR / "report2.txt",
    }

    for path in must_contain:
        text = read_file_text(path)
        assert "CONFIDENTIAL" in text, (
            f"File {path} should contain the exact string 'CONFIDENTIAL' but "
            "it does not."
        )

    for path in must_not_contain:
        text = read_file_text(path)
        assert "CONFIDENTIAL" not in text, (
            f"File {path} should NOT contain the string 'CONFIDENTIAL', but it "
            "does. Ensure the initial data matches the specification."
        )


def test_processed_directory_not_present_yet():
    assert not PROCESSED_DIR.exists(), (
        f"Directory {PROCESSED_DIR} already exists, indicating that processing "
        "may have been run prematurely. Remove/rename it before starting the "
        "exercise so the automated tests can validate your work from a clean "
        "state."
    )