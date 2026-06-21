# test_initial_state.py
#
# Pytest suite that verifies the “blank-slate” starting point for the
# documentation–sync exercise.  These tests **must** all pass _before_ the
# student begins any work.  They intentionally fail once the student has
# created the required files/directories, thereby acting as a guard that the
# checker is evaluating the correct phase of the assignment.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user").expanduser().resolve(strict=False)

# Directories that must NOT exist yet
ABSENT_DIRS = [
    HOME / "docs_work",
    HOME / "remote_backup",
    HOME / "scripts",
    HOME / "sync_logs",
]

# Files that must NOT exist yet
ABSENT_FILES = [
    HOME / "docs_work" / "introduction.md",
    HOME / "docs_work" / "user_guide.md",
    HOME / "docs_work" / "images" / "logo.png",
    HOME / "scripts" / "sync_docs.sh",
    HOME / "sync_logs" / "sync_status.log",
]


def test_home_directory_exists_and_is_emptyish():
    """
    The only guaranteed location is /home/user itself.  We assert that it exists
    and is a directory.  We do NOT enforce complete emptiness because Linux
    containers might come with dotfiles (.bashrc, .profile), but we *do* check
    that none of the exercise-specific items are present.
    """
    assert HOME.is_dir(), f"Expected {HOME} to exist as a directory."

    # Make sure none of the specific paths already live inside /home/user
    collision = [p for p in ABSENT_DIRS + ABSENT_FILES if p.exists()]
    assert (
        not collision
    ), (
        "The following paths already exist, but the initial state should be "
        f"clean:\n  " + "\n  ".join(map(str, collision))
    )


@pytest.mark.parametrize("path", ABSENT_DIRS, ids=lambda p: str(p))
def test_expected_directories_absent(path: Path):
    """
    Verify that the exercise-related directories have NOT been created yet.
    """
    assert (
        not path.exists()
    ), f"Directory {path} should NOT exist at the start of the task."


@pytest.mark.parametrize("path", ABSENT_FILES, ids=lambda p: str(p))
def test_expected_files_absent(path: Path):
    """
    Verify that the specific files enumerated in the specification do NOT
    pre-exist.  Their presence would mean the student’s workspace is not in the
    required pristine state.
    """
    assert (
        not path.exists()
    ), f"File {path} should NOT exist at the start of the task."