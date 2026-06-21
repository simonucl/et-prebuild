# test_initial_state.py
#
# This pytest suite validates that the operating‐system / filesystem
# starts in a clean state, i.e.  *before* the student performs any of the
# required backup-operator steps described in the assignment.
#
# The checks below make sure that none of the directories, files or
# archives that the student is supposed to create are present yet.
#
# If any of them already exist, the test suite fails with a clear
# message so that both the student and the automated grader know that
# the initial environment is not in the expected pristine state.

import os
from pathlib import Path

HOME = Path("/home/user").expanduser()

# ---------------------------------------------------------------------------
# Basic sanity check: the home directory of user “user” must exist.
# ---------------------------------------------------------------------------

def test_user_home_exists():
    assert HOME.is_dir(), (
        f"Expected the home directory {HOME} to exist. "
        "Without it the assignment cannot be completed."
    )

# ---------------------------------------------------------------------------
# The resources that must *NOT* exist yet.
# ---------------------------------------------------------------------------

DIRECTORIES_THAT_SHOULD_NOT_EXIST = [
    HOME / "workspace" / "secure_data",
    HOME / "workspace" / "backups",
    HOME / "workspace" / "restore_test",
]

FILES_THAT_SHOULD_NOT_EXIST = [
    HOME / "workspace" / "secure_data" / "file1.txt",
    HOME / "workspace" / "secure_data" / "file2.txt",
    HOME / "workspace" / "backups" / "secure_data_backup_20230115.tar.gz",
    HOME / "workspace" / "restore_test" / "file1.txt",
    HOME / "workspace" / "restore_test" / "file2.txt",
    HOME / "backup_restore.log",
]

# ---------------------------------------------------------------------------
# Parametrised tests for non-existence.
# ---------------------------------------------------------------------------

import pytest

@pytest.mark.parametrize("path", [*DIRECTORIES_THAT_SHOULD_NOT_EXIST])
def test_directories_do_not_exist_yet(path: Path):
    assert not path.exists(), (
        f"The directory {path} already exists, but it should NOT be present "
        "before the student carries out the assignment steps. "
        "Start with a clean workspace."
    )

@pytest.mark.parametrize("path", [*FILES_THAT_SHOULD_NOT_EXIST])
def test_files_do_not_exist_yet(path: Path):
    assert not path.exists(), (
        f"The file {path} already exists, but it should NOT be present "
        "before the student carries out the assignment steps. "
        "Start with a clean workspace."
    )