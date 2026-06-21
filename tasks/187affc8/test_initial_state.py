# test_initial_state.py
#
# This test-suite verifies the *initial* state of the filesystem,
# i.e. *before* the student starts working on the task.
#
# What we assert:
#   • /home/user/cfgmgr must NOT yet contain the three required artefacts
#     (or even exist at all).  The student will create them during the task.
#
# If any of the files already exist, the tests will fail with an
# explanatory message so that the student knows the starting point is wrong.

import os
from pathlib import Path

import pytest

# Canonical paths that must **not** be present yet.
CFG_DIR = Path("/home/user/cfgmgr")
BEFORE_FILE = CFG_DIR / "installed_packages_before.txt"
AFTER_FILE = CFG_DIR / "installed_packages_after.txt"
PATCH_FILE = CFG_DIR / "jq_install_diff.patch"


@pytest.mark.parametrize(
    "path",
    [BEFORE_FILE, AFTER_FILE, PATCH_FILE],
    ids=["before.txt", "after.txt", "diff.patch"],
)
def test_required_files_do_not_exist(path: Path):
    """
    None of the target artefacts should be present before the student
    performs any action.
    """
    assert not path.exists(), (
        f"Initial-state violation: {path} already exists. "
        "Please remove it so the exercise starts from a clean slate."
    )


def test_cfg_directory_empty_or_absent():
    """
    The directory /home/user/cfgmgr should either not exist at all,
    or, if it does exist for some reason, it must NOT already contain
    any of the three files the student will create.
    """
    if not CFG_DIR.exists():
        # Ideal case: directory is completely absent.
        return

    assert CFG_DIR.is_dir(), f"{CFG_DIR} exists but is not a directory."

    # Collect any of the target artefacts that are already present.
    offending = [p.name for p in (BEFORE_FILE, AFTER_FILE, PATCH_FILE) if p.exists()]
    assert not offending, (
        "Initial-state violation: the following files are already present in "
        f"{CFG_DIR}: {', '.join(offending)}.  They must be removed so the "
        "assignment can start from a clean state."
    )