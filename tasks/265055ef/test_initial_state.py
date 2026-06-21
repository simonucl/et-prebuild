# test_initial_state.py
#
# Pytest suite that validates the operating-system state *before* the student
# performs the backup task described in the assignment.  These tests make sure
# the expected ETL pipeline directory tree is present and correct, and that no
# backup artifacts exist yet.  Failing tests will give clear, actionable error
# messages.

import os
import stat
import textwrap

import pytest

HOME = "/home/user"
PIPELINE_ROOT = os.path.join(HOME, "etl_pipeline")
BACKUP_ROOT = os.path.join(HOME, "etl_backups")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_file(path):
    with open(path, "r", encoding="utf-8") as fp:
        return fp.read()


def _assert_not_writable_by_group_or_other(path):
    mode = os.stat(path).st_mode
    assert mode & stat.S_IWGRP == 0, f"{path} should NOT be writable by group"
    assert mode & stat.S_IWOTH == 0, f"{path} should NOT be writable by others"


# ---------------------------------------------------------------------------
# Expected filesystem structure
# ---------------------------------------------------------------------------

EXPECTED_DIRS = [
    PIPELINE_ROOT,
    os.path.join(PIPELINE_ROOT, "data"),
    os.path.join(PIPELINE_ROOT, "data", "raw"),
    os.path.join(PIPELINE_ROOT, "scripts"),
    os.path.join(PIPELINE_ROOT, "config"),
]

EXPECTED_FILES = {
    os.path.join(PIPELINE_ROOT, "data", "raw", "customers.csv"): textwrap.dedent(
        """\
        id,name,signup_date
        1,Alice,2020-01-05
        2,Bob,2021-03-12
        """
    ),
    os.path.join(PIPELINE_ROOT, "data", "raw", "transactions.csv"): textwrap.dedent(
        """\
        id,customer_id,amount,transaction_date
        1001,1,250.75,2022-11-10
        1002,2,99.99,2022-11-11
        """
    ),
    os.path.join(PIPELINE_ROOT, "scripts", "extract.sh"): textwrap.dedent(
        """\
        #!/usr/bin/env bash
        echo "Extract step placeholder"
        """
    ),
    os.path.join(PIPELINE_ROOT, "scripts", "transform.py"): textwrap.dedent(
        """\
        # Minimal transform script
        print("Transform step placeholder")
        """
    ),
    os.path.join(PIPELINE_ROOT, "config", "pipeline.yaml"): textwrap.dedent(
        """\
        pipeline:
          name: poc_etl
          schedule: "@daily"
        """
    ),
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_required_directories_exist():
    """All required directories under /home/user/etl_pipeline must already exist."""
    for dpath in EXPECTED_DIRS:
        assert os.path.isdir(dpath), f"Expected directory missing: {dpath}"


def test_expected_files_exist_with_exact_contents():
    """
    All listed files must exist with *exact* byte-for-byte contents (including
    trailing newlines).
    """
    for fpath, expected_content in EXPECTED_FILES.items():
        assert os.path.isfile(fpath), f"Expected file missing: {fpath}"
        actual = _read_file(fpath)
        assert actual == expected_content, (
            f"File contents mismatch for {fpath}.\n"
            "----- expected -----\n"
            f"{expected_content!r}\n"
            "------ actual ------\n"
            f"{actual!r}"
        )


def test_permissions_are_not_group_or_other_writable():
    """No file or directory under the pipeline root should be group/other writable."""
    for root, dirs, files in os.walk(PIPELINE_ROOT):
        _assert_not_writable_by_group_or_other(root)
        for name in files:
            _assert_not_writable_by_group_or_other(os.path.join(root, name))


def test_backup_directory_does_not_yet_exist():
    """
    Before the student runs their backup script, /home/user/etl_backups must NOT exist.
    """
    assert not os.path.exists(BACKUP_ROOT), (
        f"{BACKUP_ROOT} already exists; the backup task should not have been run yet."
    )