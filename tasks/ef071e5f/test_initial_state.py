# test_initial_state.py
#
# This pytest file validates the *initial* state of the operating system before
# the student attempts the task described in the prompt.  According to the
# specification, the file /home/user/.bashrc might not exist; if it does exist,
# it must *not* yet contain the exact line
#
#     export CAPACITY_MODE="planner"
#
# anywhere in the file.  These tests assert precisely that condition so that
# the automated grader (or a human reviewer) can be confident the environment
# starts in the expected state.

import os
import pytest

BASHRC_PATH = "/home/user/.bashrc"
TARGET_LINE = 'export CAPACITY_MODE="planner"'


def _file_lines(path):
    """
    Utility helper that returns the list of lines (without trailing newlines)
    for the given file, using UTF-8 with fallback error handling.
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        return fh.read().splitlines()


@pytest.mark.it("Ensure /home/user/.bashrc is absent or lacks the target line")
def test_bashrc_initial_state():
    """
    Initial-state expectations:

    1. /home/user/.bashrc may not exist at all.  In that case we pass.
    2. If /home/user/.bashrc *does* exist, it must NOT contain the exact line
       'export CAPACITY_MODE="planner"' anywhere within it.

    Any deviation means the starting environment is incorrect.
    """
    if not os.path.exists(BASHRC_PATH):
        # File is absent → acceptable initial state.
        return

    # File exists — inspect its contents.
    lines = _file_lines(BASHRC_PATH)

    assert TARGET_LINE not in lines, (
        f"Initial state violation: {BASHRC_PATH!r} already contains the line "
        f"{TARGET_LINE!r}.  It should not be present before the task begins."
    )