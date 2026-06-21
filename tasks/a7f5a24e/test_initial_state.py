# test_initial_state.py
#
# This test-suite validates that the workstation is in a **pristine state**
# before the student begins the “mini-compliance lab” exercise.
# Nothing that the specification asks the student to create should already
# exist.  If any artefact is found, the test will fail with a clear,
# human-readable message.
#
# Allowed libraries: stdlib + pytest only.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
AUDIT_DIR = HOME / "audit_db"
COMPANY_DB = AUDIT_DIR / "company.db"
PERMISSION_LOG = AUDIT_DIR / "permission_audit.log"
SUMMARY_TXT = AUDIT_DIR / "audit_summary.txt"


def _exists(path: Path) -> bool:
    """Convenience helper : return True if the path exists (file OR dir)."""
    return path.exists()


def _is_tight_permission(path: Path) -> bool:
    """
    Helper to check that a file does *not* already have mode 0o660.
    Used only if the file unexpectedly exists.
    """
    return (stat.S_IMODE(path.stat().st_mode) == 0o660)


def _format_missing(path: Path) -> str:
    return f"'{path}' should NOT be present at the start of the exercise."


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            AUDIT_DIR,
            id=str(AUDIT_DIR)
        ),
        pytest.param(
            COMPANY_DB,
            id=str(COMPANY_DB)
        ),
        pytest.param(
            PERMISSION_LOG,
            id=str(PERMISSION_LOG)
        ),
        pytest.param(
            SUMMARY_TXT,
            id=str(SUMMARY_TXT)
        ),
    ],
)
def test_required_items_absent(path):
    """
    Assert that none of the deliverables defined in the assignment exist yet.

    Students are supposed to create these artefacts from scratch, so any
    pre-existing file/dir would indicate an incorrect initial environment.
    """
    assert not _exists(path), _format_missing(path)


def test_home_directory_exists():
    """
    Sanity-check: the base home directory must exist and be a directory.

    This ensures the test runner itself is using the expected filesystem
    layout.
    """
    assert HOME.exists(), f"Expected base path '{HOME}' to exist."
    assert HOME.is_dir(), f"Expected '{HOME}' to be a directory."


def test_no_preexisting_db_with_permissions():
    """
    Additional guard: even if the company.db file does exist (it should not),
    verify that it does NOT already have the hardened 0o660 mode.

    This prevents a false sense of security where an unintended database file
    slips through with the correct permissions before the task begins.
    """
    if COMPANY_DB.exists():
        assert not _is_tight_permission(
            COMPANY_DB
        ), (
            f"{COMPANY_DB} unexpectedly exists with mode 660; "
            "the workstation should start empty."
        )