# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that is expected
# to exist *before* the student performs any actions.  If any of these tests
# fail it means the playground is not set up as described in the task
# statement.

import os
import stat
import pytest
from pathlib import Path

# Base directory that must already exist
BASE_DIR = Path("/home/user/release").resolve()

###############################################################################
# Helper utilities
###############################################################################
def _assert_is_file(path: Path):
    assert path.exists(), f"Expected file {path} to exist but it is missing."
    assert path.is_file(), f"Expected {path} to be a regular file."


def _assert_is_dir(path: Path):
    assert path.exists(), f"Expected directory {path} to exist but it is missing."
    assert path.is_dir(), f"Expected {path} to be a directory."


def _mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


###############################################################################
# Directory structure tests
###############################################################################
def test_release_directory_structure_exists():
    """
    The entire /home/user/release tree must already exist with the correct
    sub-directories.
    """
    _assert_is_dir(BASE_DIR)

    expected_dirs = [
        BASE_DIR / "config",
        BASE_DIR / "static",
        BASE_DIR / "tmp",
    ]

    for d in expected_dirs:
        _assert_is_dir(d)


###############################################################################
# File presence & permissions
###############################################################################

@pytest.mark.parametrize(
    "file_path, expected_mode",
    [
        (BASE_DIR / "app.py", 0o644),
        (BASE_DIR / "config" / "settings.conf", 0o600),
        (BASE_DIR / "static" / "logo.png", 0o666),   # world-writable
        (BASE_DIR / "tmp" / "debug.log", 0o777),     # world-writable
    ],
)
def test_files_exist_with_correct_permissions(file_path: Path, expected_mode: int):
    """
    Verify that each required file exists and has exactly the permission bits
    declared in the task description.
    """
    _assert_is_file(file_path)
    actual_mode = _mode(file_path)
    assert (
        actual_mode == expected_mode
    ), f"File {file_path} has mode {oct(actual_mode)}, expected {oct(expected_mode)}."


def test_world_writable_files_are_flagged_correctly():
    """
    Specifically ensure that the two files called out as world-writable really
    are world-writable (i.e. 'other' write bit is set).
    """
    for path in (
        BASE_DIR / "static" / "logo.png",
        BASE_DIR / "tmp" / "debug.log",
    ):
        _assert_is_file(path)
        assert (
            _mode(path) & 0o002
        ), f"File {path} is expected to be world-writable but it is not."


###############################################################################
# File content verification
###############################################################################

def test_app_py_contains_todo_line():
    """
    app.py must contain the specific TODO line on line 3.
    """
    app_py = BASE_DIR / "app.py"
    _assert_is_file(app_py)

    with app_py.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Ensure at least 3 lines exist
    assert len(lines) >= 3, "app.py should have at least 3 lines."
    expected_line = "    pass  # TODO Update database credentials\n"
    assert (
        lines[2] == expected_line
    ), f"Line 3 of app.py is incorrect.\nExpected: {expected_line!r}\nFound   : {lines[2]!r}"


def test_debug_log_contains_todo_line():
    """
    tmp/debug.log must have the first line exactly as described.
    """
    dbg_log = BASE_DIR / "tmp" / "debug.log"
    _assert_is_file(dbg_log)

    with dbg_log.open("r", encoding="utf-8") as fh:
        first_line = fh.readline()

    expected_line = "TODO remove debug statements before production\n"
    assert (
        first_line == expected_line
    ), f"First line of debug.log is incorrect.\nExpected: {expected_line!r}\nFound   : {first_line!r}"