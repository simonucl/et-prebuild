# test_initial_state.py
#
# This test-suite validates the **initial** filesystem layout
# that must be present before the student executes any solution.
# It intentionally makes **no reference** to the artefacts the
# student is expected to create (e.g. backup_tmp directory or
# tmp_backup.log).  If one of these tests fails it means the
# sandbox does not match the specification given in the task
# description and the evaluation/solution run should be aborted.

from pathlib import Path
import pytest

HOME = Path("/home/user")

# ---------------------------------------------------------------------------
# Directories that must already exist
# ---------------------------------------------------------------------------
EXPECTED_DIRS = [
    HOME / "my_project",
    HOME / "my_project" / "src",
    HOME / "my_project" / "test",
    HOME / "my_project" / "notes",
    HOME / "my_project" / "notes" / "tmp",
]

# ---------------------------------------------------------------------------
# Files that must already exist
# ---------------------------------------------------------------------------
EXPECTED_FILES = [
    HOME / "my_project" / "src" / "old.tmp",
    HOME / "my_project" / "src" / "main.c",
    HOME / "my_project" / "test" / "data.tmp",
    HOME / "my_project" / "debug.log",
    HOME / "my_project" / "notes" / "tmp" / "info.tmp",
]


@pytest.mark.parametrize("path", EXPECTED_DIRS)
def test_expected_directories_exist(path: Path):
    assert path.is_dir(), (
        f"Required directory missing: {path}\n"
        "The sandbox must contain all directories specified in the task "
        "description before the student command is run."
    )


@pytest.mark.parametrize("path", EXPECTED_FILES)
def test_expected_files_exist(path: Path):
    assert path.is_file(), (
        f"Required file missing: {path}\n"
        "All files listed in the initial state must be present before "
        "the student command is executed."
    )