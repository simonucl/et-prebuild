# test_initial_state.py
#
# This pytest suite verifies the **initial** operating-system state
# before the student attempts the exercise.  In particular, it confirms
# that the target output file does **not** yet exist, while the expected
# parent directory hierarchy is present and usable.
#
# The exercise will later require the student to create exactly one file:
#   /home/user/timezone_conversion.log
#
# To avoid false positives (i.e., when the assessment environment already
# contains the answer file), we explicitly assert that the file is absent.
# Any failure here instructs the learner or the testing platform to clean
# the environment before grading the final submission.

import os
from pathlib import Path

HOME_DIR = Path("/home/user")
TARGET_FILE = HOME_DIR / "timezone_conversion.log"


def test_home_directory_exists():
    """
    The base directory /home/user must exist so that the learner can
    create the required file inside it.  If this directory is missing,
    the entire exercise setup is invalid.
    """
    assert HOME_DIR.exists(), (
        "The directory '/home/user' does not exist. "
        "It must be present before the exercise begins."
    )
    assert HOME_DIR.is_dir(), (
        f"'{HOME_DIR}' exists but is not a directory. "
        "A directory is required at this path."
    )


def test_target_file_absent_initially():
    """
    The answer file must NOT exist at the start of the exercise.
    Its presence would indicate that the environment already contains
    the solution or residual data from a previous run.
    """
    assert not TARGET_FILE.exists(), (
        f"The file '{TARGET_FILE}' already exists, but it should "
        "NOT be present before the student runs their solution. "
        "Please remove it to ensure a clean initial state."
    )