# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state
# BEFORE the student performs any action for the backup task.
#
# These tests assert that:
#   1. /home/user/project   already exists and is a directory.
#   2. /home/user/project   contains at least one regular file
#      (sample.txt is expected but any file satisfies the “≥1 file” rule).
#   3. /home/user/backup    does NOT yet exist (neither file nor dir).
#   4. No target artefacts already exist inside /home/user/backup.
#
# A failure here means the starting environment is wrong and would give
# misleading results for the student’s later work.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
BACKUP_DIR = HOME / "backup"

@pytest.mark.describe("Pre-exercise filesystem sanity")
class TestInitialState:
    # 1. Project directory must already exist
    def test_project_directory_exists(self):
        assert PROJECT_DIR.exists(), (
            f"Required directory {PROJECT_DIR} is missing. "
            "The exercise must start with this directory present."
        )
        assert PROJECT_DIR.is_dir(), (
            f"{PROJECT_DIR} exists but is not a directory."
        )

    # 2. Project directory must contain at least one file
    def test_project_directory_contains_files(self):
        files = [p for p in PROJECT_DIR.iterdir() if p.is_file()]
        assert files, (
            f"{PROJECT_DIR} contains no regular files. "
            "There should be at least one file (e.g. sample.txt) "
            "to make the backup meaningful."
        )

    # 3. Backup directory must NOT yet exist
    def test_backup_directory_absent(self):
        assert not BACKUP_DIR.exists(), (
            f"{BACKUP_DIR} already exists, but the initial state should NOT "
            "have a backup directory. Remove it before starting the task."
        )

    # 4. Specific target artefacts must also be absent
    @pytest.mark.parametrize(
        "relative_path",
        [
            "project_backup.tar.gz",
            "project_backup.tar.gz.sha256",
            "backup_status.log",
        ],
    )
    def test_no_target_files_present(self, relative_path):
        target_path = BACKUP_DIR / relative_path
        assert not target_path.exists(), (
            f"Unexpected pre-existing file {target_path}. "
            "The environment must start clean so the student's script "
            "creates this file from scratch."
        )