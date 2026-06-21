# test_initial_state.py
"""
Pytest suite that verifies the *initial* operating-system / filesystem state
before the student starts working on the task.

It asserts that:
1. The LP model file `/home/user/storage_problem.lp` exists **and** contains the
   exact problem statement expected by the graders.
2. No solution log is present yet at
   `/home/user/storage_solution.log` (the student must create it).
3. The GLPK command-line solver `glpsol` is available in the system `PATH`.

Only the Python standard library and pytest are used.
"""

import os
import shutil
import pytest
from pathlib import Path

LP_PATH = Path("/home/user/storage_problem.lp")
SOLUTION_LOG_PATH = Path("/home/user/storage_solution.log")

# The canonical (expected) content of storage_problem.lp
EXPECTED_LP_LINES = [
    "Minimize",
    " obj: x1 + 2 x2 + 3 x3",
    "Subject To",
    " c1: x1 + x2 + x3 >= 10",
    "Bounds",
    " 0 <= x1 <= 4",
    " 0 <= x2 <= 5",
    " 0 <= x3 <= 7",
    "Generals",
    " x1 x2 x3",
    "End",
]


def _clean_lines(raw_lines):
    """
    Helper that:
    • strips the trailing newline from each line,
    • preserves leading spaces (they are significant here),
    • drops any blank lines that might trail the file.
    """
    return [ln.rstrip("\n") for ln in raw_lines if ln.rstrip("\n") != ""]


def test_lp_file_exists():
    """Confirm the LP model file is present before any work starts."""
    assert LP_PATH.is_file(), (
        f"The LP model file is missing:\n  Expected path: {LP_PATH}"
    )


def test_lp_file_contents_match_expected():
    """
    Verify that the LP file contains EXACTLY the expected problem lines
    (order and spacing included).
    """
    with LP_PATH.open(encoding="utf-8") as fp:
        actual_lines = _clean_lines(fp.readlines())

    assert actual_lines == EXPECTED_LP_LINES, (
        "The contents of /home/user/storage_problem.lp do not match the expected "
        "linear‐programming model.\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_LP_LINES)
    )


def test_no_solution_log_yet():
    """
    Before the student acts, the solution log should **not** exist.
    Its presence would imply the workspace is not in the pristine initial state.
    """
    assert not SOLUTION_LOG_PATH.exists(), (
        "Found /home/user/storage_solution.log, but this file should NOT exist "
        "before the student performs the task."
    )


def test_glpsol_available_in_path():
    """The GLPK solver `glpsol` must be discoverable via the system PATH."""
    glpsol_path = shutil.which("glpsol")
    assert glpsol_path is not None, (
        "The command-line solver `glpsol` was not found in the system PATH. "
        "It is required for the upcoming task."
    )