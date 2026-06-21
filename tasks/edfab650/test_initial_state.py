# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student runs any command.  It intentionally ignores all
# “output” artifacts that the student is expected to create (e.g. the archive
# file and the log line).  If any of the assertions in this file fail, the
# environment is not prepared the way the task description promises.

import os
import stat
import pytest

HOME = "/home/user"
IMPORTANT_DIR = os.path.join(HOME, "important_data")
SECURE_BACKUPS_DIR = os.path.join(HOME, "secure_backups")

FILE_1 = "file1.txt"
FILE_2 = "file2.txt"

FILE_1_CONTENT = "Alpha\n"
FILE_2_CONTENT = "Beta\n"


def _is_regular_file(path):
    """Return True if path exists and is a regular file (not dir, link, etc.)."""
    return os.path.isfile(path) and stat.S_ISREG(os.stat(path).st_mode)


def test_important_data_directory_exists():
    """/home/user/important_data must exist and be a directory."""
    assert os.path.isdir(IMPORTANT_DIR), (
        f"Expected directory {IMPORTANT_DIR!r} to exist, "
        "but it is missing or not a directory."
    )


def test_important_data_contains_exact_files():
    """
    /home/user/important_data is expected to contain exactly the two files:
    file1.txt and file2.txt – no more, no less.
    """
    expected = {FILE_1, FILE_2}
    try:
        actual = set(os.listdir(IMPORTANT_DIR))
    except FileNotFoundError:
        pytest.skip(f"{IMPORTANT_DIR} does not exist; covered by previous test.")

    assert actual == expected, (
        f"{IMPORTANT_DIR} should contain exactly {sorted(expected)}, "
        f"but it contains {sorted(actual)}."
    )


@pytest.mark.parametrize(
    "filename, expected_content",
    [(FILE_1, FILE_1_CONTENT), (FILE_2, FILE_2_CONTENT)],
)
def test_file_contents(filename, expected_content):
    """
    Verify that file1.txt contains 'Alpha\\n' and file2.txt contains 'Beta\\n'.
    """
    path = os.path.join(IMPORTANT_DIR, filename)

    assert _is_regular_file(path), (
        f"Expected a regular file at {path!r}, but it is missing "
        "or not a regular file."
    )

    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()

    assert content == expected_content, (
        f"Content mismatch for {path!r}. "
        f"Expected {expected_content!r} but got {content!r}."
    )


def test_secure_backups_directory_exists_and_writable():
    """
    /home/user/secure_backups must exist, be a directory, and be writable by
    the current user so the student can place the archive and log there.
    """
    assert os.path.isdir(SECURE_BACKUPS_DIR), (
        f"Expected directory {SECURE_BACKUPS_DIR!r} to exist, "
        "but it is missing or not a directory."
    )

    assert os.access(SECURE_BACKUPS_DIR, os.W_OK), (
        f"Directory {SECURE_BACKUPS_DIR!r} is not writable by the current user."
    )