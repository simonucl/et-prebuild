# test_initial_state.py
#
# Pytest suite to validate the initial filesystem state
# prior to the student running their rename command.
#
# The suite checks **only** the pre-existing situation:
#   1. /home/user/docs exists and is a directory.
#   2. The three “*_draft.txt” files exist.
#   3. Each draft file contains the exact expected text
#      (including its terminating newline).
#
# Per the grading-spec rules we intentionally do **not**
# look for, mention, or otherwise touch any of the output
# artefacts that will be created later (e.g. rename.log or
# “*_v1.txt” files).

import pathlib
import pytest

DOCS_DIR = pathlib.Path("/home/user/docs")

# Mapping: filename → expected file contents (with trailing newline).
EXPECTED_DRAFT_FILES = {
    "faq_draft.txt": "Frequently-asked questions draft.\n",
    "intro_draft.txt": "Introduction section draft.\n",
    "usage_draft.txt": "Usage instructions draft.\n",
}


def test_docs_directory_exists_and_is_dir():
    assert DOCS_DIR.exists(), f"Expected directory {DOCS_DIR} does not exist."
    assert DOCS_DIR.is_dir(), f"Expected {DOCS_DIR} to be a directory."


@pytest.mark.parametrize("filename,expected_content", EXPECTED_DRAFT_FILES.items())
def test_each_draft_file_exists_with_correct_content(filename, expected_content):
    file_path = DOCS_DIR / filename
    assert file_path.exists(), f"Required draft file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    # Read and compare file content.
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"Could not decode {file_path} as UTF-8: {exc}")

    assert (
        content == expected_content
    ), (
        f"Contents of {file_path} do not match the required initial text.\n"
        f"Expected:\n{expected_content!r}\nFound:\n{content!r}"
    )