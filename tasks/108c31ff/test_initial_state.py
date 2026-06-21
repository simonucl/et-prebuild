# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state expected by the
assignment “quick security-hygiene scan on PostgreSQL backups”.

The tests purposefully avoid checking for any objects that the student’s
solution is supposed to create later (e.g. /home/user/security_scan/*).

Only Python stdlib + pytest are used.
"""
import os
import stat
import gzip
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# CONSTANTS                                                                   #
# --------------------------------------------------------------------------- #
HOME = Path("/home/user")
BACKUP_DIR = HOME / "db_backups"

HR_SQL = BACKUP_DIR / "hr_2023-05-01.sql"
SALES_SQL_GZ = BACKUP_DIR / "sales_2023-05-01.sql.gz"
DEV_SQL = BACKUP_DIR / "dev_2023-05-01.sql"

EXPECTED_HR_CONTENT = [
    "-- HR Database dump",
    "CREATE TABLE employees(id int);",
    "CREATE ROLE hr_user WITH LOGIN PASSWORD 'secret123';",
    "-- End",
]

EXPECTED_DEV_CONTENT = [
    "-- Dev DB",
    "SELECT 1;",
]


# --------------------------------------------------------------------------- #
# HELPERS                                                                     #
# --------------------------------------------------------------------------- #
def octal_perm(path: Path) -> str:
    """
    Return the file permission bits as a zero-padded octal string, e.g. "0644".
    """
    return format(stat.S_IMODE(path.stat().st_mode), "04o")


# --------------------------------------------------------------------------- #
# TESTS                                                                       #
# --------------------------------------------------------------------------- #
def test_backup_directory_exists_and_is_directory():
    assert BACKUP_DIR.exists(), f"Expected directory {BACKUP_DIR} to exist."
    assert BACKUP_DIR.is_dir(), f"{BACKUP_DIR} exists but is not a directory."


@pytest.mark.parametrize(
    "path, expected_perm",
    [
        (HR_SQL, "0644"),
        (SALES_SQL_GZ, "0600"),
        (DEV_SQL, "0600"),
    ],
)
def test_backup_files_exist_and_have_correct_permissions(path: Path, expected_perm: str):
    assert path.exists(), f"Expected backup file {path} to exist."
    assert path.is_file(), f"{path} exists but is not a regular file."
    actual_perm = octal_perm(path)
    assert (
        actual_perm == expected_perm
    ), f"{path} has permissions {actual_perm}, expected {expected_perm}."


def test_hr_sql_content_exact_match():
    assert HR_SQL.exists(), f"{HR_SQL} missing (required for content check)."
    with HR_SQL.open("r", encoding="utf-8") as fh:
        lines = [line.rstrip("\n") for line in fh.readlines()]
    assert (
        lines == EXPECTED_HR_CONTENT
    ), f"Content of {HR_SQL} does not match expected 4-line template."


def test_dev_sql_content_exact_match():
    assert DEV_SQL.exists(), f"{DEV_SQL} missing (required for content check)."
    with DEV_SQL.open("r", encoding="utf-8") as fh:
        lines = [line.rstrip("\n") for line in fh.readlines()]
    assert (
        lines == EXPECTED_DEV_CONTENT
    ), f"Content of {DEV_SQL} does not match expected 2-line template."


def test_sales_sql_gz_is_valid_gzip_stream():
    """
    Ensure the .sql.gz file is a readable gzip stream.  We don't inspect the
    contents, merely that it can be decompressed without error and yields data.
    """
    assert SALES_SQL_GZ.exists(), f"{SALES_SQL_GZ} missing (required for gzip check)."
    with gzip.open(SALES_SQL_GZ, "rb") as fh:
        data = fh.read(100)  # read a small chunk; entire file not needed
    assert (
        data
    ), f"{SALES_SQL_GZ} appears to be empty or not a valid gzip stream."


def test_hr_file_is_world_readable_by_other():
    """
    Ensure that the 'other' read bit (world-readable) is set for hr_2023-05-01.sql.
    """
    st_mode = HR_SQL.stat().st_mode
    has_other_read = bool(st_mode & stat.S_IROTH)
    assert (
        has_other_read
    ), f"{HR_SQL} should be world-readable (permission 0644) but is not."


def test_no_unexpected_backups_missing():
    """
    Sanity check that *at least* the three expected backup files are present.
    This guards against accidental test-environment corruption.
    """
    present_files = {p.name for p in BACKUP_DIR.iterdir() if p.is_file()}
    expected_files = {HR_SQL.name, SALES_SQL_GZ.name, DEV_SQL.name}
    missing = expected_files - present_files
    assert not missing, f"Expected backup files missing: {', '.join(sorted(missing))}"