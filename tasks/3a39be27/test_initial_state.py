# test_initial_state.py
#
# Pytest suite that validates the operating-system state **before**
# the student performs any action for the “security-audit virtual-env”
# exercise.  The tests confirm that none of the artefacts the student
# is supposed to create yet exist.  If any of them are already present,
# the suite fails with a clear, actionable message.

import os
from pathlib import Path
import pytest

# Base paths that will be created by the student.
HOME = Path("/home/user")
SEC_AUDIT_DIR = HOME / "sec_audit"
VENV_DIR = SEC_AUDIT_DIR / "audit_env"
ACTIVATE_FILE = VENV_DIR / "bin" / "activate"
PERM_LOG = SEC_AUDIT_DIR / "activate_permission.log"


@pytest.mark.parametrize(
    "path, should_exist, descr",
    [
        (SEC_AUDIT_DIR, False, "top-level audit directory /home/user/sec_audit"),
        (VENV_DIR, False, "virtual-environment directory /home/user/sec_audit/audit_env"),
        (ACTIVATE_FILE, False, "activate script /home/user/sec_audit/audit_env/bin/activate"),
        (PERM_LOG, False, "permission-log file /home/user/sec_audit/activate_permission.log"),
    ],
)
def test_expected_artifacts_absent(path: Path, should_exist: bool, descr: str) -> None:
    """
    Ensure that no artefacts expected *after* the student completes the task
    are present *before* the task starts.
    """
    exists = path.exists()
    if should_exist:
        assert exists, f"Expected {descr} to exist, but it is missing."
    else:
        assert not exists, (
            f"{descr} already exists at {path}. "
            "The workspace must start clean so the student's work can be evaluated accurately."
        )