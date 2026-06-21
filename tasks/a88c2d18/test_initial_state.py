# test_initial_state.py
#
# This pytest file verifies that the machine is in a **clean** state
# before the student carries out the “perf_lab” setup steps.
#
# Expected “clean slate”:
#   • The directory  /home/user/perf_lab            must NOT exist.
#   • The file       /home/user/perf_lab/run_profile.sh  must NOT exist.
#   • The file       /home/user/perf_lab/setup.log       must NOT exist.
#
# If any of the above items are already present, the tests will fail with
# a clear, actionable message so the learner can remove them and start
# the exercise from a known baseline.

import os
import pytest

PERF_LAB_DIR = "/home/user/perf_lab"
PROFILE_SCRIPT = os.path.join(PERF_LAB_DIR, "run_profile.sh")
SETUP_LOG = os.path.join(PERF_LAB_DIR, "setup.log")


@pytest.mark.order(1)
def test_perflab_directory_absent():
    """
    The perf_lab directory must NOT exist before the exercise starts.
    """
    assert not os.path.exists(PERF_LAB_DIR), (
        f"The directory {PERF_LAB_DIR!r} already exists. "
        "Please remove/rename it before starting the task."
    )


@pytest.mark.order(2)
def test_run_profile_script_absent():
    """
    The helper script should not be present yet.
    """
    assert not os.path.exists(PROFILE_SCRIPT), (
        f"The file {PROFILE_SCRIPT!r} already exists. "
        "Start with a clean state by removing it."
    )


@pytest.mark.order(3)
def test_setup_log_absent():
    """
    The setup.log must not pre-exist.
    """
    assert not os.path.exists(SETUP_LOG), (
        f"The file {SETUP_LOG!r} already exists. "
        "Remove it so the exercise can generate a fresh log."
    )