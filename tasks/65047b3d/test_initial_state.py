# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system state
# before the student begins the exercise described in the task
# instructions.  According to the specification, the directory
# /home/user/exp1 and anything beneath it must *not* exist yet.
#
# Only Python’s stdlib and pytest are used.

from pathlib import Path

EXP1_ROOT = Path("/home/user/exp1")


def test_exp1_directory_absent_initially():
    """
    The exercise starts with a completely clean slate: the directory
    /home/user/exp1 must be absent.  If the directory (or any of its
    would-be children) already exists, the student would be starting
    from an incorrect initial state, and downstream instructions or
    automated grading could behave unpredictably.
    """
    assert not EXP1_ROOT.exists(), (
        f"Pre-exercise invariant violated: {EXP1_ROOT} already exists.\n"
        "Remove this directory (and anything below it) before proceeding."
    )