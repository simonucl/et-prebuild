# test_initial_state.py
#
# This test-suite validates the starting filesystem layout *before*
# the student’s solution is executed.  It purposefully avoids checking
# for the presence (or absence) of any output artefacts such as the
# todo_summary.log file because those belong to the *post*-exercise
# state.
#
# The tests assert that:
#   • /home/user/docs exists and is a directory
#   • The expected sub-directories and Markdown files exist
#   • Each Markdown file’s exact content (line-by-line) matches what
#     the exercise description promises
#
# Only pytest + Python’s stdlib are used.

import os
import textwrap
import pytest

DOC_ROOT = "/home/user/docs"

# ---------------------------------------------------------------------------
# Expected layout and contents
# ---------------------------------------------------------------------------

EXPECTED_STRUCTURE = {
    "chapter1/introduction.md": textwrap.dedent(
        """\
        # Introduction
        Overview of the project.
        TODO: add more detail about scope
        Additional background text.
        TODO - revise later
        """
    ).splitlines(),
    "chapter1/setup.md": textwrap.dedent(
        """\
        # Setup
        Prerequisites
        Build instructions.
        TODO : include installation steps
        """
    ).splitlines(),
    "chapter2/advanced-topics.md": textwrap.dedent(
        """\
        # Advanced Topics
        TODO: add performance tips
        TODO - add case studies
        Completed first draft.
        """
    ).splitlines(),
}


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def abs_path(relative_path: str) -> str:
    """Return the absolute path inside DOC_ROOT for a given relative path."""
    return os.path.join(DOC_ROOT, relative_path)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_docs_root_exists_and_is_dir():
    assert os.path.isdir(DOC_ROOT), (
        f"Expected {DOC_ROOT} to exist and be a directory, "
        "but it is missing or not a directory."
    )


@pytest.mark.parametrize("relative_path", EXPECTED_STRUCTURE.keys())
def test_markdown_file_exists(relative_path):
    full_path = abs_path(relative_path)
    assert os.path.isfile(full_path), (
        f"Expected Markdown file '{full_path}' to exist, but it does not."
    )


@pytest.mark.parametrize("relative_path,expected_lines", EXPECTED_STRUCTURE.items())
def test_markdown_file_contents(relative_path, expected_lines):
    """
    Verify that each file’s *entire* content matches exactly what the
    exercise specifies (same text, same order, no extra/missing lines).
    """
    full_path = abs_path(relative_path)
    with open(full_path, encoding="utf-8") as fh:
        actual_lines = [line.rstrip("\n") for line in fh]

    # Helpful diagnostics on mismatch
    assert actual_lines == expected_lines, (
        f"Content mismatch in '{full_path}'.\n"
        f"Expected ({len(expected_lines)} lines):\n{expected_lines}\n"
        f"Actual ({len(actual_lines)} lines):\n{actual_lines}"
    )


def test_no_unexpected_markdown_files_present():
    """
    Ensure that only the Markdown files declared in EXPECTED_STRUCTURE
    are present under /home/user/docs.  This guards against accidental
    extra files influencing the exercise outcome.
    """
    discovered = []
    for root, _, files in os.walk(DOC_ROOT):
        for fname in files:
            if fname.lower().endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, fname), DOC_ROOT)
                discovered.append(rel_path)

    unexpected = sorted(set(discovered) - set(EXPECTED_STRUCTURE))
    assert not unexpected, (
        "Unexpected *.md files found under the docs tree which are not part "
        f"of the initial fixture: {unexpected}"
    )