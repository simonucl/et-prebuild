# test_initial_state.py
#
# This pytest file validates that the *initial* on-disk state exactly matches
# what the assignment description promises.  It checks only the pre-existing
# files/directories and never looks for the output file that the student is
# supposed to create later.

import pathlib
import re
import pytest

# Base directory that must already exist
BASE_DIR = pathlib.Path("/home/user/restore-tests").resolve()

# Absolute paths of the two Markdown files that must already exist
STEP1 = BASE_DIR / "step1.md"
STEP2 = BASE_DIR / "step2.md"

@pytest.fixture(scope="module")
def md_files():
    """
    Return a list of all *.md files found under BASE_DIR (recursively).
    """
    return list(BASE_DIR.rglob("*.md"))

def test_base_directory_exists():
    assert BASE_DIR.is_dir(), f"Required directory {BASE_DIR} is missing."

def test_required_files_exist(md_files):
    """
    Ensure that exactly the expected Markdown files are present and nothing else.
    """
    paths = {p.resolve() for p in md_files}
    expected = {STEP1.resolve(), STEP2.resolve()}
    missing = expected - paths
    extra   = paths - expected

    assert not missing, f"The following required file(s) are missing: {', '.join(map(str, missing))}"
    assert not extra,   f"Unexpected Markdown file(s) present: {', '.join(map(str, extra))}"

def test_step1_exact_content():
    """
    Validate the exact content of /home/user/restore-tests/step1.md.

    Expected (␠ represents an ordinary space character, \n the newline):

        Restore Step 1␠␠\n
        Run backup command.\n
    """
    expected_lines = [
        "Restore Step 1  \n",       # two trailing spaces
        "Run backup command.\n",
    ]

    with STEP1.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == expected_lines, (
        f"Content of {STEP1} does not match the expected two-line text with "
        f"two trailing spaces at the end of line 1.\n"
        f"Expected lines:\n{repr(expected_lines)}\n"
        f"Actual lines:\n{repr(actual_lines)}"
    )

def test_step2_exact_content():
    """
    Validate the exact content of /home/user/restore-tests/step2.md.

    Expected:

        Restore Step 2\n
        Verify backup.\n
    """
    expected_lines = [
        "Restore Step 2\n",
        "Verify backup.\n",
    ]

    with STEP2.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == expected_lines, (
        f"Content of {STEP2} does not match the expected two-line text.\n"
        f"Expected lines:\n{repr(expected_lines)}\n"
        f"Actual lines:\n{repr(actual_lines)}"
    )

def test_only_one_trailing_whitespace_line(md_files):
    """
    Across *all* Markdown files in the directory tree, exactly one line
    (Step 1, line 1) must have trailing whitespace (space or tab characters).
    """
    trailing_pattern = re.compile(r"[ \t]+$")

    offenders = []  # list of (path, line_number, line_text)
    for path in md_files:
        with path.open("r", encoding="utf-8") as fh:
            for idx, line in enumerate(fh, start=1):
                if trailing_pattern.search(line.rstrip("\n")):
                    offenders.append((path, idx, line))

    # Exactly one offending line expected
    assert len(offenders) == 1, (
        f"Expected exactly one line with trailing whitespace, "
        f"but found {len(offenders)}.\n"
        f"Details: {offenders}"
    )

    offending_path, offending_lineno, offending_text = offenders[0]
    assert offending_path.resolve() == STEP1.resolve() and offending_lineno == 1, (
        "The only line with trailing whitespace should be line 1 of "
        f"{STEP1}, but got {offending_path}:{offending_lineno}"
    )

    # Confirm the text matches exactly with two trailing spaces
    assert offending_text == "Restore Step 1  \n", (
        f"The offending line's content is unexpected:\n{repr(offending_text)}"
    )