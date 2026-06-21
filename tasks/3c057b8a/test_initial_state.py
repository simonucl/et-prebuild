# test_initial_state.py
#
# This pytest suite verifies that the *initial* filesystem state
# is exactly as expected **before** the student starts working on
# the assignment.  If any of these tests fail, the grading
# environment itself is wrong (or the student has already modified
# the system), so the subsequent “action” tests would be unreliable.

import os
from pathlib import Path

# Hard-coded absolute paths as required by the specification.
HOME_DIR               = Path("/home/user")
DOCS_WORKING_DIR       = HOME_DIR / "docs_working"
PRODUCTION_DOCS_DIR    = HOME_DIR / "production_docs"
SYNC_LOGS_DIR          = HOME_DIR / "sync_logs"
SYNC_LOG_FILE          = SYNC_LOGS_DIR / "sync_001.log"

def _dir_listing(path: Path):
    """
    Helper that returns a *deterministically sorted* list of items
    in a directory, excluding the special entries “.” and “..”.
    """
    return sorted(os.listdir(path))

def test_docs_working_exists_and_is_empty():
    assert DOCS_WORKING_DIR.exists(), (
        f"Expected directory {DOCS_WORKING_DIR} does not exist."
    )
    assert DOCS_WORKING_DIR.is_dir(), (
        f"{DOCS_WORKING_DIR} exists but is not a directory."
    )

    listing = _dir_listing(DOCS_WORKING_DIR)
    assert listing == [], (
        f"{DOCS_WORKING_DIR} should be empty but contains: {listing}"
    )

def test_production_docs_contains_only_two_expected_files():
    assert PRODUCTION_DOCS_DIR.exists(), (
        f"Expected directory {PRODUCTION_DOCS_DIR} does not exist."
    )
    assert PRODUCTION_DOCS_DIR.is_dir(), (
        f"{PRODUCTION_DOCS_DIR} exists but is not a directory."
    )

    expected_files = {"introduction.md", "obsolete.txt"}
    actual_files   = set(_dir_listing(PRODUCTION_DOCS_DIR))

    # 1. Directory should contain exactly the expected files (no more, no less)
    assert actual_files == expected_files, (
        f"{PRODUCTION_DOCS_DIR} should contain exactly {sorted(expected_files)} "
        f"but actually contains {sorted(actual_files)}"
    )

    # 2. Verify the *contents* of introduction.md
    intro_path = PRODUCTION_DOCS_DIR / "introduction.md"
    with intro_path.open("r", encoding="utf-8") as fp:
        content = fp.read()
    assert content == "Old content\n", (
        f"Unexpected content in {intro_path}. "
        f"Expected 'Old content\\n' but found: {repr(content)}"
    )

    # 3. Verify the *contents* of obsolete.txt
    obsolete_path = PRODUCTION_DOCS_DIR / "obsolete.txt"
    with obsolete_path.open("r", encoding="utf-8") as fp:
        content = fp.read()
    assert content == "remove me\n", (
        f"Unexpected content in {obsolete_path}. "
        f"Expected 'remove me\\n' but found: {repr(content)}"
    )

def test_sync_logs_directory_exists_and_is_empty():
    assert SYNC_LOGS_DIR.exists(), (
        f"Expected directory {SYNC_LOGS_DIR} does not exist."
    )
    assert SYNC_LOGS_DIR.is_dir(), (
        f"{SYNC_LOGS_DIR} exists but is not a directory."
    )

    listing = _dir_listing(SYNC_LOGS_DIR)
    assert listing == [] or listing == ["."], (
        f"{SYNC_LOGS_DIR} should be empty before the exercise starts, "
        f"but contains: {listing}"
    )

    # The specific log file should *not* exist yet.
    assert not SYNC_LOG_FILE.exists(), (
        f"{SYNC_LOG_FILE} should not exist before the sync operation."
    )