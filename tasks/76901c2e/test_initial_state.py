# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state before the
# student performs any of the required permission-changing tasks.
#
# Checked pre-conditions (nothing from the “expected final state” is tested):
#   1. /home/user/corp/policies/company_policy.txt  → mode 600
#   2. /home/user/corp/projects/bob_project         → directory, mode 755
#   3. /home/user/corp/finance/payroll.xls          → mode 775
#
# No assertions are made about any files or directories that the student
# will create or modify later (e.g. support_task.log, shared/team_docs, etc.).
#
# Only stdlib + pytest are used.

import os
import stat
import pytest

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _imode(path: str) -> int:
    """
    Return the permission bits (e.g. 0o755) for *path*.
    """
    return stat.S_IMODE(os.stat(path).st_mode)


def _human(octal_mode: int) -> str:
    """
    Convert an int such as 0o755 to a human-readable string "755".
    """
    return oct(octal_mode).replace("0o", "")


# --------------------------------------------------------------------------- #
# Parametrised tests for the three pre-existing paths
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path, expected_mode, must_be_dir",
    [
        ("/home/user/corp/policies/company_policy.txt", 0o600, False),
        ("/home/user/corp/projects/bob_project",        0o755, True),
        ("/home/user/corp/finance/payroll.xls",         0o775, False),
    ],
)
def test_initial_files_and_dirs_present_with_correct_permissions(
    path: str, expected_mode: int, must_be_dir: bool
) -> None:
    """
    Ensure that each required path exists and has the exact permissions
    described in the task’s *initial* situation.
    """
    assert os.path.exists(path), (
        f"Required path does not exist (but should, at the start of the task): {path}"
    )

    # Verify directory/file type
    if must_be_dir:
        assert os.path.isdir(path), (
            f"Expected '{path}' to be a directory, but it is not."
        )
    else:
        assert os.path.isfile(path), (
            f"Expected '{path}' to be a regular file, but it is not."
        )

    # Verify permissions
    actual_mode = _imode(path)
    assert actual_mode == expected_mode, (
        f"Incorrect permissions on '{path}'. "
        f"Expected {_human(expected_mode)}, found {_human(actual_mode)}."
    )