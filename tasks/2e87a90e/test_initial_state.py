# test_initial_state.py
#
# This pytest suite validates the **initial** state of the filesystem
# before the student creates the Makefile or any output artefacts.
#
# It purposefully does NOT touch or assert anything about paths that
# will be generated later (html/, build/, documentation.zip, Makefile, …).

import pathlib
import pytest

BASE_DIR = pathlib.Path("/home/user/doc-project")
MARKDOWN_DIR = BASE_DIR / "markdown"
INTRO_MD = MARKDOWN_DIR / "intro.md"
SETUP_MD = MARKDOWN_DIR / "setup.md"


def _read_lines(path: pathlib.Path):
    """
    Return a list of lines **with** their trailing newline characters kept
    exactly as in the file.
    """
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


def test_directories_exist():
    assert BASE_DIR.is_dir(), f"Expected directory {BASE_DIR} to exist."
    assert MARKDOWN_DIR.is_dir(), (
        f"Expected directory {MARKDOWN_DIR} to exist inside {BASE_DIR}."
    )


@pytest.mark.parametrize("md_file", [INTRO_MD, SETUP_MD])
def test_markdown_files_exist(md_file):
    assert md_file.is_file(), f"Expected markdown file {md_file} to exist."


def test_intro_md_contents():
    lines = _read_lines(INTRO_MD)
    expected = [
        "# Introduction\n",
        "\n",
        "This is the introduction document.\n",
        "\n",
    ]
    assert (
        lines == expected
    ), f"{INTRO_MD} does not contain the expected 4 lines.\nExpected: {expected!r}\nFound: {lines!r}"


def test_setup_md_contents():
    lines = _read_lines(SETUP_MD)
    expected = [
        "# Setup\n",
        "\n",
        "Follow these steps to set up the project.\n",
        "\n",
    ]
    assert (
        lines == expected
    ), f"{SETUP_MD} does not contain the expected 4 lines.\nExpected: {expected!r}\nFound: {lines!r}"