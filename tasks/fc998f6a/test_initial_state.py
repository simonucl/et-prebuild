# test_initial_state.py
#
# Pytest suite that verifies the filesystem state **before** the student
# begins any work on the “symlink repair” task.  All assertions include
# custom messages so that failures clearly describe what is wrong and
# where to look.

import os
from pathlib import Path
import pytest
import stat


# ---------------------------------------------------------------------------
# Constants – absolute paths we will validate
# ---------------------------------------------------------------------------

BACKUP_DIR = Path("/home/user/backups/full_2023_10_01/data")
PROJECT_LINK_DIR = Path("/home/user/project/data_link")
AUDIT_LOG = Path("/home/user/project/symlink_audit.log")

DB_FILES = ["customer.db", "orders.db", "inventory.db"]


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def is_regular_file(path: Path) -> bool:
    """True if `path` is a real, regular file (not a symlink)."""
    try:
        return path.is_file() and not path.is_symlink()
    except FileNotFoundError:
        return False


def symlink_target(path: Path) -> str:
    """Return the absolute path that a symlink ultimately resolves to."""
    return str(path.resolve())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_backup_files_exist_and_are_regular_files():
    """
    Verify that the three .db files exist inside the latest backup directory
    and are *regular* files (not symlinks, devices, etc.).
    """
    assert BACKUP_DIR.is_dir(), (
        f"Expected backup directory '{BACKUP_DIR}' to exist and be a directory."
    )

    missing = [f for f in DB_FILES if not (BACKUP_DIR / f).exists()]
    assert not missing, (
        f"The following files are missing from {BACKUP_DIR}: {', '.join(missing)}"
    )

    non_regular = [
        f for f in DB_FILES
        if not is_regular_file(BACKUP_DIR / f)
    ]
    assert not non_regular, (
        f"The following paths exist but are not regular files in {BACKUP_DIR}: "
        f"{', '.join(non_regular)}"
    )


def test_project_link_directory_exists():
    """
    The project directory that will host the symbolic links must exist.
    """
    assert PROJECT_LINK_DIR.is_dir(), (
        f"Expected project link directory '{PROJECT_LINK_DIR}' to exist and be a directory."
    )


def test_customer_db_symlink_is_correct_and_working():
    """
    customer.db symlink should already be correct and functional.
    """
    link_path = PROJECT_LINK_DIR / "customer.db"
    expected_target = str((BACKUP_DIR / "customer.db").resolve())

    assert link_path.is_symlink(), (
        f"'{link_path}' is expected to be a symlink but is not."
    )
    assert os.path.exists(link_path), (
        f"'{link_path}' is a symlink but it is broken (target does not exist)."
    )
    assert symlink_target(link_path) == expected_target, (
        f"'{link_path}' should point to '{expected_target}' "
        f"but actually resolves to '{symlink_target(link_path)}'."
    )


def test_orders_db_symlink_is_present_but_broken():
    """
    orders.db symlink should exist yet be broken (points to missing September backup).
    """
    link_path = PROJECT_LINK_DIR / "orders.db"
    expected_target_tail = "/home/user/backups/full_2023_09_01/data/orders.db"

    assert link_path.is_symlink(), (
        f"'{link_path}' is expected to be a symlink but is not."
    )

    # The link should *not* resolve to an existing file.
    assert not os.path.exists(link_path), (
        f"'{link_path}' is expected to be a broken symlink, "
        f"but it resolves to an existing file."
    )

    # Its resolved path should match the (now missing) September backup.
    assert symlink_target(link_path) == expected_target_tail, (
        f"'{link_path}' should resolve to '{expected_target_tail}', "
        f"but actually resolves to '{symlink_target(link_path)}'."
    )


def test_inventory_db_symlink_is_missing():
    """
    inventory.db symlink should *not* exist at all in the initial state.
    """
    link_path = PROJECT_LINK_DIR / "inventory.db"
    assert not link_path.exists(), (
        f"'{link_path}' should be absent in the initial state but is present."
    )


def test_audit_log_not_present_initially():
    """
    The audit log must not pre-exist; it should be created by the student's script.
    """
    assert not AUDIT_LOG.exists(), (
        f"Audit log '{AUDIT_LOG}' should not exist before the task is performed."
    )