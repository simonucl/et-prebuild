# test_initial_state.py
#
# Pytest suite that verifies the *initial* state of the filesystem
# before the student script runs.  It checks that the tiny demo
# project exists exactly as described in the task statement.

import os
from pathlib import Path

# Base paths
HOME = Path("/home/user")
PROJECT_ROOT = HOME / "projects"
APP_DIR = PROJECT_ROOT / "app"

# Expected file contents (lines **without** trailing newlines)
EXPECTED_FILES = {
    APP_DIR / "main.py": [
        "# Sample app",
        "def login():",
        "    # TODO: improve security",
        '    password = "12345"',
    ],
    APP_DIR / "utils.py": [
        "# utility",
        'secret_key = "abcde"',
        "def helper():",
        "    pass",
    ],
}


def test_project_root_exists():
    assert PROJECT_ROOT.is_dir(), (
        f"Directory {PROJECT_ROOT} is missing. "
        "The demo project must reside at /home/user/projects."
    )


def test_app_directory_exists():
    assert APP_DIR.is_dir(), (
        f"Directory {APP_DIR} is missing. "
        "The ‘app’ sub-directory must already exist."
    )


def test_required_source_files_exist():
    for path in EXPECTED_FILES:
        assert path.is_file(), f"Required file {path} is missing."


def test_no_unexpected_subdirectories_in_app():
    subdirs = [p for p in APP_DIR.iterdir() if p.is_dir()]
    assert not subdirs, (
        f"Unexpected sub-directories found in {APP_DIR}: "
        + ", ".join(str(p) for p in subdirs)
    )


def test_file_contents_are_exactly_as_expected():
    """
    Verifies that each required file contains exactly the 4 lines
    stipulated in the task description.
    """
    for path, expected_lines in EXPECTED_FILES.items():
        with path.open("r", encoding="utf-8") as fh:
            actual = [line.rstrip("\n") for line in fh.readlines()]

        # Helpful, granular assertion messages.
        assert len(actual) == len(
            expected_lines
        ), f"{path} should have {len(expected_lines)} lines, found {len(actual)}."

        for idx, (exp, act) in enumerate(zip(expected_lines, actual), start=1):
            assert (
                exp == act
            ), f"Line {idx} of {path} is incorrect.\nExpected: {exp!r}\nFound:    {act!r}"