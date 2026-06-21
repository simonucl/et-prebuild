# test_initial_state.py
#
# Pytest suite that validates the filesystem *before* the student performs the
# actions described in the assignment.  These tests assert the presence and
# basic contents of the pre-existing project tree so that subsequent grading
# steps can rely on a known good starting point.
#
# Only the initial state is verified; the tests intentionally make **no**
# reference to any files or directories the student is supposed to create
# (e.g. benchmarks/, benchmark.log, src.tar.gz).

import os
import stat
import pytest

PROJECT_ROOT = "/home/user/project"
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
UTILS_DIR = os.path.join(SRC_DIR, "utils")
TIME_BINARY = "/usr/bin/time"
README = os.path.join(PROJECT_ROOT, "README.md")
INIT_PY = os.path.join(SRC_DIR, "__init__.py")
MAIN_PY = os.path.join(SRC_DIR, "main.py")
HELPERS_PY = os.path.join(UTILS_DIR, "helpers.py")


def assert_path_is_file(path: str):
    assert os.path.isfile(path), f"Expected file does not exist: {path}"


def assert_path_is_dir(path: str):
    assert os.path.isdir(path), f"Expected directory does not exist: {path}"


def test_project_root_exists_and_writable():
    """
    The project root must exist *and* be writable by the current user so that
    benchmark artefacts can be created later.
    """
    assert_path_is_dir(PROJECT_ROOT)

    # Root must be writable
    assert os.access(PROJECT_ROOT, os.W_OK), (
        f"Project root {PROJECT_ROOT} is not writable; "
        "student will be unable to create benchmark artefacts."
    )


def test_readme_exists_and_has_minimum_lines():
    """
    README.md must exist and contain at least 5 lines.
    """
    assert_path_is_file(README)

    with open(README, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert len(lines) >= 5, (
        f"{README} should have at least 5 lines; "
        f"found only {len(lines)}."
    )


def test_src_tree_structure():
    """
    Validate the source tree skeleton that exists before the student works.
    """
    # Directories
    assert_path_is_dir(SRC_DIR)
    assert_path_is_dir(UTILS_DIR)

    # Files
    assert_path_is_file(INIT_PY)
    assert_path_is_file(MAIN_PY)
    assert_path_is_file(HELPERS_PY)

    # __init__.py must be empty
    assert os.path.getsize(INIT_PY) == 0, (
        f"{INIT_PY} is expected to be empty but is not."
    )

    # main.py should contain the canonical Hello-world line
    with open(MAIN_PY, "r", encoding="utf-8") as fh:
        content = fh.read()
    assert "print('Hello world')" in content.replace('"', "'"), (
        f"{MAIN_PY} should contain print('Hello world') but does not."
    )

    # helpers.py should declare a helper() function
    with open(HELPERS_PY, "r", encoding="utf-8") as fh:
        helpers_py_src = fh.read()
    assert "def helper(" in helpers_py_src, (
        f"{HELPERS_PY} should define a function named helper()."
    )


def test_time_binary_available_and_executable():
    """
    The external timing binary /usr/bin/time must be present and executable.
    """
    assert_path_is_file(TIME_BINARY)

    mode = os.stat(TIME_BINARY).st_mode
    assert mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH), (
        f"{TIME_BINARY} exists but is not executable."
    )