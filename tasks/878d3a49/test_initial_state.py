# test_initial_state.py
#
# This pytest file validates the *initial* state of the workspace
# before the student attempts the exercise.  It checks that the
# expected source Markdown files are present with the correct first
#-line headings and that the artefacts to be created by the student
# (INDEX.md and index_build.log) are **not** present yet.
#
# The tests purposefully fail with clear, actionable messages if
# anything in the starting state is wrong or missing.
#
# Requirements checked:
#   1. /home/user/docs directory exists.
#   2. The three source files intro.md, usage.md, faq.md exist.
#   3. Each of the source files begins with the expected H1 heading.
#   4. No unexpected Markdown files exist in the directory.
#   5. INDEX.md and index_build.log do NOT exist yet.
#
# Only standard library and pytest are used.

from pathlib import Path
import pytest

# Constants for paths and expected data
DOCS_DIR = Path("/home/user/docs")
EXPECTED_MD_FILES = {
    "faq.md":    "# FAQ",
    "intro.md":  "# Introduction",
    "usage.md":  "# Usage Guide",
}
INDEX_FILE = DOCS_DIR / "INDEX.md"
LOG_FILE = DOCS_DIR / "index_build.log"


def _read_first_line(path: Path) -> str:
    """Return the first line of a file, stripped of trailing newline characters."""
    with path.open("r", encoding="utf-8") as fp:
        return fp.readline().rstrip("\n")


def test_docs_directory_exists():
    """/docs directory must be present."""
    assert DOCS_DIR.exists(), f"Directory {DOCS_DIR} is missing."
    assert DOCS_DIR.is_dir(), f"{DOCS_DIR} exists but is not a directory."


def test_source_markdown_files_present_with_correct_headings():
    """Verify each expected Markdown file is present and has the correct H1 heading."""
    for filename, expected_heading in EXPECTED_MD_FILES.items():
        file_path = DOCS_DIR / filename
        assert file_path.exists(), f"Expected source file {file_path} is missing."
        assert file_path.is_file(), f"{file_path} exists but is not a file."
        first_line = _read_first_line(file_path)
        assert first_line == expected_heading, (
            f"{file_path} first line mismatch.\n"
            f"Expected: {expected_heading!r}\n"
            f"Found:    {first_line!r}"
        )


def test_no_unexpected_markdown_files():
    """Ensure no extra *.md files are present before the task starts."""
    md_files = {p.name for p in DOCS_DIR.glob("*.md")}
    unexpected = md_files - set(EXPECTED_MD_FILES)
    assert unexpected == set(), (
        "Unexpected Markdown files present before exercise starts: "
        f"{', '.join(sorted(unexpected))}"
    )


def test_index_and_log_do_not_exist_yet():
    """INDEX.md and index_build.log should not exist before the student runs their solution."""
    assert not INDEX_FILE.exists(), f"{INDEX_FILE} should NOT exist before the task is attempted."
    assert not LOG_FILE.exists(), f"{LOG_FILE} should NOT exist before the task is attempted."