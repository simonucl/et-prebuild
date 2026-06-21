# test_initial_state.py
#
# Pytest suite that verifies the machine **before** the learner begins work on the
# “checksum-verification report” exercise.
#
# We make sure that:
#   • /home/user/backups/   exists
#   • the three *.sql.gz    archives are present exactly as described
#   • expected_checksums.sha256 exists and contains the three correct lines
#   • the “verification” directory either does **not** exist or, if it does, that
#     backup_checksum_report.log is absent (the learner must create it)
#
# Only the standard library and pytest are used.

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
BACKUPS_DIR = HOME / "backups"
VERIFICATION_DIR = HOME / "verification"
REPORT_FILE = VERIFICATION_DIR / "backup_checksum_report.log"

EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb924"
    "27ae41e4649b934ca495991b7852b855"
)

CUSTOMERS = BACKUPS_DIR / "db_customers_full_20230710.sql.gz"
ORDERS = BACKUPS_DIR / "db_orders_full_20230710.sql.gz"
INVENTORY = BACKUPS_DIR / "db_inventory_full_20230710.sql.gz"
EXPECTED_SHA_FILE = BACKUPS_DIR / "expected_checksums.sha256"

INVENTORY_EXPECTED_TEXT = (
    "INVENTORY BACKUP\n"
    "item_id,item_name,stock\n"
    "1001,Widget,150\n"
    "1002,Gadget,200\n"
)


# ------------------------- helper utilities ------------------------- #
def sha256(path: Path) -> str:
    """Return the hex-encoded SHA-256 digest of the file at *path*."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            h.update(block)
    return h.hexdigest()


# ----------------------------- tests -------------------------------- #
def test_backups_directory_exists():
    assert BACKUPS_DIR.is_dir(), (
        f"Required directory {BACKUPS_DIR} is missing. "
        "Copy last-night’s backups there before proceeding."
    )


@pytest.mark.parametrize(
    "file_path",
    [CUSTOMERS, ORDERS, INVENTORY],
)
def test_each_backup_archive_is_present(file_path: Path):
    assert file_path.is_file(), (
        f"Expected backup archive {file_path} is missing."
    )


def test_empty_archives_are_zero_bytes():
    for f in (CUSTOMERS, ORDERS):
        size = f.stat().st_size
        assert size == 0, (
            f"{f} should be a zero-byte (empty) file but is {size} bytes."
        )


def test_inventory_archive_has_expected_content():
    content = INVENTORY.read_text(encoding="utf-8")
    assert content == INVENTORY_EXPECTED_TEXT, (
        f"{INVENTORY} does not have the expected contents.\n"
        "Make sure it holds the INVENTORY BACKUP sample data exactly as "
        "spelled out in the task description."
    )


def test_expected_checksums_file_exists():
    assert EXPECTED_SHA_FILE.is_file(), (
        f"Required checksum listing {EXPECTED_SHA_FILE} is missing."
    )


def test_expected_checksums_file_contents():
    lines = EXPECTED_SHA_FILE.read_text(encoding="utf-8").splitlines()
    expected_lines = {
        f"{EMPTY_SHA256}  {CUSTOMERS.name}",
        f"{EMPTY_SHA256}  {ORDERS.name}",
        f"{EMPTY_SHA256}  {INVENTORY.name}",
    }
    assert set(lines) == expected_lines, (
        f"{EXPECTED_SHA_FILE} does not have the expected lines.\n"
        "It must contain exactly these three lines (hash, two spaces, filename):\n"
        + "\n".join(sorted(expected_lines))
    )


def test_inventory_checksum_is_not_empty_hash():
    actual = sha256(INVENTORY)
    assert actual != EMPTY_SHA256, (
        "Sanity check failed: inventory file’s SHA-256 appears to be the "
        "empty-file hash. The file should contain data so its digest must differ."
    )


def test_report_file_does_not_preexist():
    """
    The learner is supposed to create verification/backup_checksum_report.log.
    It should therefore not exist beforehand.
    """
    if REPORT_FILE.exists():
        # If the directory already exists, the file must NOT.
        pytest.fail(
            f"{REPORT_FILE} already exists. Remove it so the learner can create a "
            "fresh checksum-verification report."
        )