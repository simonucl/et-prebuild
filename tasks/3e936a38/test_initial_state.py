# test_initial_state.py
#
# This pytest file validates that the workstation is in a clean
# “pre-task” state for the compliance-audit assignment.
#
# It checks that:
#   1. The directory /home/user/compliance_audit does **not** exist,
#      OR it exists but is completely empty.
#   2. The file /home/user/compliance_audit/security_audit_report.json
#      does **not** already exist.
#
# These assertions guarantee that the student starts with a blank slate
# and that any artefacts found after their solution runs are definitely
# produced by them.

from pathlib import Path
import os
import stat
import pytest

HOME_DIR = Path("/home/user").resolve()
AUDIT_DIR = HOME_DIR / "compliance_audit"
REPORT_FILE = AUDIT_DIR / "security_audit_report.json"


def _list_dir_contents(directory: Path):
    """
    Helper that returns a list of absolute Paths for every entry
    (file or directory) directly inside `directory`.
    If the directory does not exist, returns an empty list.
    """
    if not directory.exists():
        return []
    return [entry.resolve() for entry in directory.iterdir()]


def test_home_directory_exists_and_is_directory():
    assert HOME_DIR.exists(), f"Expected home directory {HOME_DIR} to exist."
    assert HOME_DIR.is_dir(), f"Expected {HOME_DIR} to be a directory."


def test_audit_directory_absent_or_empty():
    """
    The compliance_audit directory should either:
      • not exist at all, or
      • exist and be completely empty.

    This prevents any pre-existing files from interfering with
    the student’s work.
    """
    if not AUDIT_DIR.exists():
        # Ideal case: directory not yet created.
        return

    # If it does exist, ensure it is truly empty.
    assert AUDIT_DIR.is_dir(), (
        f"{AUDIT_DIR} exists but is not a directory; "
        "remove it before beginning the task."
    )

    contents = _list_dir_contents(AUDIT_DIR)
    assert (
        len(contents) == 0
    ), (
        f"{AUDIT_DIR} must be empty before the task starts, "
        f"but found these entries: {', '.join(map(str, contents))}"
    )


def test_report_file_does_not_exist():
    """
    The final JSON report must not exist yet.  If it does, the student’s
    solution might be skipped or overwritten unintentionally.
    """
    assert not REPORT_FILE.exists(), (
        f"Found pre-existing report file at {REPORT_FILE}. "
        "Remove it so the student can generate a fresh report."
    )
    # If the path exists but is something unexpected (e.g. a directory),
    # fail explicitly.
    assert not REPORT_FILE.is_dir(), (
        f"Expected {REPORT_FILE} to be absent, but a directory "
        "with that name already exists."
    )