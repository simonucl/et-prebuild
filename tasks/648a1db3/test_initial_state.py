# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student starts working on the “symlink-task”.
#
# It purposefully does **not** check for any of the files or directories
# that the student is supposed to create (e.g. “/home/user/project/bin/…”
# or “/home/user/symlink-task/verification.log”), because those are
# expected to be missing at this point.

import os
import stat
import pytest

PROJECT_DIR = "/home/user/project"
SRC_DIR = os.path.join(PROJECT_DIR, "src")
MAIN_PY = os.path.join(SRC_DIR, "main.py")


def _assert_path_is_dir(path: str):
    assert os.path.exists(path), f"Expected directory {path!r} to exist, but it is missing."
    assert os.path.isdir(path), f"Expected {path!r} to be a directory."


def _assert_path_is_file(path: str):
    assert os.path.exists(path), f"Expected file {path!r} to exist, but it is missing."
    assert os.path.isfile(path), f"Expected {path!r} to be a regular file."


def test_project_directory_exists_and_is_directory():
    """
    The top-level project directory must already exist.
    """
    _assert_path_is_dir(PROJECT_DIR)


def test_src_directory_exists_and_is_directory():
    """
    The “src” sub-directory must already exist inside the project directory.
    """
    _assert_path_is_dir(SRC_DIR)


def test_main_py_exists_and_has_expected_content():
    """
    Verifies that /home/user/project/src/main.py exists, is a regular file,
    is executable, and contains the expected shebang and print statement.
    """
    _assert_path_is_file(MAIN_PY)

    # Confirm the file is executable by *someone* (any execute bit set).
    st_mode = os.stat(MAIN_PY).st_mode
    assert st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH), (
        f"{MAIN_PY!r} should be executable (have at least one execute bit set)."
    )

    # Read the file and validate its contents.
    with open(MAIN_PY, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Expected minimal contents:
    expected_first_line = "#!/usr/bin/env python3"
    expected_second_line = 'print("Hello from main!")'

    assert lines, f"{MAIN_PY!r} is empty."
    assert lines[0].strip() == expected_first_line, (
        f"The first line of {MAIN_PY!r} should be exactly {expected_first_line!r} "
        f"but got {lines[0]!r}."
    )
    assert any(expected_second_line == line.strip() for line in lines), (
        f"{MAIN_PY!r} should contain the line {expected_second_line!r}."
    )