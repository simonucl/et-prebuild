# test_initial_state.py
"""
Pytest suite that validates the pre-exercise operating-system / filesystem state.

The checks performed here assert that the *initial* deployment environment is
exactly as described in the task:

1. /home/user/optim            – must exist and be a directory (mode 755).
2. /home/user/optim/update_lp.py – must exist, be executable, have mode 755 and
   contain the exact 7-line stub shown in the task description.
3. /home/user/optim/verification.log – MUST NOT exist yet; the student will
   create it during the exercise.

Only the Python stdlib and pytest are used.
"""

import os
import stat
from pathlib import Path

import pytest


OPTIM_DIR = Path("/home/user/optim")
UPDATE_LP = OPTIM_DIR / "update_lp.py"
VERIFICATION_LOG = OPTIM_DIR / "verification.log"

EXPECTED_UPDATE_LP_CONTENT = (
    "#!/usr/bin/env python3\n"
    '"""\n'
    "Tiny smoke-test LP solver stub shipped with every deployment.\n"
    "DO NOT EDIT.\n"
    '"""\n'
    "def main():\n"
    '    print("SOLVER_OK objective=1764")\n'
    'if __name__ == "__main__":\n'
    "    main()\n"
)


def _mode(path: Path) -> int:
    """
    Return path permission bits (e.g. 0o755) without file-type bits.
    """
    return stat.S_IMODE(path.stat().st_mode)


@pytest.mark.order(1)
def test_optim_directory_exists_with_correct_permissions():
    assert OPTIM_DIR.exists(), (
        f"Required directory {OPTIM_DIR} is missing. "
        "The deployment directory must be present before the exercise starts."
    )
    assert OPTIM_DIR.is_dir(), f"{OPTIM_DIR} exists but is not a directory."

    expected_mode = 0o755
    actual_mode = _mode(OPTIM_DIR)
    assert (
        actual_mode == expected_mode
    ), f"{OPTIM_DIR} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}."


@pytest.mark.order(2)
def test_update_lp_exists_executable_with_correct_permissions():
    assert UPDATE_LP.exists(), (
        f"Required solver script {UPDATE_LP} is missing. "
        "It must be present before the exercise starts."
    )
    assert UPDATE_LP.is_file(), f"{UPDATE_LP} exists but is not a regular file."

    # Check that it is executable by the owner.
    is_exec = os.access(UPDATE_LP, os.X_OK)
    assert is_exec, f"{UPDATE_LP} is not marked as executable."

    expected_mode = 0o755
    actual_mode = _mode(UPDATE_LP)
    assert (
        actual_mode == expected_mode
    ), f"{UPDATE_LP} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}."


@pytest.mark.order(3)
def test_update_lp_has_exact_expected_content():
    actual_content = UPDATE_LP.read_text(encoding="utf-8")
    assert (
        actual_content == EXPECTED_UPDATE_LP_CONTENT
    ), (
        f"{UPDATE_LP} content differs from the expected stub.\n"
        "Ensure the file has not been modified prior to the exercise."
    )

    # Additional sanity: file should end with a single trailing newline
    assert actual_content.endswith("\n"), f"{UPDATE_LP} must end with a newline character."


@pytest.mark.order(4)
def test_verification_log_is_absent_initially():
    assert (
        not VERIFICATION_LOG.exists()
    ), (
        f"{VERIFICATION_LOG} already exists but should not be present before the student "
        "runs the solver. Ensure the workspace is clean."
    )