# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the student carries out any actions for the “compressed-backup”
# exercise described in the instructions.
#
# The tests make sure that:
#   1. /home/user/project_docs/ exists and already contains the three
#      expected draft files with the correct contents.
#   2. No archive, extracted copy, or log file from the task is present
#      yet.  (The student has not started the exercise.)
#
# Only the Python standard library and pytest are used.
#
# If any test fails, the assertion message pinpoints what is missing or
# unexpectedly present, giving the learner a clear hint about the mismatch
# with the expected initial environment.
#
# ----------------------------------------------------------------------

import os
from pathlib import Path

# --- Constants ---------------------------------------------------------

HOME = Path("/home/user")
PROJECT_DOCS_DIR = HOME / "project_docs"
ARCHIVES_DIR = HOME / "archives"
REVIEW_DOCS_DIR = HOME / "review_docs"

ARCHIVE_FILE = ARCHIVES_DIR / "project_docs_20230115.tar.gz"
LOG_FILE = ARCHIVES_DIR / "compression_log.txt"

EXPECTED_FILES = {
    "intro.txt": "Welcome to the intro.",
    "usage.txt": "Usage instructions go here.",
    "changelog.txt": "Changelog:\n* Initial draft completed.",
}


# --- Helper ------------------------------------------------------------

def read_file(path: Path) -> str:
    """
    Return the full textual content of *path* using UTF-8 encoding.

    The helper guarantees the file is closed promptly and always returns a
    string (no trailing newline trimming is performed so that assertions
    can be explicit about newline handling when needed).
    """
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


# --- Tests -------------------------------------------------------------

def test_project_docs_directory_exists_and_is_correct_type():
    """
    The /home/user/project_docs/ directory *must* exist before the student
    begins; it contains the draft documentation to be archived.
    """
    assert PROJECT_DOCS_DIR.exists(), (
        f"Required directory {PROJECT_DOCS_DIR} is missing.  "
        "The initial draft files should already be available."
    )
    assert PROJECT_DOCS_DIR.is_dir(), (
        f"{PROJECT_DOCS_DIR} exists but is not a directory."
    )


def test_project_docs_files_present_with_expected_content():
    """
    Each of the three draft files must already exist and contain the exact
    text stated in the spec.  We compare without enforcing the presence of
    a final trailing newline for robustness, but the main body of the text
    must match verbatim.
    """
    for filename, expected_content in EXPECTED_FILES.items():
        file_path = PROJECT_DOCS_DIR / filename

        # Existence and correct file type
        assert file_path.exists(), (
            f"Expected draft file {file_path} is missing."
        )
        assert file_path.is_file(), (
            f"{file_path} exists but is not a regular file."
        )

        # Content check (ignore a single optional trailing newline)
        actual_content = read_file(file_path)
        if actual_content.endswith("\n") and not expected_content.endswith("\n"):
            actual_content = actual_content[:-1]  # strip exactly one trailing \n
        assert actual_content == expected_content, (
            f"Contents of {file_path} do not match the expected initial draft "
            "text.  The environment should provide the pristine drafts."
        )


def test_archive_file_not_present_yet():
    """
    The compressed archive should *not* exist before the student does the
    exercise.  Its presence would indicate that the tasks have already been
    run or the environment is in an unexpected state.
    """
    assert not ARCHIVE_FILE.exists(), (
        f"{ARCHIVE_FILE} already exists, but the archive is supposed to be "
        "created by the student."
    )


def test_log_file_not_present_yet():
    """
    The log file documenting the compression operation must not exist yet.
    """
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists, but the student has not created it yet."
    )


def test_review_docs_directory_not_present_yet():
    """
    The extraction target directory should not exist before the student
    performs the extraction step.
    """
    assert not REVIEW_DOCS_DIR.exists(), (
        f"{REVIEW_DOCS_DIR} already exists, but it should be created only "
        "after the archive is extracted."
    )