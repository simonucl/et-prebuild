# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem / project state
# BEFORE the student runs any solution code.  These tests will fail
# immediately if the starting conditions described in the task
# description are not met.
#
# Only standard library + pytest are used.

from pathlib import Path
import pytest
import re

PROJECT_ROOT = Path("/home/user/project")
SRC_DIR       = PROJECT_ROOT / "src"
LOGS_DIR      = PROJECT_ROOT / "logs"
AUTHORS_CSV   = PROJECT_ROOT / "authors.csv"
PROCESSING_LOG = LOGS_DIR / "processing.log"

# Expected static metadata per file -------------------------------
EXPECTED_METADATA = {
    "db.py":    ("Alice Brown", "2023-05-10"),
    "main.py":  ("John Doe",    "2023-05-12"),
    "utils.py": ("Jane Smith",  "2023-05-11"),
}

@pytest.mark.parametrize("filename", EXPECTED_METADATA.keys())
def test_source_files_exist(filename):
    """Verify that each required source file is present."""
    path = SRC_DIR / filename
    assert path.is_file(), f"Expected file {path} to exist."

def test_logs_directory_exists_and_is_empty():
    """logs/ must exist and start out empty."""
    assert LOGS_DIR.is_dir(), f"Expected directory {LOGS_DIR} to exist."
    contents = list(LOGS_DIR.iterdir())
    assert len(contents) == 0, (
        f"logs directory should be empty initially, but contains: "
        f"{', '.join(str(p.name) for p in contents)}"
    )

@pytest.mark.parametrize("filename,expected", EXPECTED_METADATA.items())
def test_header_comments_and_metadata(filename, expected):
    """
    Ensure each .py file starts with exactly the two comment lines
    'Author: <name>' and 'Last Modified: <date>'.
    """
    author_expected, date_expected = expected
    path = SRC_DIR / filename
    with path.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Strip leading/trailing whitespace so indentation doesn't matter.
    stripped = [ln.strip() for ln in lines]

    # Find positions of Author and Last Modified lines (allow for optional
    # triple-quote lines on either side).
    try:
        author_idx = next(i for i, ln in enumerate(stripped) if ln.startswith("Author:"))
        date_idx   = next(i for i, ln in enumerate(stripped) if ln.startswith("Last Modified:"))
    except StopIteration:
        pytest.fail(
            f"{path} does not contain the required 'Author:' and "
            f"'Last Modified:' comment lines as the first two metadata lines."
        )

    assert author_idx < date_idx, (
        f"In {path} the 'Author:' line must appear before 'Last Modified:'."
    )

    # Verify exact metadata
    author_actual = stripped[author_idx].replace("Author:", "", 1).strip()
    date_actual   = stripped[date_idx].replace("Last Modified:", "", 1).strip()

    assert author_actual == author_expected, (
        f"{path}: Expected author '{author_expected}', found '{author_actual}'."
    )
    assert date_actual == date_expected, (
        f"{path}: Expected last-modified date '{date_expected}', found '{date_actual}'."
    )

@pytest.mark.parametrize("filename", EXPECTED_METADATA.keys())
def test_files_contain_tab_characters(filename):
    """
    Before processing, each source file must still contain at least one
    TAB character.  The follow-up task requires the student to replace them.
    """
    path = SRC_DIR / filename
    text = path.read_text(encoding="utf-8")
    assert "\t" in text, (
        f"{path} is expected to contain TAB characters before processing "
        "(none found)."
    )

def test_authors_csv_does_not_exist_yet():
    """authors.csv must *not* exist before the student's script runs."""
    assert not AUTHORS_CSV.exists(), (
        f"{AUTHORS_CSV} should not exist yet; it will be created by the solution."
    )

def test_processing_log_absent():
    """
    processing.log should not exist initially.  If it does,
    ensure it does NOT already contain the summary line expected after
    processing.
    """
    if not PROCESSING_LOG.exists():
        return  # Perfectly fine; nothing to check.
    tail = PROCESSING_LOG.read_text(encoding="utf-8").splitlines()[-1]
    assert tail.strip() != "Metadata extracted for 3 files", (
        f"{PROCESSING_LOG} already ends with the summary line that should be "
        f"added only after processing."
    )