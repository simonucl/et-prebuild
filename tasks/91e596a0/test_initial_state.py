# test_initial_state.py
#
# This test-suite verifies that the workspace is completely clean *before*
# the student starts working on the “sandbox” assignment.  Every file and
# directory that the final grader will later look for **must be absent** at
# this point.  If any of them already exist, the initial-state check will
# fail and tell the student what needs to be removed/reset.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user").expanduser().resolve()

# Sanity-check: we assume the /home/user directory itself is present.
def test_home_exists():
    assert HOME.is_dir(), f"Expected base directory {HOME} to exist."


# All paths that MUST NOT exist yet (they will be created by the student).
MUST_BE_ABSENT = [
    HOME / "webapp",
    HOME / "webapp/public",
    HOME / "webapp/config",
    HOME / "webapp/config/settings.json",
    HOME / "webapp/scripts",
    HOME / "webapp/scripts/backup.sh",
    HOME / "permission_report.txt",
]

@pytest.mark.parametrize("path", MUST_BE_ABSENT)
def test_path_is_absent(path: Path):
    assert not path.exists(), (
        f"{path} already exists, but the workspace should start completely empty. "
        "Please remove this item before running the actual assignment steps."
    )