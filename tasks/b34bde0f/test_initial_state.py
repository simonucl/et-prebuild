# test_initial_state.py
#
# Pytest suite to confirm that the operating-system / file-system is
# in the expected *clean* state **before** the student performs any
# actions for the “text-encoding regression suite” exercise.
#
# The tests make sure that:
#   • the working directory /home/user/encoding_tests does NOT yet
#     contain any of the required artefacts (and preferably does not
#     exist at all);
#   • none of the files the student has to create are already present;
#   • the standard utility `iconv` that the student will need is
#     available in $PATH.
#
# Only the Python standard library and pytest are used.


import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Constants describing the expected “clean slate”.
# ---------------------------------------------------------------------------

EXPECT_DIR = Path("/home/user/encoding_tests")

REQUIRED_BASENAMES = [
    "utf8_spanish.txt",
    "iso_french.txt",
    "utf8_spanish_iso.txt",
    "iso_french_utf8.txt",
    "conversion_results.log",
]

REQUIRED_PATHS = [EXPECT_DIR / name for name in REQUIRED_BASENAMES]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def human_readable_file_list(path: Path):
    """
    Produce a human-readable, sorted file list of `path`.
    If the path does not exist, returns the string '<non-existent>'.
    """
    if not path.exists():
        return "<non-existent>"
    if not path.is_dir():
        return f"<exists but is NOT a directory: {path}>"
    contents = sorted(p.name for p in path.iterdir())
    return " ".join(contents) if contents else "<empty directory>"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_working_directory_absent_or_empty():
    """
    The directory /home/user/encoding_tests should *not* contain any files
    before the student starts.  It is acceptable if it does not yet exist;
    it is also acceptable if it exists but is still completely empty.
    """
    if not EXPECT_DIR.exists():
        # Preferred case: the directory does not exist yet.
        assert True
    else:
        # Fallback: it exists, but must be completely empty.
        contents = list(EXPECT_DIR.iterdir())
        assert (
            len(contents) == 0
        ), (
            f"The directory {EXPECT_DIR} should be empty before the task begins.\n"
            f"Current contents: {human_readable_file_list(EXPECT_DIR)}"
        )


@pytest.mark.parametrize("path", REQUIRED_PATHS)
def test_required_files_do_not_exist_yet(path: Path):
    """
    None of the five files that the student has to create should already
    be present.
    """
    assert (
        not path.exists()
    ), (
        f"The file {path} should NOT exist before the student starts the task.\n"
        f"Found it unexpectedly in the filesystem."
    )


def test_iconv_available():
    """
    The exercise instructions explicitly mention the `iconv` tool, so it
    must be available in the current environment.
    """
    iconv_path = shutil.which("iconv")
    assert (
        iconv_path is not None
    ), "The `iconv` utility is required but could not be found in $PATH."