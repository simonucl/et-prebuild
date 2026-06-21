# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system /
# filesystem before the student performs any action for the “FinOps quarterly
# cost report” task.
#
# Do NOT edit anything in this file when doing the task; it is only executed by
# the autograder to make sure the starting conditions are correct.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
REPORT_FILE = HOME / "reports" / "2023-Q3-cloud-costs.csv"
FINOPS_DIR = HOME / "finops"
LATEST_DIR = FINOPS_DIR / "latest"
AUDIT_LOG = FINOPS_DIR / "audit.log"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _is_empty_directory(directory: Path) -> bool:
    """Return True if `directory` exists and contains no files/dirs."""
    return directory.is_dir() and not any(directory.iterdir())


def _has_rw_execute(directory: Path) -> bool:
    """Return True if current user has rwx permissions on the directory."""
    return (
        os.access(directory, os.R_OK)
        and os.access(directory, os.W_OK)
        and os.access(directory, os.X_OK)
    )


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_report_file_exists_and_is_regular_file():
    assert REPORT_FILE.exists(), (
        f"Required source report file missing: {REPORT_FILE}"
    )
    assert REPORT_FILE.is_file(), (
        f"{REPORT_FILE} exists but is not a regular file"
    )
    mode = REPORT_FILE.stat().st_mode
    assert not stat.S_ISLNK(mode), (
        f"{REPORT_FILE} should be a regular file, not a symlink"
    )


def test_report_file_contents():
    expected_lines = [
        "Account,Service,Cost (USD)\n",
        "000123456789,EC2,1043.57\n",
        "000123456789,S3,132.18\n",
    ]
    with REPORT_FILE.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert lines == expected_lines, (
        "The contents of the report file are not as expected.\n"
        f"Expected lines:\n{expected_lines}\nGot:\n{lines}"
    )


def test_finops_directory_structure():
    # /home/user/finops must exist and be a directory.
    assert FINOPS_DIR.exists(), f"FinOps directory missing: {FINOPS_DIR}"
    assert FINOPS_DIR.is_dir(), f"{FINOPS_DIR} exists but is not a directory"

    # User needs rwx access to /home/user/finops so they can create the link and log file.
    assert _has_rw_execute(FINOPS_DIR), (
        f"User lacks rwx permissions on {FINOPS_DIR}"
    )

    # /home/user/finops/latest must exist, be a directory, and be empty.
    assert LATEST_DIR.exists(), f"'latest' directory missing: {LATEST_DIR}"
    assert LATEST_DIR.is_dir(), f"{LATEST_DIR} exists but is not a directory"
    assert _is_empty_directory(LATEST_DIR), (
        f"'latest' directory should start empty but contains: "
        f"{list(LATEST_DIR.iterdir())}"
    )


def test_audit_log_absent_before_task():
    assert not AUDIT_LOG.exists(), (
        f"Audit log {AUDIT_LOG} should not exist before the task begins"
    )


def test_symlink_does_not_preexist():
    target_link = LATEST_DIR / "current_qtr_costs.csv"
    assert not target_link.exists(), (
        f"Symlink {target_link} should not exist before the task begins"
    )