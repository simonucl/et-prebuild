# test_initial_state.py
#
# This test-suite validates the operating-system / filesystem *before*
# the student performs any action on the machine.  It confirms that the
# starting point matches the specification that the grader as well as
# the assignment text rely on.
#
# Only stdlib + pytest are used.
#
# Paths that are inspected:
#   • /home/user/db_dumps/
#   • /home/user/backups/
#   • /home/user/backup_report.log
#
# The tests make sure that
#   1. /home/user/db_dumps exists and contains exactly the three *.sql files.
#   2. Each *.sql file has the expected size and basic contents.
#   3. /home/user/backups exists and is completely empty.
#   4. /home/user/backup_report.log does **not** exist yet.
#
# If any assertion fails, the error message tells the student exactly
# what is missing or differs from the expected initial state.

import os
from pathlib import Path

import pytest

# -----------------------------------------------------------------------------
# Reference data that the initial state *must* contain
# -----------------------------------------------------------------------------
DB_DUMPS_DIR = Path("/home/user/db_dumps")
BACKUPS_DIR = Path("/home/user/backups")
BACKUP_REPORT = Path("/home/user/backup_report.log")

EXPECTED_FILES = {
    "customers.sql": {
        "size": 43,
        "must_contain": "CREATE TABLE customers",
    },
    "orders.sql": {
        "size": 45,
        "must_contain": "CREATE TABLE orders",
    },
    "products.sql": {
        "size": 46,
        "must_contain": "CREATE TABLE products",
    },
}


# -----------------------------------------------------------------------------
# Helper utilities
# -----------------------------------------------------------------------------
def _collect_file_names(directory: Path):
    """Return a set of file names (not paths) that reside in *directory*."""
    return {p.name for p in directory.iterdir() if p.is_file()}


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_db_dumps_directory_and_files_present():
    """The /home/user/db_dumps directory exists with exactly the
    three expected SQL files and nothing else.
    """
    assert DB_DUMPS_DIR.exists(), f"Expected directory {DB_DUMPS_DIR} does not exist."
    assert DB_DUMPS_DIR.is_dir(), f"{DB_DUMPS_DIR} exists but is not a directory."

    present_files = _collect_file_names(DB_DUMPS_DIR)
    expected_files = set(EXPECTED_FILES.keys())

    # Exact membership check (both directions)
    missing = expected_files - present_files
    extra = present_files - expected_files

    assert not missing, (
        "Missing SQL dump files in /home/user/db_dumps: "
        + ", ".join(sorted(missing))
    )
    assert not extra, (
        "Unexpected extra files found in /home/user/db_dumps: "
        + ", ".join(sorted(extra))
    )


@pytest.mark.parametrize("filename,meta", EXPECTED_FILES.items())
def test_sql_file_sizes_and_basic_contents(filename, meta):
    """Each SQL file has the correct byte size and contains the expected table
    name so that later steps can rely on deterministic sizes and contents.
    """
    file_path = DB_DUMPS_DIR / filename
    assert file_path.exists(), f"Required dump file {file_path} is missing."

    stat = file_path.stat()
    assert (
        stat.st_size == meta["size"]
    ), f"{filename} has size {stat.st_size}, expected {meta['size']} bytes."

    # A light-weight content sanity check to avoid over-specifying the file
    # while still guaranteeing it is the intended SQL dump.
    with file_path.open("r", encoding="utf-8", errors="surrogateescape") as fh:
        first_line = fh.readline()
    expected_snippet = meta["must_contain"]
    assert expected_snippet in first_line, (
        f"{filename} does not appear to be the correct dump file;\n"
        f"expected the line to contain {expected_snippet!r}, got {first_line!r}"
    )


def test_backups_directory_is_empty():
    """The pre-existing /home/user/backups directory must be present and empty
    so that the student can safely create new artefacts.
    """
    assert BACKUPS_DIR.exists(), f"Expected directory {BACKUPS_DIR} does not exist."
    assert BACKUPS_DIR.is_dir(), f"{BACKUPS_DIR} exists but is not a directory."

    contents = list(BACKUPS_DIR.iterdir())
    assert (
        not contents
    ), f"{BACKUPS_DIR} is expected to be empty, but contains: {', '.join(str(p) for p in contents)}"


def test_backup_report_does_not_exist_yet():
    """backup_report.log should *not* exist before the student runs their
    backup commands.
    """
    assert not BACKUP_REPORT.exists(), (
        f"{BACKUP_REPORT} already exists, but it should be created only "
        "by the student’s backup script."
    )