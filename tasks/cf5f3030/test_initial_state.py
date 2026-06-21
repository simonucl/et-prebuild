# test_initial_state.py
#
# This pytest suite confirms that the working environment is clean
# before the student starts the task.  Specifically, it ensures the
# required artefacts do NOT yet exist so the student must create them
# from scratch.

import os
import pytest

HOME_DIR = "/home/user"
SCRIPT_PATH = f"{HOME_DIR}/proposed_firewall_rules.sh"
CSV_PATH = f"{HOME_DIR}/firewall_rules.csv"


def test_home_directory_present():
    """
    The /home/user directory must exist; otherwise subsequent tasks
    cannot be completed.  We do NOT create it—its absence is a genuine
    infrastructure problem.
    """
    assert os.path.isdir(HOME_DIR), (
        f"Expected home directory at {HOME_DIR!r} to exist before the task begins."
    )


@pytest.mark.parametrize("path", [SCRIPT_PATH, CSV_PATH])
def test_required_files_absent_initially(path):
    """
    Before the student starts, the artefact files should *not* already
    exist.  Their presence would suggest the environment is dirty or a
    previous run leaked state.
    """
    assert not os.path.exists(path), (
        f"Found unexpected file or directory at {path!r}. "
        "The workspace must start clean so the student can create the artefacts."
    )