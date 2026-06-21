# test_initial_state.py
#
# This test-suite verifies the *initial* state of the operating system
# before the student performs any action.  For this particular task
# we must ensure that the alert-rules file the student is expected to
# create does **not** yet exist.  The test fails loudly if the file is
# already present, as that would invalidate the exercise.

import os
import pathlib

ALERT_RULES_PATH = pathlib.Path("/home/user/monitoring/alert.rules")


def test_alert_rules_file_does_not_exist():
    """
    PRE-CONDITION:
        The rules file must not exist yet.  The student’s solution is
        to create it with the required single alert line.

    EXPECTED:
        ‑ /home/user/monitoring/alert.rules does **not** exist as either
          a regular file, symlink, or directory.

    FAILURE MESSAGE:
        Clearly states that the file is unexpectedly present.
    """
    assert not ALERT_RULES_PATH.exists(), (
        f"Pre-condition failed: '{ALERT_RULES_PATH}' already exists. "
        "The student is expected to create this file as part of the task, "
        "but it is present before any action has been taken."
    )