# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must
# be present before the student performs any actions.  It deliberately
# avoids checking for the output directory (/home/user/perm_audit) or
# its contents, because those are part of the required *end-state*.
#
# The tests confirm that the sample directory tree handed to the
# student by the “security auditor” exists exactly as described.

import os
import stat
import pytest

# Absolute paths handed to the student
PROJECT_DIR = "/home/user/project"
SAMPLE_FILES = {
    "/home/user/project/file1.txt": 0o644,
    "/home/user/project/secret.txt": 0o600,
}


def _mode_as_octal(path: str) -> int:
    """
    Return the permission bits of `path` as an int in octal form
    suitable for comparison (e.g., 0o644).  Follows symlinks (default
    stat() behavior) which is fine here because the spec makes no
    mention of symlinks.
    """
    st_mode = os.stat(path).st_mode
    return stat.S_IMODE(st_mode)


def test_project_directory_exists():
    assert os.path.isdir(
        PROJECT_DIR
    ), f"Required directory {PROJECT_DIR!r} is missing or not a directory."


@pytest.mark.parametrize("filepath, expected_mode", SAMPLE_FILES.items())
def test_sample_files_exist_with_correct_permissions(filepath, expected_mode):
    assert os.path.isfile(
        filepath
    ), f"Required sample file {filepath!r} is missing or not a regular file."

    actual_mode = _mode_as_octal(filepath)
    # Using base-8 representation in the assertion message for clarity
    assert (
        actual_mode == expected_mode
    ), (
        f"File {filepath!r} has permissions {oct(actual_mode)} "
        f"but expected {oct(expected_mode)}."
    )