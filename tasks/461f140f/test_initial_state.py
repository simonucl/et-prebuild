# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the student performs any actions for the “backup-administrator”
# assignment.
#
# What we check here:
#   • Presence of the /home/user/data/… directory tree
#   • Presence, type, and POSIX permissions (0755 for dirs, 0644 for files)
#   • Exact byte-for-byte contents of the four seed files
#
# What we deliberately do *not* check (per authoring rules):
#   • Any path under /home/user/backup or /home/user/restore
#   • Any archive or log file that the student is tasked to create later
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")

# ---------------------------------------------------------------------------
# Expected directories and their required permission bits
# ---------------------------------------------------------------------------
EXPECTED_DIRS = [
    os.path.join(DATA_DIR),
    os.path.join(DATA_DIR, "finance"),
    os.path.join(DATA_DIR, "finance", "budget"),
    os.path.join(DATA_DIR, "hr"),
    os.path.join(DATA_DIR, "hr", "policies"),
]
DIR_PERMS = 0o755  # drwxr-xr-x


# ---------------------------------------------------------------------------
# Expected files, their permission bits and *exact* byte contents
# ---------------------------------------------------------------------------
EXPECTED_FILES = {
    os.path.join(DATA_DIR, "finance", "accounts.txt"): (
        0o644,
        b"Quarterly accounts receivable: Q4 2024\n"
        b"Total: 123456\n",
    ),
    os.path.join(DATA_DIR, "finance", "budget", "2024_budget.xlsx"): (
        0o644,
        b"dummy finance spreadsheet\n",
    ),
    os.path.join(DATA_DIR, "hr", "employees.csv"): (
        0o644,
        b"id,name,department\n"
        b"1,Alice,HR\n"
        b"2,Bob,HR\n",
    ),
    os.path.join(DATA_DIR, "hr", "policies", "leave_policy.md"): (
        0o644,
        b"# Leave Policy\n"
        b"All employees are entitled to 30 days of leave per year.\n",
    ),
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def _perm_bits(path):
    """Return the permission bits (similar to `ls -l` numeric mode)."""
    return stat.S_IMODE(os.stat(path).st_mode)


# ---------------------------------------------------------------------------
# Test definitions
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("dpath", EXPECTED_DIRS)
def test_required_directories_exist_with_correct_perms(dpath):
    assert os.path.exists(dpath), f"Required directory missing: {dpath}"
    assert os.path.isdir(dpath), f"Expected a directory, found something else: {dpath}"

    perms = _perm_bits(dpath)
    assert (
        perms == DIR_PERMS
    ), f"Directory {dpath} has permissions {oct(perms)}, expected {oct(DIR_PERMS)}"


@pytest.mark.parametrize("fpath,expect", EXPECTED_FILES.items())
def test_required_files_exist_with_correct_perms_and_contents(fpath, expect):
    expected_perms, expected_bytes = expect

    assert os.path.exists(fpath), f"Required file missing: {fpath}"
    assert os.path.isfile(fpath), f"Expected a regular file, found something else: {fpath}"

    perms = _perm_bits(fpath)
    assert (
        perms == expected_perms
    ), f"File {fpath} has permissions {oct(perms)}, expected {oct(expected_perms)}"

    with open(fpath, "rb") as fh:
        contents = fh.read()

    assert (
        contents == expected_bytes
    ), f"Contents of {fpath} do not match the expected initial state."