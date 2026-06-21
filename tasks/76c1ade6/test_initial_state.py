# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the operating
# system / file-system **before** the student performs the task.
# According to the task description, the learner must create
#   /home/user/activities/analytics-pg_optimize_commands.log
# only *after* running the three required Docker commands.
#
# Therefore, at the outset *no such file should exist*.  If it is
# already present, it means the exercise has either been solved
# prematurely or the environment was not properly reset.

from pathlib import Path

LOG_PATH = Path("/home/user/activities/analytics-pg_optimize_commands.log")


def test_log_file_does_not_exist_yet():
    """
    The command-audit log must *not* exist before the student starts
    working on the exercise.  Its presence at this point would indicate
    that the environment is in an unexpected state.
    """
    assert not LOG_PATH.exists(), (
        f"\nThe log file {LOG_PATH} already exists.\n"
        "The exercise requires creating this file only *after* executing\n"
        "the three Docker commands.  Please reset/clean the environment\n"
        "so the learner can perform the task from a clean state."
    )