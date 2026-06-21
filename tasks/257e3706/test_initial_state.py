# test_initial_state.py
#
# This Pytest suite verifies that the starting environment is **clean**
# before the learner begins the exercise.  Nothing from the required
# deliverables should already exist.

import os
import stat
import pytest

DIR_PATH = "/home/user/security/firewall"
SCRIPT_PATH = os.path.join(DIR_PATH, "planned_rules_v1.sh")
LOG_PATH = os.path.join(DIR_PATH, "resource_capacity.log")


def _explain_perm(path: str) -> str:
    """Return a human-readable string of the file’s permission bits."""
    mode = os.stat(path).st_mode
    return oct(mode & 0o777)


def test_directory_not_preexisting():
    """
    The target directory should NOT exist yet.
    A pre-existing directory could hide already-completed work and
    invalidate the learning objective.
    """
    assert not os.path.exists(DIR_PATH), (
        f"The directory {DIR_PATH} already exists. "
        "The environment must start clean so that the learner can "
        "create it themselves."
    )


@pytest.mark.parametrize("path", [SCRIPT_PATH, LOG_PATH])
def test_no_deliverable_files_present(path):
    """
    Neither the firewall script nor the capacity-planning log may be
    present at the outset.
    """
    assert not os.path.exists(path), (
        f"The file {path} already exists in the starting environment. "
        "Please remove it so the learner can create it."
    )


def test_no_executable_leftovers():
    """
    There must be no executable file named planned_rules_v1.sh anywhere
    under /home/user prior to the task.  A wildcard search guards
    against misplaced artefacts from previous runs.
    """
    for root, _dirs, files in os.walk("/home/user"):
        for fname in files:
            if fname == "planned_rules_v1.sh":
                full = os.path.join(root, fname)
                mode = _explain_perm(full)
                pytest.fail(
                    f"Found an unexpected pre-existing executable "
                    f"({full} with mode {mode}). "
                    "Remove it so the learner starts from a clean slate."
                )