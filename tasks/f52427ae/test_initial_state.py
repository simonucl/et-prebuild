# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# BEFORE the student performs any actions described in the task.
#
# These tests guard against starting from an already-modified system.
# If any test here fails, the environment is not in the expected
# “before” layout and must be fixed *before* the student solution runs.
#
# Rules checked (initial state expected):
# 1. /home/user/site_admin/users.csv exists with **exact** contents:
#
#        username,status
#        alice,active
#        bob,active
#        charlie,active
#
#    (including a trailing newline on every line, i.e. file length 4 lines).
#
# 2. Workspace directories that must already exist:
#       /home/user/site_admin/www/alice/
#       /home/user/site_admin/www/bob/
#       /home/user/site_admin/www/charlie/
#
#    Each of them must contain an index.html file (content and permissions
#    are *not* validated here).
#
# 3. Workspace directory that must **NOT** exist yet:
#       /home/user/site_admin/www/dana/
#
# 4. File /home/user/site_admin/admin_actions.log must either not exist or,
#    if it exists, it must **NOT** already contain any entries mentioning
#    the username 'dana' or a DEACTIVATE_USER or DELETE_WORKSPACE action
#    for 'charlie'.  (Those actions belong to the “after” state.)
#
# Only the Python standard library and pytest are used.

import os
import re
import stat
from pathlib import Path

import pytest


HOME = Path("/home/user")
SITE_ADMIN = HOME / "site_admin"
USERS_CSV = SITE_ADMIN / "users.csv"
WWW = SITE_ADMIN / "www"
ADMIN_LOG = SITE_ADMIN / "admin_actions.log"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def assert_exists(path: Path, is_dir: bool = False, is_file: bool = False):
    """Assert that *path* exists and is a directory/file as requested."""
    assert path.exists(), f"Expected {path} to exist, but it is missing."
    if is_dir:
        assert path.is_dir(), f"Expected {path} to be a directory."
    if is_file:
        assert path.is_file(), f"Expected {path} to be a regular file."


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_site_admin_structure_exists():
    """Top-level folder, csv and www directory must be present."""
    assert_exists(SITE_ADMIN, is_dir=True)
    assert_exists(USERS_CSV, is_file=True)
    assert_exists(WWW, is_dir=True)


def test_users_csv_initial_contents_exact_match():
    """users.csv must contain exactly three active users alice/bob/charlie."""
    expected_lines = [
        "username,status\n",
        "alice,active\n",
        "bob,active\n",
        "charlie,active\n",
    ]
    data = USERS_CSV.read_text(encoding="utf-8")
    actual_lines = data.splitlines(keepends=True)
    assert actual_lines == expected_lines, (
        "users.csv does not match the expected initial contents.\n"
        f"Expected lines:\n{''.join(expected_lines)}\n"
        f"Actual lines:\n{''.join(actual_lines)}"
    )


@pytest.mark.parametrize("user", ["alice", "bob", "charlie"])
def test_existing_workspaces_and_index_files(user):
    """alice, bob and charlie workspaces must pre-exist with index.html."""
    ws_dir = WWW / user
    idx_file = ws_dir / "index.html"

    assert_exists(ws_dir, is_dir=True)
    assert_exists(idx_file, is_file=True)

    # Directory must be at least accessible (r-x) by owner.
    dir_mode = ws_dir.stat().st_mode
    assert dir_mode & stat.S_IRUSR, f"{ws_dir} is not readable by owner."
    assert dir_mode & stat.S_IXUSR, f"{ws_dir} is not executable by owner."


def test_dana_workspace_must_not_exist_yet():
    """dana directory should not exist in the initial state."""
    dana_dir = WWW / "dana"
    assert not dana_dir.exists(), (
        "Workspace for user 'dana' already exists, "
        "but it must be created by the student solution."
    )


def test_admin_log_not_prepopulated_with_solution_actions():
    """
    admin_actions.log may or may not exist initially, but it must **not**
    already contain actions that belong to the student's forthcoming work
    (e.g. ADD_USER for dana or DEACTIVATE_USER for charlie).
    """
    if not ADMIN_LOG.exists():
        pytest.skip("admin_actions.log does not exist yet; this is allowed.")

    pattern = re.compile(
        r".*,(ADD_USER|DEACTIVATE_USER|DELETE_WORKSPACE|CREATE_WORKSPACE|SET_PERMS),"
        r"(dana|charlie)\s*$"
    )

    offending_lines = [
        line for line in ADMIN_LOG.read_text(encoding="utf-8").splitlines()
        if pattern.search(line)
    ]
    assert not offending_lines, (
        "admin_actions.log already contains entries that should only appear "
        "AFTER the student performs the required actions:\n"
        + "\n".join(offending_lines)
    )