# test_initial_state.py
#
# This test-suite asserts that the operating-system / filesystem is still
# in its pristine “before the student starts” state.  NONE of the objects
# that will later be created by the finished Makefile project may exist
# at this point.  If any one of them already exists, we fail early and
# tell the learner to start from a clean slate.

from pathlib import Path
import pytest

# Base path for the forthcoming project
BASE_DIR = Path("/home/user/backup_demo")

# All filesystem objects that *must NOT* exist yet
MUST_BE_ABSENT = [
    BASE_DIR / "data" / "report1.txt",
    BASE_DIR / "data" / "report2.txt",
    BASE_DIR / "data" / "log.txt",
    BASE_DIR / "Makefile",
    BASE_DIR / "backup.log",
    BASE_DIR / "backups" / "data_backup.tar.gz",
]

@pytest.mark.parametrize("path", MUST_BE_ABSENT)
def test_pristine_state(path: Path):
    """
    Before any work is done, none of the target files or directories
    should exist.  If they do, the student is not starting from a
    clean environment and the automated checker will later mis-judge
    the submission.
    """
    assert not path.exists(), (
        f"Unexpected pre-existing object found:\n"
        f"  {path}\n"
        f"This file/directory must NOT be present before you start the task. "
        f"Begin from a clean state and create it only through your Makefile."
    )