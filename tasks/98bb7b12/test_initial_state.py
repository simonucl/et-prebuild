# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem is
# in the expected “clean” state *before* the student performs any action
# for the “PostgreSQL backup settings” exercise.
#
# Expected initial state (truth):
#   1. The directory  /home/user/db_backup       MUST NOT exist.
#   2. The file       /home/user/db_backup/.env  MUST NOT exist.
#
# These tests fail with clear, instructive messages if the initial state
# has already been modified (e.g., the directory or file was pre-created),
# ensuring the learner starts from a known baseline.
#
# Only Python stdlib and pytest are used.

import os
import pytest

DB_BACKUP_DIR = "/home/user/db_backup"
ENV_FILE_PATH = "/home/user/db_backup/.env"


def _path_readable_state(path: str) -> str:
    """
    Helper: returns a string describing the current state of `path`
    to aid in assertion failure messages.
    """
    if os.path.islink(path):
        return "a symlink"
    if os.path.isdir(path):
        return "a directory"
    if os.path.isfile(path):
        return "a file"
    if os.path.exists(path):
        return "something (unknown type)"
    return "non-existent"


def _assert_path_absent(path: str):
    """
    Assert that `path` does not exist in any form (file, dir, symlink, etc.).
    Provide a rich assertion message if the path is present.
    """
    assert not os.path.exists(path), (
        f"Precondition failed: {path} should NOT exist in the initial state, "
        f"but it is currently {_path_readable_state(path)}. "
        "Remove it before running the learner's solution."
    )


@pytest.mark.describe("Initial OS/FS state for PostgreSQL backup settings exercise")
class TestInitialState:
    def test_db_backup_directory_absent(self):
        """
        The directory /home/user/db_backup must NOT exist before the student runs
        their solution; they are responsible for creating it.
        """
        _assert_path_absent(DB_BACKUP_DIR)

    def test_env_file_absent(self):
        """
        The file /home/user/db_backup/.env must NOT exist before the student runs
        their solution; they are responsible for creating it with exact content.
        """
        _assert_path_absent(ENV_FILE_PATH)