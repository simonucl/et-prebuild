# test_initial_state.py
#
# Pytest suite to validate the initial state of the environment
# *before* the student performs any action for the “Temporarily switch
# shell to UTC & C.UTF-8 and generate verification log” task.
#
# Rules verified:
#   • The log file /home/user/time_locale_check.log MUST NOT exist yet.
#     It will be created by the student solution.  If it exists already,
#     the initial state is invalid.

import os
import pytest

LOG_PATH = "/home/user/time_locale_check.log"


def test_log_file_does_not_exist():
    """
    The verification log must not be present before the student runs
    their commands.  Its existence would invalidate the starting
    conditions of the task.
    """
    assert not os.path.exists(
        LOG_PATH
    ), (
        f"The file {LOG_PATH} already exists. "
        "The initial environment should not contain this file; "
        "it must be created by your solution."
    )