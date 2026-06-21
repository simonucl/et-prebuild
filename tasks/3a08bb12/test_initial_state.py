# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state **before**
# the student performs any hardening or auditing actions for the
# “Incident directory hardening & permission audit” exercise.
#
# DO NOT MODIFY THIS FILE.  If any test here fails, the starting
# environment is not what the assignment expects.

import os
import stat
import pytest
from pathlib import Path

# Fixed paths used throughout the assignment.
INCIDENT_DIR = Path("/home/user/incident_reports")
REPORT_FILE = INCIDENT_DIR / "report_2023_11_15.txt"
FLAG_FILE = INCIDENT_DIR / "triage_complete.flag"
AUDIT_LOG = INCIDENT_DIR / "permissions_audit.log"


def _octal_mode(path: Path) -> int:
    """
    Return the permission bits of `path` as an integer in octal form
    (e.g. 0o755).  This masks out file-type bits, selinux, etc.
    """
    return stat.S_IMODE(path.stat().st_mode)


def test_incident_directory_exists_and_is_directory():
    assert INCIDENT_DIR.exists(), (
        f"Expected directory {INCIDENT_DIR} to exist, but it does not."
    )
    assert INCIDENT_DIR.is_dir(), (
        f"Expected {INCIDENT_DIR} to be a directory, but it is not."
    )


def test_incident_directory_permissions():
    mode = _octal_mode(INCIDENT_DIR)
    expected = 0o755  # rwxr-xr-x, **no** set-gid yet
    assert mode == expected, (
        f"{INCIDENT_DIR} should start with permissions {oct(expected)} "
        f"but currently has {oct(mode)}."
    )

    # Ensure the set-gid bit is NOT set in the initial state.
    has_setgid = bool(INCIDENT_DIR.stat().st_mode & stat.S_ISGID)
    assert not has_setgid, (
        f"{INCIDENT_DIR} unexpectedly has the set-gid bit set at the start."
    )


def test_report_file_exists_and_is_regular_file():
    assert REPORT_FILE.exists(), (
        f"Expected file {REPORT_FILE} to exist, but it does not."
    )
    assert REPORT_FILE.is_file(), (
        f"Expected {REPORT_FILE} to be a regular file, but it is not."
    )


def test_report_file_permissions():
    mode = _octal_mode(REPORT_FILE)
    expected = 0o644  # rw-r--r--
    assert mode == expected, (
        f"{REPORT_FILE} should start with permissions {oct(expected)} "
        f"but currently has {oct(mode)}."
    )


def test_report_file_contents_unchanged():
    expected_content = "PLACEHOLDER: do not modify\n"
    with REPORT_FILE.open("r", encoding="utf-8") as fp:
        data = fp.read()
    assert data == expected_content, (
        f"{REPORT_FILE} contents differ from the expected placeholder.\n"
        "Did someone modify the file prematurely?"
    )


def test_no_flag_file_yet():
    assert not FLAG_FILE.exists(), (
        f"{FLAG_FILE} should NOT exist in the initial state."
    )


def test_no_audit_log_yet():
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} should NOT exist in the initial state."
    )


def test_no_extra_regular_files_present():
    """
    Verify that the directory contains exactly one regular file
    (report_2023_11_15.txt) at the start.  Hidden files (dotfiles) are
    not expected either, but we only enforce the regular-file count to
    keep the check simple.
    """
    regular_files = [
        p.name
        for p in INCIDENT_DIR.iterdir()
        if p.is_file()
    ]
    assert regular_files == [REPORT_FILE.name], (
        f"Unexpected files found in {INCIDENT_DIR}: {regular_files}. "
        f"Only {REPORT_FILE.name} should be present initially."
    )