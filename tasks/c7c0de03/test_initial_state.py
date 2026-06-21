# test_initial_state.py
#
# Pytest suite that validates the “pre-ETL backup” starting state
# before the student runs any commands.
#
# Truths we validate:
#   1. /home/user/etl_workspace/incoming/  exists with the required files.
#   2. /home/user/etl_workspace/backups/   does NOT exist yet.
#   3. No pre-existing /home/user/etl_workspace/backups/incoming_backup.tar.gz
#      should be on disk.

from pathlib import Path
import pytest

HOME = Path("/home/user")
WS   = HOME / "etl_workspace"
INCOMING_DIR = WS / "incoming"
BACKUPS_DIR  = WS / "backups"
ARCHIVE_PATH = BACKUPS_DIR / "incoming_backup.tar.gz"


@pytest.fixture(scope="module")
def incoming_expected_paths():
    """
    Return a list of the *exact* paths that must already exist
    inside /home/user/etl_workspace/incoming/.
    """
    return [
        INCOMING_DIR / "january.csv",
        INCOMING_DIR / "february.csv",
        INCOMING_DIR / "readme.txt",
        INCOMING_DIR / "extras",
        INCOMING_DIR / "extras" / "notes.csv",
    ]


def test_incoming_directory_exists():
    assert INCOMING_DIR.exists(), (
        f"Expected directory {INCOMING_DIR} to exist, "
        "but it is missing."
    )
    assert INCOMING_DIR.is_dir(), (
        f"{INCOMING_DIR} exists but is not a directory."
    )


def test_incoming_required_files_present(incoming_expected_paths):
    # Verify each required file/directory exists and has the correct type.
    for path in incoming_expected_paths:
        assert path.exists(), f"Required path {path} is missing."
        if path.suffix:  # Path has a file extension -> should be a file
            assert path.is_file(), f"{path} should be a file."
        else:            # No extension -> we expect a directory
            assert path.is_dir(), f"{path} should be a directory."


def test_backups_directory_absent():
    # The backup directory should *not* exist yet.
    assert not BACKUPS_DIR.exists(), (
        f"Directory {BACKUPS_DIR} should not exist before the task is run. "
        "Create it as part of the single shell command."
    )


def test_archive_absent():
    # The target archive must not pre-exist.
    assert not ARCHIVE_PATH.exists(), (
        f"Archive {ARCHIVE_PATH} already exists — the student is expected "
        "to create it during the task."
    )