# test_initial_state.py
#
# This test-suite validates that the filesystem is in the **initial** state
# expected *before* the learner starts working on the backup task.
#
# It asserts:
#   • /home/user/backup_src exists and is a directory.
#   • /home/user/backup_src/file1.txt and file2.txt both exist, are regular
#     files, and contain exactly the expected text (including the trailing
#     newlines).
#   • The helper directories that the learner is supposed to create
#     (/home/user/backup_archive, /home/user/backup_restore, /home/user/backup_log)
#     do **NOT** yet exist.
#
# If any assertion fails, the error message explains exactly what is wrong
# so the environment can be fixed before the actual exercise begins.

import os
import stat
import pytest

HOME = "/home/user"
SRC_DIR = os.path.join(HOME, "backup_src")
ARCHIVE_DIR = os.path.join(HOME, "backup_archive")
RESTORE_DIR = os.path.join(HOME, "backup_restore")
LOG_DIR = os.path.join(HOME, "backup_log")

FILE1 = os.path.join(SRC_DIR, "file1.txt")
FILE2 = os.path.join(SRC_DIR, "file2.txt")

FILE1_CONTENT = "Report id: FQ1-2024\nTotal revenue: $1,000,000\n"
FILE2_CONTENT = "HR internal directory v2.3\nLast updated: 2024-05-12\n"


def _assert_readable_writable(path: str) -> None:
    """
    Helper that fails the test with a clear message if `path` is not readable
    and writable by the current (non-root) user.
    """
    if not os.access(path, os.R_OK):
        pytest.fail(f"'{path}' exists but is not readable by the user.")
    if not os.access(path, os.W_OK):
        pytest.fail(f"'{path}' exists but is not writable by the user.")


def test_backup_src_directory_exists_and_accessible():
    assert os.path.isdir(SRC_DIR), (
        f"Required source directory '{SRC_DIR}' is missing or not a directory."
    )
    _assert_readable_writable(SRC_DIR)


@pytest.mark.parametrize(
    "file_path, expected_content",
    [
        (FILE1, FILE1_CONTENT),
        (FILE2, FILE2_CONTENT),
    ],
)
def test_source_files_exist_and_have_expected_content(file_path, expected_content):
    # Existence & type
    assert os.path.isfile(
        file_path
    ), f"Source file '{file_path}' is missing or not a regular file."

    # Read / write permissions
    _assert_readable_writable(file_path)

    # Content
    with open(file_path, "r", encoding="utf-8") as fh:
        actual = fh.read()
    assert actual == expected_content, (
        f"Content of '{file_path}' does not match the expected initial text."
    )


@pytest.mark.parametrize(
    "path, description",
    [
        (ARCHIVE_DIR, "backup_archive directory"),
        (RESTORE_DIR, "backup_restore directory"),
        (LOG_DIR, "backup_log directory"),
        (os.path.join(ARCHIVE_DIR, "project_backup.tar.gz"), "target archive file"),
        (os.path.join(LOG_DIR, "integrity_check.log"), "integrity log file"),
    ],
)
def test_target_locations_do_not_yet_exist(path, description):
    assert not os.path.exists(
        path
    ), f"{description!s} ('{path}') already exists, but it should be absent before the task starts."