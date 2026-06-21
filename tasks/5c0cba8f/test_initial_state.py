# test_initial_state.py
#
# Pytest suite that verifies the **initial** state of the operating system
# before the student starts working on the “compliance_audit” task.
#
# We check that the artefacts the student is required to create
#   • /home/user/compliance_audit/audit.sqlite
#   • /home/user/compliance_audit/audit_20230421.log
# are NOT present yet.  The top-level directory itself may or may not exist;
# that detail is left deliberately flexible as the spec allows for pre-existing
# unrelated content.
#
# If any of the required artefacts already exist, the tests fail with a clear
# explanation so the learner knows the environment is not in the expected
# pristine state.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
AUDIT_DIR = HOME / "compliance_audit"
DB_FILE = AUDIT_DIR / "audit.sqlite"
LOG_FILE = AUDIT_DIR / "audit_20230421.log"


@pytest.mark.parametrize(
    "path,description",
    [
        (DB_FILE, "SQLite database '/home/user/compliance_audit/audit.sqlite'"),
        (LOG_FILE, "Audit log '/home/user/compliance_audit/audit_20230421.log'"),
    ],
)
def test_required_files_absent(path: Path, description: str):
    """
    Neither the database nor the log file should exist before the student
    performs any actions.
    """
    assert not path.exists(), (
        f"{description} already exists, but the environment should start clean. "
        "Remove it before beginning the task."
    )


def test_audit_dir_state_is_consistent():
    """
    The parent directory may or may not exist.  If it does exist, it must NOT
    already contain either of the target artefacts.
    """
    if not AUDIT_DIR.exists():
        # Nothing further to check – directory absence is perfectly acceptable.
        return

    # Directory exists; ensure it does NOT already contain the artefacts we
    # expect the student to create later.
    present = [p.name for p in (DB_FILE, LOG_FILE) if p.exists()]
    assert not present, (
        "Directory '/home/user/compliance_audit/' is present but already "
        f"contains unexpected file(s): {', '.join(present)}.  The initial state "
        "must not contain these artefacts."
    )