# test_initial_state.py
#
# This pytest suite verifies that the system starts in a *clean* state
# before the student begins working on the “parallel backup utility”.
# None of the task-related directories / files / logs / archives should
# exist yet.  If any of them are already present, that would indicate
# that the environment is *not* pristine and the subsequent grading
# could yield false results.
#
# NOTE:  The tests purposely **fail** when they *do* find any of the
#        paths that will be produced by a correct solution.  This is
#        intentional: at this moment in time the student has not run
#        anything, therefore those artefacts must be absent.

from pathlib import Path
import pytest

HOME = Path("/home/user")

# All directories that a correct solution will eventually create.
DIRS_SHOULD_NOT_EXIST = [
    HOME / "projects",
    HOME / "projects" / "data1",
    HOME / "projects" / "data2",
    HOME / "bin",
    HOME / "archives",
]

# All files that a correct solution will eventually create.
FILES_SHOULD_NOT_EXIST = [
    HOME / "projects" / "data1" / "alpha.txt",
    HOME / "projects" / "data1" / "beta.txt",
    HOME / "projects" / "data2" / "gamma.txt",
    HOME / "projects" / "data2" / "delta.txt",
    HOME / "bin"      / "parallel_backup.sh",
    HOME / "archives" / "data1_20230101T120000Z.tar.gz",
    HOME / "archives" / "data2_20230101T120000Z.tar.gz",
    HOME / "archives" / "backup_20230101T120000Z.log",
]


def test_home_directory_present():
    """Sanity-check that /home/user exists and is a directory."""
    assert HOME.is_dir(), "/home/user must exist and be a directory for the exercise."


@pytest.mark.parametrize("path", DIRS_SHOULD_NOT_EXIST)
def test_directories_absent_initially(path: Path):
    """No target directories should exist before the student starts."""
    assert not path.exists(), (
        f"Unexpected directory found before start: {path}\n"
        "The workspace must be pristine; nothing from the task should exist yet."
    )


@pytest.mark.parametrize("path", FILES_SHOULD_NOT_EXIST)
def test_files_absent_initially(path: Path):
    """No target files or archives should exist before the student starts."""
    assert not path.exists(), (
        f"Unexpected file found before start: {path}\n"
        "The workspace must be pristine; nothing from the task should exist yet."
    )