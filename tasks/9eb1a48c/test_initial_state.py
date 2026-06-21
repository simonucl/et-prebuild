# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system /
# filesystem **before** the learner performs any actions for the “tidy up
# outline” exercise.
#
# The suite asserts the following initial conditions:
#   1. /home/user/architecture_outline.md exists as an ordinary file with the
#      exact two-line contents described in the task specification.
#   2. No /home/user/documentation directory (or any of its expected
#      sub-directories) exists yet.
#   3. No symlink has been created.
#   4. No log file has been produced.
#
# Only the Python standard library and pytest are used.

import os
import stat
from pathlib import Path

HOME = Path("/home/user")
DOC_ROOT = HOME / "documentation"
SOURCE_DIR = DOC_ROOT / "source"
REVIEW_DIR = DOC_ROOT / "review"
ORIGINAL_MD = HOME / "architecture_outline.md"
MOVED_MD = SOURCE_DIR / "architecture_outline.md"
SYMLINK = REVIEW_DIR / "architecture_outline.md"
LOG_FILE = HOME / "symlink_report.log"

EXPECTED_MD_CONTENT = "# System Architecture\nInitial outline.\n"


def test_original_file_present_with_correct_content():
    """
    The outline must initially exist as a *regular* file in /home/user with the
    precise two-line content (and trailing newline) shown in the instructions.
    """
    assert ORIGINAL_MD.exists(), (
        f"Expected initial file {ORIGINAL_MD} to exist, but it is missing."
    )
    assert ORIGINAL_MD.is_file(), (
        f"Expected {ORIGINAL_MD} to be a regular file, but it is not."
    )

    # Ensure it's not already a symlink.
    st = ORIGINAL_MD.lstat()
    assert not stat.S_ISLNK(st.st_mode), (
        f"Expected {ORIGINAL_MD} to be a regular file, "
        "but it is already a symbolic link."
    )

    content = ORIGINAL_MD.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_MD_CONTENT
    ), "The content of architecture_outline.md does not match the expected two-line outline."


def test_documentation_tree_absent():
    """
    No documentation directory tree should exist yet.
    """
    assert not DOC_ROOT.exists(), (
        f"Did not expect {DOC_ROOT} to exist before the task starts."
    )
    # If the root is absent, children must also be absent, but check explicitly
    # for clearer error messages in intermittent runs.
    assert not SOURCE_DIR.exists(), (
        f"{SOURCE_DIR} should not exist before the learner creates it."
    )
    assert not REVIEW_DIR.exists(), (
        f"{REVIEW_DIR} should not exist before the learner creates it."
    )


def test_symlink_and_log_absent():
    """
    The symlink inside review/ and the symlink report log must not be present
    before the learner performs any commands.
    """
    assert not SYMLINK.exists(), (
        f"Unexpected pre-existing symlink {SYMLINK}; the learner must create it."
    )
    assert not LOG_FILE.exists(), (
        f"Unexpected pre-existing log file {LOG_FILE}; the learner must create it."
    )


def test_moved_file_not_yet_present():
    """
    The file should not already be located in the destination directory prior to
    the learner’s action.
    """
    assert not MOVED_MD.exists(), (
        f"Found {MOVED_MD} already present, but the learner "
        "has not had a chance to move the file yet."
    )