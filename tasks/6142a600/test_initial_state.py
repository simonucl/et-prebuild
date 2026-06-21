# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student performs any work on the “TSV merge” exercise.
#
# The tests assert that:
# 1. The three source TSV files exist *exactly* as specified.
# 2. Their byte-for-byte contents (including TABs and LF line endings) are correct.
# 3. No output artefacts (/home/user/documents/final/release_master.tsv and
#    /home/user/logs/merge_activities.log) exist yet.
#
# Only modules from the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DRAFTS_DIR = HOME / "documents" / "drafts"
FINAL_FILE = HOME / "documents" / "final" / "release_master.tsv"
LOG_FILE = HOME / "logs" / "merge_activities.log"

# ---------------------------------------------------------------------------#
# Helper utilities
# ---------------------------------------------------------------------------#
def read_binary(path: Path) -> bytes:
    """Return the raw bytes of *path* (raises pytest failure if not a file)."""
    if not path.is_file():
        pytest.fail(f"Expected file at {path} is missing.")
    return path.read_bytes()


def assert_exact_content(path: Path, expected: bytes) -> None:
    """Assert that *path* exists and its byte content matches *expected*."""
    actual = read_binary(path)
    if actual != expected:
        pytest.fail(
            f"Content mismatch in {path}.\n"
            "Expected (repr):\n"
            f"{repr(expected)}\n"
            "Actual (repr):\n"
            f"{repr(actual)}"
        )


def assert_not_exists(path: Path) -> None:
    """Fail if *path* exists (either as file or directory)."""
    if path.exists():
        pytest.fail(
            f"{path} should NOT exist before the student starts the task, "
            "but it is present."
        )

# ---------------------------------------------------------------------------#
# Expected byte-for-byte contents of the three initial TSV files
# (TAB = \t, LF = \n).  Each file has exactly four lines.
# ---------------------------------------------------------------------------#
CHAPTER_EXPECTED = (
    b"ChapterID\tSeq\tTitle\n"
    b"CH01\t1\tIntroduction\n"
    b"CH02\t2\tInstallation\n"
    b"CH03\t3\tConfiguration\n"
)

AUTHOR_EXPECTED = (
    b"ID\tAuthorName\tEmail\n"
    b"11\tAlice Johnson\talice@example.com\n"
    b"12\tBob Smith\tbob@example.com\n"
    b"13\tCarol Chen\tcarol@example.com\n"
)

RELEASE_EXPECTED = (
    b"Ref\tStage\tTargetDate\n"
    b"a\tdraft\t2023-10-01\n"
    b"b\treview\t2023-10-15\n"
    b"c\tfinal\t2023-11-01\n"
)

# Mapping of pathname → expected content for parametrised testing
INITIAL_FILES = {
    DRAFTS_DIR / "chapter_data.tsv": CHAPTER_EXPECTED,
    DRAFTS_DIR / "author_data.tsv": AUTHOR_EXPECTED,
    DRAFTS_DIR / "release_data.tsv": RELEASE_EXPECTED,
}

# ---------------------------------------------------------------------------#
# Test suite
# ---------------------------------------------------------------------------#
@pytest.mark.parametrize("filepath, expected", INITIAL_FILES.items())
def test_initial_tsv_files_exist_with_correct_content(filepath: Path, expected: bytes):
    """
    The three original TSV files must exist under /home/user/documents/drafts/
    and their contents must match the specification *exactly* (tabs, newlines,
    and byte order).
    """
    # Existence and exact byte match are checked by helper:
    assert_exact_content(filepath, expected)

    # Additional sanity checks: exactly 4 lines, and every line ends with LF.
    text = expected.decode("utf-8")
    lines = text.split("\n")
    assert lines[-1] == "", (
        f"{filepath} should end with a single LF on its last line."
    )
    assert len(lines) - 1 == 4, (
        f"{filepath} should contain exactly 4 lines "
        f"(found {len(lines)-1})."
    )


def test_output_files_do_not_exist_yet():
    """
    Before the merge task is carried out, neither the consolidated TSV file nor
    the command-journal log should exist anywhere on the filesystem.
    """
    assert_not_exists(FINAL_FILE)
    assert_not_exists(LOG_FILE)