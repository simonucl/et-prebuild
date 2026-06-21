# test_initial_state.py
#
# This test-suite validates that the operating-system / file-system is
# still in a **clean initial state** *before* the student starts working
# on the “project-local time-zone and locale” task.  Nothing that the
# student is expected to create should exist yet.
#
# If any of these tests fail it means the environment is **not** clean
# and the grader will be unable to determine whether the student’s work
# is correct.  Each failure message pin-points exactly what is already
# present and therefore must be removed (or the VM must be reset) before
# the student begins.
#
# NOTE:  We only use the Python standard library and pytest.

import os
import stat
import pytest

HOME = "/home/user"
DEV_ROOT = os.path.join(HOME, "dev_project")

# Directories that **must not** exist yet
DIRS_SHOULD_BE_ABSENT = [
    DEV_ROOT,
    os.path.join(DEV_ROOT, "config"),
    os.path.join(DEV_ROOT, "scripts"),
    os.path.join(DEV_ROOT, "logs"),
]

# Files that **must not** exist yet
FILES_SHOULD_BE_ABSENT = [
    os.path.join(DEV_ROOT, "config", "timezone.conf"),
    os.path.join(DEV_ROOT, "config", "locale.conf"),
    os.path.join(DEV_ROOT, "scripts", "apply_env.sh"),
    os.path.join(DEV_ROOT, "logs", "env_validation.log"),
]


@pytest.mark.parametrize("path", DIRS_SHOULD_BE_ABSENT)
def test_directories_absent(path):
    """
    The required project directories must NOT exist before the student
    performs any action.
    """
    assert not os.path.exists(path), (
        f"Pre-existing directory “{path}” found.\n"
        "The environment must start clean.  Remove this directory or "
        "reset the VM before giving the task to the student."
    )


@pytest.mark.parametrize("path", FILES_SHOULD_BE_ABSENT)
def test_files_absent(path):
    """
    None of the files the student is supposed to create should exist yet.
    """
    assert not os.path.exists(path), (
        f"Pre-existing file “{path}” found.\n"
        "The environment must not contain any of the target files prior "
        "to the student’s work."
    )


def test_apply_env_sh_not_executable():
    """
    Even if an unexpected apply_env.sh file is present, it must *not*
    already be marked executable—otherwise the state is contaminated.
    """
    script_path = os.path.join(DEV_ROOT, "scripts", "apply_env.sh")
    if os.path.exists(script_path):
        mode = os.stat(script_path).st_mode
        is_exec = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
        assert not is_exec, (
            f"Unexpected executable script at “{script_path}”. "
            "The student must create this script themselves; remove it "
            "or reset the VM."
        )