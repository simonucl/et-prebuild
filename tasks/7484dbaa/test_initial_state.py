# test_initial_state.py
"""
Pytest suite validating the *initial* filesystem state before the student’s
house-keeping script runs.

The tests intentionally *do not* look for any of the files that will be created
by the student (prod_hostnames.txt, region_counts.csv, servers_stage.csv).  We
only assert the pre-existing conditions that must be true before processing
starts.
"""

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
INV_DIR = HOME / "inventory"
SERVERS_CSV = INV_DIR / "servers.csv"
PROC_LOG = INV_DIR / "process.log"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def file_mode(path: Path) -> int:
    """Return the permission bits (e.g. 0o644) of *path*."""
    return stat.S_IMODE(path.stat().st_mode)


def read_text(path: Path) -> str:
    """Read *path* as UTF-8 text."""
    with path.open("rt", encoding="utf-8") as fh:
        return fh.read()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_inventory_directory_exists_and_is_accessible():
    assert INV_DIR.exists(), f"Required directory {INV_DIR} is missing."
    assert INV_DIR.is_dir(), f"{INV_DIR} exists but is not a directory."
    # Basic permission sanity check: directory should at least be readable/executable
    expected_exec = bool(INV_DIR.stat().st_mode & stat.S_IXUSR)
    assert expected_exec, f"{INV_DIR} must be traversable (owner execute bit set)."


def test_servers_csv_exists_and_permissions_are_644():
    assert SERVERS_CSV.exists(), f"Required file {SERVERS_CSV} is missing."
    assert SERVERS_CSV.is_file(), f"{SERVERS_CSV} exists but is not a regular file."
    assert file_mode(SERVERS_CSV) == 0o644, (
        f"{SERVERS_CSV} must have permissions 644 "
        f"(currently {oct(file_mode(SERVERS_CSV))})."
    )


def test_servers_csv_exact_contents():
    expected = (
        "id,hostname,ip,env,region\n"
        "1,web-01,10.0.0.11,prod,us-east\n"
        "2,web-02,10.0.0.12,prod,us-east\n"
        "3,api-01,10.0.1.21,staging,us-west\n"
        "4,api-02,10.0.1.22,prod,eu-central\n"
        "5,db-01,10.0.2.31,prod,us-east\n"
        "6,db-02,10.0.2.32,staging,us-west\n"
    )
    actual = read_text(SERVERS_CSV)
    assert (
        actual == expected
    ), "servers.csv does not match the expected initial contents."


def test_process_log_absent_or_regular_file():
    if PROC_LOG.exists():
        assert PROC_LOG.is_file(), (
            f"{PROC_LOG} exists but is not a regular file "
            "(it should be a normal text file or absent)."
        )
    else:
        # File absence is acceptable at this stage.
        assert not PROC_LOG.exists(), (
            f"{PROC_LOG} unexpectedly exists; "
            "this test expects it to be either absent or an empty file."
        )


def test_future_output_files_do_not_yet_exist():
    """Ensure that the files the student is about to create are *not* present."""
    for fname in (
        INV_DIR / "prod_hostnames.txt",
        INV_DIR / "region_counts.csv",
        INV_DIR / "servers_stage.csv",
    ):
        assert not fname.exists(), (
            f"{fname} should not exist before the student script runs."
        )