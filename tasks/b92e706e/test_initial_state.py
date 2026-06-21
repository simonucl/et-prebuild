# test_initial_state.py
#
# This pytest suite validates that the operating-system state is **clean**
# before the student starts the task.  Nothing that the student is supposed
# to create (directories, permissions, audit log) should exist yet.

import os
import stat
import pytest

# Absolute paths that **must not exist** before the student runs any commands.
CONFIDENTIAL_DIR = "/home/user/policy_demo/confidential"
PUBLIC_DIR       = "/home/user/policy_demo/public"
AUDIT_LOG        = "/home/user/policy_demo/permission_audit.log"

@pytest.mark.parametrize(
    "path,expected_type",
    [
        (CONFIDENTIAL_DIR, "directory"),
        (PUBLIC_DIR, "directory"),
        (AUDIT_LOG, "file"),
    ],
)
def test_paths_do_not_exist_yet(path: str, expected_type: str):
    """
    Ensure the directories and audit log required by the task
    are not present before the student performs any action.

    If any of these paths already exist, the test fails with a
    clear, actionable message.
    """
    assert not os.path.exists(path), (
        f"Pre-existing {expected_type} found at '{path}'.\n"
        "The filesystem must start in a clean state so the student's "
        "commands demonstrate creation and permission setting from scratch."
    )


def test_no_partial_parent_directory():
    """
    The parent directory '/home/user/policy_demo' may or may not exist
    prior to the task.  If it *does* exist, it must be empty so that the
    student can create only the required items inside it.

    We allow the directory to be absent (clean slate) or present but empty.
    """
    parent = "/home/user/policy_demo"
    if not os.path.exists(parent):
        # Totally absent is acceptable and even expected on a fresh system.
        return

    # Parent exists—ensure it is actually a directory.
    st = os.stat(parent)
    assert stat.S_ISDIR(st.st_mode), (
        f"'{parent}' exists but is not a directory."
    )

    # Directory should be empty at this stage.
    contents = os.listdir(parent)
    assert contents == [] or contents == ["." or ".."], (
        f"'{parent}' is expected to be empty before the task starts, "
        f"but it already contains: {contents}"
    )