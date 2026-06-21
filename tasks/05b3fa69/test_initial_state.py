# test_initial_state.py
#
# Pytest suite that verifies the initial OS / filesystem state
# before the student performs any actions for the “SQLite catalogue”
# exercise.  It checks that the small project located in
# /home/user/my_project exists and that its three project files are
# present with the exact byte sizes expected by the grading rubric.
#
# IMPORTANT:  Per the instructions, this test file deliberately makes
# no assertions whatsoever about any output artefacts the student is
# required to create later (e.g., /home/user/my_project/db/,
# project_files.db, project_files_dump.sql, db_log.txt, etc.).
#
# Only the *pre-existing* files and directories are examined here.
import os
import stat
import pytest

PROJECT_DIR = "/home/user/my_project"

# (filename, expected_size_in_bytes)
FILES_EXPECTED = [
    ("main.py", 23),
    ("utils.py", 28),
    ("README.md", 49),
]


def test_project_directory_exists_and_is_readable():
    """
    Ensure /home/user/my_project exists, is a directory,
    and is readable by the current user.
    """
    assert os.path.exists(PROJECT_DIR), (
        f"Expected project directory '{PROJECT_DIR}' does not exist."
    )
    assert os.path.isdir(PROJECT_DIR), (
        f"'{PROJECT_DIR}' exists but is not a directory."
    )

    # Check that we have execute permission (to traverse) and read permission.
    mode = os.stat(PROJECT_DIR).st_mode
    can_traverse = bool(mode & stat.S_IXUSR)
    can_read = bool(mode & stat.S_IRUSR)
    assert can_traverse and can_read, (
        f"Insufficient permissions to access directory '{PROJECT_DIR}'. "
        "Expected read and execute permissions for the current user."
    )


@pytest.mark.parametrize("filename, expected_size", FILES_EXPECTED)
def test_project_files_exist_with_correct_size(filename: str, expected_size: int):
    """
    For each required file, verify that it:
      1. Exists at the expected absolute path.
      2. Is a regular file (not a directory, symlink, etc.).
      3. Has the exact byte size mandated by the exercise specification.
    """
    full_path = os.path.join(PROJECT_DIR, filename)

    # 1. Presence check
    assert os.path.exists(full_path), (
        f"Required file '{full_path}' is missing."
    )

    # 2. File-type check
    assert os.path.isfile(full_path), (
        f"'{full_path}' exists but is not a regular file."
    )

    # 3. Size check
    actual_size = os.path.getsize(full_path)
    assert actual_size == expected_size, (
        f"File '{full_path}' has size {actual_size} bytes, "
        f"but {expected_size} bytes were expected."
    )