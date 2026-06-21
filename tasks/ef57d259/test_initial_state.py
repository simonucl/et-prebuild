# test_initial_state.py
"""
Pytest suite that verifies the machine is in the expected *pre-task* state.

The student task is to CREATE the following artefacts *after* this test passes:
    /home/user/deploy/                    (directory)
    /home/user/deploy/firewall_rules.sh  (executable shell script)
    /home/user/deploy/firewall_rules.log (plain text log, NOT executable)

This file purposely ensures none of those deliverables are present yet, so that
the subsequent “final-state” tests can meaningfully check the student’s work.
"""

import os
import stat
import pytest

HOME_DIR = "/home/user"
DEPLOY_DIR = os.path.join(HOME_DIR, "deploy")
FW_SCRIPT = os.path.join(DEPLOY_DIR, "firewall_rules.sh")
FW_LOG = os.path.join(DEPLOY_DIR, "firewall_rules.log")


def _is_executable(path: str) -> bool:
    """
    Return True if the *owner* execute bit is set on the given path.
    The test only concerns itself with the owner bit because the
    requirements mandate at least that much.
    """
    mode = os.stat(path).st_mode
    return bool(mode & stat.S_IXUSR)


def test_home_directory_exists():
    assert os.path.isdir(HOME_DIR), (
        f"Expected user home directory {HOME_DIR!r} to exist as a directory."
    )


def test_deploy_directory_absent_or_empty():
    """
    The /home/user/deploy directory may or may not exist at the start.
    If it already exists, it must *not* contain the files that the
    student is supposed to create later on.
    """
    if not os.path.exists(DEPLOY_DIR):
        # Perfectly acceptable: directory not yet created.
        return

    assert os.path.isdir(DEPLOY_DIR), (
        f"{DEPLOY_DIR!r} exists but is not a directory."
    )

    # Ensure the target files do not pre-exist.
    for unwanted in (FW_SCRIPT, FW_LOG):
        assert not os.path.exists(unwanted), (
            f"Found unexpected file {unwanted!r} — "
            "the student should be responsible for creating it."
        )


@pytest.mark.parametrize("path", [FW_SCRIPT, FW_LOG])
def test_firewall_files_absent(path):
    """
    Neither firewall_rules.sh nor firewall_rules.log should exist yet.
    """
    assert not os.path.exists(path), (
        f"File {path!r} already exists; it should be created by the student."
    )


def test_no_preexisting_executable_permissions():
    """
    If by any chance /home/user/deploy/firewall_rules.sh exists (for instance
    from a stale workspace), ensure it is *not* pre-marked as executable.
    This guards against accidentally handing the solution to the student.
    """
    if os.path.exists(FW_SCRIPT):
        assert not _is_executable(FW_SCRIPT), (
            f"{FW_SCRIPT!r} is unexpectedly executable — "
            "the student should set its permissions."
        )