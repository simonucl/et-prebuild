# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student carries out any work.  It asserts that
# exactly the starting artifacts are present and that none of the required
# output files have been created yet.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
INV_DIR = HOME / "inventory"
AUDIT_FILE = INV_DIR / "ssh_audit.csv"

# Files that must *not* exist yet (the deliverables)
DELIVERABLES = [
    INV_DIR / "ssh_root_status.txt",
    INV_DIR / "ssh_port_map.txt",
    INV_DIR / "ssh_summary.tsv",
]

LOG_DIR = HOME / "task_logs"
LOG_FILE = LOG_DIR / "column_manipulation.log"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _perm_bits(path: Path) -> int:
    """
    Return the permission bits (e.g. 0o755) of path.
    """
    return stat.S_IMODE(path.stat().st_mode)


def _read_lines(path: Path):
    """
    Read *text* file and return its lines without trailing newlines.
    """
    return path.read_text(encoding="utf-8").splitlines()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_inventory_directory_exists_and_permissions():
    assert INV_DIR.exists(), f"Directory {INV_DIR} is missing."
    assert INV_DIR.is_dir(), f"{INV_DIR} exists but is not a directory."
    expected_perm = 0o755
    perms = _perm_bits(INV_DIR)
    assert (
        perms == expected_perm
    ), f"Directory {INV_DIR} should have permissions {oct(expected_perm)}, found {oct(perms)}."


def test_audit_file_exists_and_permissions():
    assert AUDIT_FILE.exists(), f"File {AUDIT_FILE} is missing."
    assert AUDIT_FILE.is_file(), f"{AUDIT_FILE} exists but is not a regular file."
    expected_perm = 0o644
    perms = _perm_bits(AUDIT_FILE)
    assert (
        perms == expected_perm
    ), f"File {AUDIT_FILE} should have permissions {oct(expected_perm)}, found {oct(perms)}."


def test_audit_file_content_exact():
    expected_lines = [
        "serverName,port,permitRootLogin,protocol,extra",
        "alpha,22,yes,2,ok",
        "beta,2222,no,2,deprecated",
        "gamma,22,prohibit-password,2,ok",
        "delta,22,no,2,ok",
        "epsilon,2200,yes,2,legacy",
    ]
    actual_lines = _read_lines(AUDIT_FILE)
    assert (
        actual_lines == expected_lines
    ), f"Content of {AUDIT_FILE} does not match the required 6-line CSV template."


@pytest.mark.parametrize("path", DELIVERABLES)
def test_deliverable_files_do_not_exist_yet(path):
    assert (
        not path.exists()
    ), f"Deliverable file {path} should NOT exist before the task is attempted."


def test_log_file_absent_or_empty():
    """
    The verification log directory/file must not pre-exist.
    If the directory exists from an earlier run, that is tolerated,
    but the file itself must not yet exist.
    """
    if LOG_FILE.exists():
        pytest.fail(f"Log file {LOG_FILE} should not exist prior to student work.")


def test_no_extra_files_in_inventory(tmp_path_factory):
    """
    Ensure that /home/user/inventory only contains the single starting CSV file.
    """
    entries = sorted(INV_DIR.iterdir())
    # Permit one file only: ssh_audit.csv
    assert entries == [AUDIT_FILE], (
        f"{INV_DIR} should contain ONLY {AUDIT_FILE.name} at this stage; "
        f"found {[e.name for e in entries]}"
    )