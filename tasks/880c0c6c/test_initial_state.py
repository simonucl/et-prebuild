# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the workspace
_before_ the student performs any actions.

What we check (and why):
1. The drafts directory exists – the task depends on it.
2. Exactly three Markdown draft files are present with the expected names.
3. Each draft file contains **one** (and only one) top-level H1 heading.
4. Each draft file contains **exactly one** occurrence of the case-sensitive
   word “TBD” (the text that must later be replaced).
5. Each draft file has at least one line containing the string “TODO”.
6. None of the draft files already contain the replacement phrase
   “To Be Determined” (ensures the student still has work to do).

We explicitly do **not** check anything inside /home/user/docs/reports,
because those artefacts do **not** exist yet and are the deliverables
the student is going to create.
"""

import os
import re
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants used throughout the test suite
# ---------------------------------------------------------------------------
HOME = Path("/home/user")
DRAFTS_DIR = HOME / "docs" / "drafts"
DRAFT_FILENAMES = ("intro.md", "setup.md", "usage.md")
TBD_REGEX = re.compile(r"\bTBD\b")
H1_REGEX = re.compile(r"^# .+")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def read_file(path: Path) -> list[str]:
    """Return a list of lines (stripped of trailing newlines) from *path*."""
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_drafts_directory_exists():
    assert DRAFTS_DIR.exists(), f"Required directory {DRAFTS_DIR} is missing."
    assert DRAFTS_DIR.is_dir(), f"{DRAFTS_DIR} exists but is not a directory."


@pytest.mark.parametrize("filename", DRAFT_FILENAMES)
def test_markdown_file_exists(filename):
    path = DRAFTS_DIR / filename
    assert path.exists(), f"Expected file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."


@pytest.mark.parametrize("filename", DRAFT_FILENAMES)
def test_single_h1_heading_per_file(filename):
    path = DRAFTS_DIR / filename
    lines = read_file(path)
    h1_count = sum(1 for ln in lines if H1_REGEX.match(ln))
    assert (
        h1_count == 1
    ), f"{path} should contain exactly one top-level H1 heading, found {h1_count}."


@pytest.mark.parametrize("filename", DRAFT_FILENAMES)
def test_exactly_one_tbd_occurrence(filename):
    path = DRAFTS_DIR / filename
    text = path.read_text(encoding="utf-8")
    occurrences = TBD_REGEX.findall(text)
    assert (
        len(occurrences) == 1
    ), f"{path} should contain exactly one occurrence of 'TBD', found {len(occurrences)}."


@pytest.mark.parametrize("filename", DRAFT_FILENAMES)
def test_at_least_one_todo_line_present(filename):
    path = DRAFTS_DIR / filename
    lines = read_file(path)
    todo_lines = [ln for ln in lines if "TODO" in ln]
    assert (
        len(todo_lines) >= 1
    ), f"{path} should have at least one line containing 'TODO', found none."


@pytest.mark.parametrize("filename", DRAFT_FILENAMES)
def test_to_be_determined_not_yet_present(filename):
    path = DRAFTS_DIR / filename
    text = path.read_text(encoding="utf-8")
    assert (
        "To Be Determined" not in text
    ), f"{path} already contains 'To Be Determined' – nothing left to replace?"