# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating‐system
# before the student performs any action for the “observability env settings”
# exercise.  Nothing related to the final expected artefacts must exist yet.
#
# If any of the following assertions fails it means the environment has
# already been modified (or is unexpectedly populated) and is therefore
# unsuitable as a clean starting point for the student.

import os
import stat
import pytest
from pathlib import Path

# Absolute paths that must NOT exist at the beginning of the exercise
MONITORING_DIR = Path("/home/user/monitoring")
CONF_DIR       = MONITORING_DIR / "conf"
LOGS_DIR       = MONITORING_DIR / "logs"
ENV_SH         = CONF_DIR / "env.sh"
ENV_LOG        = LOGS_DIR / "env_check.log"


@pytest.mark.parametrize(
    "path",
    [
        MONITORING_DIR,
        CONF_DIR,
        LOGS_DIR,
        ENV_SH,
        ENV_LOG,
    ],
)
def test_paths_do_not_exist(path):
    """
    Ensure that none of the directories or files expected in the *final*
    solution are present prior to the student's work.
    """
    assert not path.exists(), (
        f"Path '{path}' should NOT exist yet. "
        "The environment must start in a clean state so the student can "
        "create it as part of the task."
    )


def test_no_partial_hierarchy():
    """
    A common corner-case is that /home/user/monitoring exists while the deeper
    hierarchy does not. We make sure nothing under /home/user/monitoring exists
    at all.  This guards against stale artefacts from previous runs.
    """
    if MONITORING_DIR.exists():
        # Something is wrong: the top-level directory exists.  Gather a quick
        # inventory to help the student understand what needs to be cleaned.
        offending_paths = []
        for root, dirs, files in os.walk(MONITORING_DIR):
            for name in dirs + files:
                offending_paths.append(os.path.join(root, name))
        offending_list = "\n".join(offending_paths) or "(empty directory)"
        pytest.fail(
            f"Directory '{MONITORING_DIR}' already exists but should not. "
            f"Contents found:\n{offending_list}"
        )