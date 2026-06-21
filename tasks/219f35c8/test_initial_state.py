# test_initial_state.py
#
# This pytest suite validates the initial filesystem state *before*
# the student carries out the backup task.  It asserts that
#
# 1. /home/user/app exists and contains exactly the two expected files,
#    with the precise contents specified in the task description.
# 2. The backup destination (/home/user/backups) and any artefacts that
#    should be created by the student (archive + log file) do **not**
#    yet exist.
#
# Only Python’s stdlib and pytest are used.

import os
import stat
import pytest

# ---------------------------------------------------------------------------
# Expected constants
# ---------------------------------------------------------------------------

HOME = "/home/user"
APP_DIR = os.path.join(HOME, "app")
BACKUPS_DIR = os.path.join(HOME, "backups")
ARCHIVE_NAME = "app_backup_20231005_153000.tar.gz"
ARCHIVE_PATH = os.path.join(BACKUPS_DIR, ARCHIVE_NAME)
LOG_PATH = os.path.join(BACKUPS_DIR, "backup.log")

EXPECTED_FILES = {
    "index.html": "<html>Hello World</html>\n",
    "config.yaml": "port: 8080\n",
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_file(path):
    """Return the full *text* contents of a file."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Tests for /home/user/app
# ---------------------------------------------------------------------------

def test_app_directory_exists_and_is_directory():
    assert os.path.isdir(APP_DIR), (
        f"Required directory {APP_DIR} does not exist or is not a directory."
    )

def test_app_directory_contents_are_exact():
    # List only regular files (ignore potential rogue dotfiles/subdirs)
    present_files = sorted(
        f for f in os.listdir(APP_DIR)
        if stat.S_ISREG(os.stat(os.path.join(APP_DIR, f)).st_mode)
    )

    expected_files_sorted = sorted(EXPECTED_FILES.keys())
    assert present_files == expected_files_sorted, (
        f"{APP_DIR} should contain exactly the files "
        f"{expected_files_sorted}, but contains {present_files}."
    )

@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_app_files_have_exact_content(filename, expected_content):
    file_path = os.path.join(APP_DIR, filename)
    assert os.path.isfile(file_path), f"Expected file {file_path} is missing."
    actual_content = read_file(file_path)
    assert actual_content == expected_content, (
        f"Content mismatch in {file_path}.\n"
        f"Expected ({len(expected_content)} bytes):\n{expected_content!r}\n\n"
        f"Got ({len(actual_content)} bytes):\n{actual_content!r}"
    )

# ---------------------------------------------------------------------------
# Tests confirming that no backup artefacts pre-exist
# ---------------------------------------------------------------------------

def test_backups_directory_absent_initially():
    assert not os.path.exists(BACKUPS_DIR), (
        f"{BACKUPS_DIR} should NOT exist before the backup task starts."
    )

def test_backup_archive_absent_initially():
    assert not os.path.exists(ARCHIVE_PATH), (
        f"Backup archive {ARCHIVE_PATH} should NOT exist before the task starts."
    )

def test_backup_log_absent_initially():
    assert not os.path.exists(LOG_PATH), (
        f"Backup log {LOG_PATH} should NOT exist before the task starts."
    )