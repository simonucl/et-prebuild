# test_initial_state.py
#
# This test-suite validates that the operating-system / filesystem is in the
# expected INITIAL state *before* the learner carries out the exercise.
#
# The learner’s task is to create          /home/user/sec_audit_env
# and several artefacts beneath it.  Therefore none of these resources
# should exist at the outset.  If they DO exist, we raise an assertion
# explaining exactly what is wrong so the learner (or the lab
# provisioning scripts) can rectify the environment before the real tests
# run.

import os
import stat
import pytest
from pathlib import Path


# Constant paths used throughout the suite
HOME_DIR = Path("/home/user")
VENV_DIR = HOME_DIR / "sec_audit_env"
AUDIT_LOG = VENV_DIR / "permission_audit.log"


@pytest.mark.parametrize("path", [HOME_DIR])
def test_home_directory_exists_and_is_directory(path):
    """
    Sanity-check: /home/user must already exist and be a directory so that the
    learner has a place to create the virtual-environment.  We do NOT check
    permissions on the home directory here; only that it exists and is the
    correct type.
    """
    assert path.exists(), (
        f"Expected base directory {path!s} to exist, but it does not.  "
        "Please create it before running the exercise."
    )
    assert path.is_dir(), (
        f"Expected {path!s} to be a directory, but found something else "
        f"(type: {path.stat().st_mode:o})."
    )


def test_sec_audit_env_does_not_exist():
    """
    The target virtual-environment directory *must not* exist yet.  The learner
    will create it as part of the exercise.  We fail early if it already exists
    so the workspace can be cleaned, ensuring a fair testing environment.
    """
    assert not VENV_DIR.exists(), (
        f"The directory {VENV_DIR!s} already exists, but the exercise expects "
        "to create it from scratch.  Please remove or rename it before "
        "continuing."
    )


def test_permission_audit_log_absent():
    """
    Likewise, the compliance log should not pre-exist.  Its presence would
    indicate that someone has already attempted (successfully or not) the
    exercise, which would invalidate the starting conditions.
    """
    assert not AUDIT_LOG.exists(), (
        f"The audit log {AUDIT_LOG!s} is present before the exercise starts.  "
        "Remove it so the learner can generate it afresh."
    )


def test_no_stale_venv_artifacts_inside_target_path():
    """
    Defensive check: even if /home/user/sec_audit_env does NOT exist as a
    *directory*, we make sure that no file, symlink, socket, etc. exists at
    that path.  Anything other than “absent” would interfere with the commands
    the learner is expected to run (e.g. `python -m venv ...`).
    """
    if VENV_DIR.exists():
        pytest.skip(
            "Path exists – handled in previous test; skipping stale artefact check."
        )
    else:
        # Path is expected not to exist at all – stat() should fail.
        with pytest.raises(FileNotFoundError):
            os.stat(VENV_DIR)