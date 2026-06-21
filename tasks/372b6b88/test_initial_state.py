# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state *before* the
# student has executed anything.  It ensures that the scaffold supplied to the
# learner is present and correct.
#
# What we assert:
#   1. /home/user/solver_demo exists and is a directory with mode 755.
#   2. /home/user/solver_demo/run_lp.py exists, is executable (mode 755),
#      and contains exactly the three expected print statements.
#   3. /home/user/solver_demo/lp_result.txt does NOT yet exist.
#   4. No extra files/directories are present inside /home/user/solver_demo.
#
# If any of these conditions are not met, the tests fail with a clear,
# actionable message.

import os
import stat
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #
HOME = Path("/home/user")
DEMO_DIR = HOME / "solver_demo"
SCRIPT_PATH = DEMO_DIR / "run_lp.py"
RESULT_PATH = DEMO_DIR / "lp_result.txt"

EXPECTED_DIR_MODE = 0o755
EXPECTED_SCRIPT_MODE = 0o755

EXPECTED_SCRIPT_LINES = [
    '#!/usr/bin/env python3\n',
    'print("objective=22.0")\n',
    'print("x=4.0")\n',
    'print("y=5.0")\n',
]


# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #
def _mode(path: Path) -> int:
    """Return the permission bits (e.g. 0o755) for the given path."""
    return stat.S_IMODE(path.stat().st_mode)


def _read_lines(path: Path) -> list:
    """Read all lines from *path*, preserving newline characters."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_solver_demo_directory_exists_and_is_correct():
    assert DEMO_DIR.exists(), f"Directory {DEMO_DIR} is missing."
    assert DEMO_DIR.is_dir(), f"{DEMO_DIR} exists but is not a directory."
    mode = _mode(DEMO_DIR)
    assert mode == EXPECTED_DIR_MODE, (
        f"{DEMO_DIR} should have permissions {oct(EXPECTED_DIR_MODE)} "
        f"but has {oct(mode)}."
    )


def test_run_lp_script_exists_mode_and_contents():
    # Existence & type
    assert SCRIPT_PATH.exists(), f"Expected script {SCRIPT_PATH} is missing."
    assert SCRIPT_PATH.is_file(), f"{SCRIPT_PATH} exists but is not a regular file."

    # Permissions
    mode = _mode(SCRIPT_PATH)
    assert mode == EXPECTED_SCRIPT_MODE, (
        f"{SCRIPT_PATH} should have permissions {oct(EXPECTED_SCRIPT_MODE)} "
        f"but has {oct(mode)}."
    )

    # Contents
    lines = _read_lines(SCRIPT_PATH)
    assert lines == EXPECTED_SCRIPT_LINES, (
        f"{SCRIPT_PATH} does not contain the expected lines.\n"
        f"Expected:\n{''.join(EXPECTED_SCRIPT_LINES)}\n"
        f"Found:\n{''.join(lines)}"
    )


def test_lp_result_txt_does_not_yet_exist():
    assert not RESULT_PATH.exists(), (
        f"{RESULT_PATH} already exists, but the student has not yet run the "
        f"workflow.  The initial state should *not* include this file."
    )


def test_no_extra_files_in_demo_dir():
    expected_entries = {SCRIPT_PATH.name}  # Only run_lp.py should be present
    actual_entries = {entry.name for entry in DEMO_DIR.iterdir()}
    extra = actual_entries - expected_entries
    missing = expected_entries - actual_entries

    assert not missing, (
        f"The following expected items are missing from {DEMO_DIR}: {sorted(missing)}"
    )
    assert not extra, (
        f"Unexpected extra items found in {DEMO_DIR}: {sorted(extra)}\n"
        "The starter directory should contain only run_lp.py."
    )