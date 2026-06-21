# test_initial_state.py
#
# Pytest suite that validates the expected *initial* filesystem layout
# before the learner performs any actions for the “storage usage summary”
# exercise.  Only standard-library modules and pytest are used.

import csv
import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
STORAGE_DIR = HOME / "storage"
LOGS_DIR = STORAGE_DIR / "logs"
VOLUMES_CSV = STORAGE_DIR / "volumes.csv"

# ---- helpers -----------------------------------------------------------------


def octal_permissions(p: Path) -> int:
    """
    Return the permission bits (e.g. 0o755, 0o644) for a given Path.
    """
    return stat.S_IMODE(p.stat().st_mode)


# ---- tests -------------------------------------------------------------------


def test_storage_directory_exists():
    """
    /home/user/storage must exist and be a directory.
    """
    assert STORAGE_DIR.exists(), f"Required directory {STORAGE_DIR} is missing."
    assert STORAGE_DIR.is_dir(), f"{STORAGE_DIR} exists but is not a directory."


def test_logs_directory_exists_and_permissions():
    """
    /home/user/storage/logs must exist with permissions 0755.
    """
    assert LOGS_DIR.exists(), f"Required directory {LOGS_DIR} is missing."
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."

    expected_perm = 0o755
    actual_perm = octal_permissions(LOGS_DIR)
    assert (
        actual_perm == expected_perm
    ), f"{LOGS_DIR} permissions are {oct(actual_perm)}, expected {oct(expected_perm)}."


def test_volumes_csv_exists_and_permissions():
    """
    /home/user/storage/volumes.csv must exist with permissions 0644.
    """
    assert VOLUMES_CSV.exists(), f"Required file {VOLUMES_CSV} is missing."
    assert VOLUMES_CSV.is_file(), f"{VOLUMES_CSV} exists but is not a regular file."

    expected_perm = 0o644
    actual_perm = octal_permissions(VOLUMES_CSV)
    assert (
        actual_perm == expected_perm
    ), f"{VOLUMES_CSV} permissions are {oct(actual_perm)}, expected {oct(expected_perm)}."


@pytest.fixture(scope="module")
def csv_rows():
    """
    Read the CSV file once and expose the parsed rows as a list of dicts.
    """
    with VOLUMES_CSV.open(newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    return rows


def test_volumes_csv_header(csv_rows):
    """
    The CSV header must match:
        hostname,mount_point,disk_total_gb,disk_used_gb
    """
    expected_fieldnames = [
        "hostname",
        "mount_point",
        "disk_total_gb",
        "disk_used_gb",
    ]
    assert (
        csv_rows
    ), f"{VOLUMES_CSV} appears to be empty or has no data rows."

    actual_fieldnames = list(csv_rows[0].keys())
    assert (
        actual_fieldnames == expected_fieldnames
    ), f"CSV header fields are {actual_fieldnames}, expected {expected_fieldnames}."


def test_volumes_csv_content(csv_rows):
    """
    Validate that the CSV contains exactly the expected five data rows
    and that numeric fields are integers.
    """
    expected_rows = [
        ("alpha", "/data", 500, 325),
        ("alpha", "/backup", 1000, 100),
        ("bravo", "/data", 750, 629),
        ("bravo", "/logs", 250, 77),
        ("charlie", "/var", 600, 420),
    ]

    assert len(csv_rows) == len(
        expected_rows
    ), f"CSV should have {len(expected_rows)} data rows, found {len(csv_rows)}."

    for idx, (expected_host, expected_mount, expected_total, expected_used) in enumerate(
        expected_rows
    ):
        row = csv_rows[idx]
        host = row["hostname"]
        mount = row["mount_point"]
        try:
            total = int(row["disk_total_gb"])
            used = int(row["disk_used_gb"])
        except ValueError:
            pytest.fail(
                f"Row {idx+1}: disk_total_gb and disk_used_gb must be integers "
                f"(got {row['disk_total_gb']!r}, {row['disk_used_gb']!r})."
            )

        assert (
            host == expected_host
        ), f"Row {idx+1}: hostname is {host!r}, expected {expected_host!r}."
        assert (
            mount == expected_mount
        ), f"Row {idx+1}: mount_point is {mount!r}, expected {expected_mount!r}."
        assert (
            total == expected_total
        ), f"Row {idx+1}: disk_total_gb is {total}, expected {expected_total}."
        assert (
            used == expected_used
        ), f"Row {idx+1}: disk_used_gb is {used}, expected {expected_used}."