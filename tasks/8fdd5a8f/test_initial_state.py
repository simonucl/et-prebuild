# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating system
# before the student performs any actions for the “MLOps DNS audit” exercise.
#
# Ground truth:
#   • The user’s home directory (/home/user) already exists.
#   • No part of the desired /home/user/mlops tree is present yet.
#
# The checks below make sure these assumptions hold.
# If any assertion fails, the machine is in an unexpected state and the
# exercise cannot reliably proceed.

import os
import pytest

HOME_DIR = "/home/user"
MLOPS_DIR = os.path.join(HOME_DIR, "mlops")

def test_home_directory_exists():
    """
    The baseline /home/user directory must be present; otherwise the
    exercise instructions cannot be followed.
    """
    assert os.path.isdir(HOME_DIR), (
        f"Expected the home directory {HOME_DIR!r} to exist, but it does not."
    )

def test_mlops_directory_absent():
    """
    The /home/user/mlops directory (and anything underneath it) must *not*
    exist before the student starts.  Its presence would indicate that the
    machine is in a dirty state from an earlier run.
    """
    assert not os.path.exists(MLOPS_DIR), (
        f"The directory {MLOPS_DIR!r} should NOT exist before the exercise "
        "begins, but it is already present."
    )