# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the filesystem
# before the learner performs any actions.  Only the staged sources
# in /home/user/source_release are checked.  Output-related paths
# (/home/user/package, /home/user/testing_area, archives, listings,
# etc.) are deliberately **not** inspected, in accordance with
# grading rules.

import os
from pathlib import Path

SOURCE_DIR = Path("/home/user/source_release")
APP_FILE = SOURCE_DIR / "app.py"
REQ_FILE = SOURCE_DIR / "requirements.txt"


def test_source_directory_exists():
    """The source directory must be present."""
    assert SOURCE_DIR.is_dir(), (
        f"Expected directory {SOURCE_DIR} to exist, but it is missing."
    )


def test_source_directory_contents_exact():
    """
    The source directory must contain *exactly* two files:
    app.py and requirements.txt, and nothing else.
    """
    expected = {"app.py", "requirements.txt"}
    actual = {p.name for p in SOURCE_DIR.iterdir()}
    assert actual == expected, (
        f"{SOURCE_DIR} should contain exactly {sorted(expected)}; "
        f"found {sorted(actual)} instead."
    )


def test_app_py_contents():
    """app.py must contain the expected two-line Python script."""
    assert APP_FILE.is_file(), f"Missing file: {APP_FILE}"
    with APP_FILE.open("r", encoding="utf-8") as fh:
        contents = fh.read().splitlines()

    expected_lines = [
        "#!/usr/bin/env python3",
        'print("Hello, CI/CD!")',
    ]
    assert contents == expected_lines, (
        f"{APP_FILE} has unexpected contents.\n"
        f"Expected:\n{expected_lines}\n\nGot:\n{contents}"
    )


def test_requirements_txt_contents():
    """requirements.txt must pin the requests library to 2.31.0."""
    assert REQ_FILE.is_file(), f"Missing file: {REQ_FILE}"
    with REQ_FILE.open("r", encoding="utf-8") as fh:
        contents = fh.read().strip()

    expected = "requests==2.31.0"
    assert contents == expected, (
        f"{REQ_FILE} should contain exactly '{expected}' "
        f"(plus a trailing newline). Got: '{contents}'."
    )