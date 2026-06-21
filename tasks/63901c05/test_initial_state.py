# test_initial_state.py
#
# This pytest suite validates that the filesystem starts in the exact state
# stipulated by the task description *before* the student performs any action.

import os
from pathlib import Path

# Constant paths used throughout the tests
HOME = Path("/home/user")
PROJECTS_DIR = HOME / "projects"
OLD_DIR = PROJECTS_DIR / "old"
OUTPUT_FILE = PROJECTS_DIR / "python_file_list.txt"

# Expected files and directories
EXPECTED_TOP_LEVEL_PY = {
    "alpha.py",
    "beta.py",
    "gamma_processor.py",
    "zeta.py",
}

EXPECTED_OTHER_FILES = {
    "readme.md",
    "data.csv",
}

EXPECTED_OLD_PY = {"legacy.py"}


def test_projects_directory_exists_and_is_directory():
    assert PROJECTS_DIR.exists(), f"Expected directory {PROJECTS_DIR} is missing."
    assert PROJECTS_DIR.is_dir(), f"{PROJECTS_DIR} exists but is not a directory."


def test_expected_top_level_python_files_exist_and_no_extras():
    """
    1. Verify that each expected .py file exists and is a regular file.
    2. Verify that there are *no additional* .py files at the top level.
    """
    # Collect actual top-level .py files
    actual_py_files = {
        entry.name
        for entry in PROJECTS_DIR.iterdir()
        if entry.is_file() and entry.suffix == ".py"
    }

    # 1. All expected are present
    missing = EXPECTED_TOP_LEVEL_PY - actual_py_files
    assert not missing, (
        "The following expected Python files are missing from "
        f"{PROJECTS_DIR}: {', '.join(sorted(missing))}"
    )

    # 2. No unexpected .py files
    unexpected = actual_py_files - EXPECTED_TOP_LEVEL_PY
    assert not unexpected, (
        "Unexpected top-level .py files found in "
        f"{PROJECTS_DIR}: {', '.join(sorted(unexpected))}"
    )


def test_expected_non_python_files_exist():
    actual_other_files = {
        entry.name
        for entry in PROJECTS_DIR.iterdir()
        if entry.is_file() and entry.suffix != ".py"
    }

    missing = EXPECTED_OTHER_FILES - actual_other_files
    assert not missing, (
        "The following expected non-Python files are missing from "
        f"{PROJECTS_DIR}: {', '.join(sorted(missing))}"
    )


def test_old_directory_structure():
    # Old directory exists
    assert OLD_DIR.exists(), f"Expected directory {OLD_DIR} is missing."
    assert OLD_DIR.is_dir(), f"{OLD_DIR} exists but is not a directory."

    # legacy.py exists within old/
    legacy_path = OLD_DIR / "legacy.py"
    assert legacy_path.exists(), f"Expected file {legacy_path} is missing."
    assert legacy_path.is_file(), f"{legacy_path} exists but is not a regular file."

    # Ensure no extra .py files inside old/ beyond expected
    actual_old_py = {
        entry.name
        for entry in OLD_DIR.iterdir()
        if entry.is_file() and entry.suffix == ".py"
    }
    unexpected_old_py = actual_old_py - EXPECTED_OLD_PY
    assert not unexpected_old_py, (
        "Unexpected .py files found in "
        f"{OLD_DIR}: {', '.join(sorted(unexpected_old_py))}"
    )


def test_output_file_does_not_exist_yet():
    assert not OUTPUT_FILE.exists(), (
        f"{OUTPUT_FILE} should not exist before the student runs their command."
    )