# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before**
# the student carries out any actions for the “checksum / quarantine /
# audit-log” task.
#
# Expectations:
# 1. The raw directory and four specific files already exist.
# 2. The reference_md5.txt file lists exactly three checksums.
# 3. customers.csv   and transactions.csv already match their reference
#    checksums, while products.csv is intentionally corrupted.
# 4. No “cleaned”, “quarantine” directories or audit-log file exist yet.
#
# If any of these pre-conditions are violated the tests will fail,
# giving the learner a clear signal that the starting environment is
# wrong.

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
RAW_DIR = HOME / "datasets" / "raw"
REFERENCE_FILE = HOME / "datasets" / "reference_md5.txt"
CLEANED_DIR = HOME / "datasets" / "cleaned"
QUARANTINE_DIR = HOME / "datasets" / "quarantine"
AUDIT_LOG = HOME / "dataset_audit.log"

RAW_FILES = {
    "customers.csv": "0cc175b9c0f1b6a831c399e269772661",   # content: "a"
    "products.csv":  "4a8a08f09d37b73795649038408b5f33",   # should NOT match
    "transactions.csv": "92eb5ffee6ae2fec3ad71c777531578f" # content: "b"
}


def md5_of_file(path: Path) -> str:
    """Return the hexadecimal MD5 checksum of the file at *path*."""
    hash_md5 = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def read_reference_md5_file() -> dict:
    """Parse reference_md5.txt into a {filename: checksum} dict."""
    if not REFERENCE_FILE.exists():
        pytest.fail(f"Reference file missing: {REFERENCE_FILE}")
    reference = {}
    with REFERENCE_FILE.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            # expecting format: "<hash>  <filename>"
            try:
                checksum, filename = line.split(None, 1)
            except ValueError:  # pragma: no cover
                pytest.fail(f"Malformed line in {REFERENCE_FILE}: {line!r}")
            reference[filename.strip()] = checksum.strip()
    return reference


# --------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------- #

def test_raw_directory_exists():
    assert RAW_DIR.is_dir(), f"Expected raw directory to exist: {RAW_DIR}"


@pytest.mark.parametrize("fname", RAW_FILES.keys())
def test_each_raw_file_exists(fname):
    path = RAW_DIR / fname
    assert path.is_file(), f"Missing file: {path}"


def test_reference_md5_file_content():
    reference = read_reference_md5_file()
    # Must contain exactly the three expected lines
    assert reference.keys() == RAW_FILES.keys(), (
        f"{REFERENCE_FILE} must reference exactly these files: "
        f"{', '.join(RAW_FILES)}"
    )
    # Check that the expected hash in the truth matches customers/products/transactions
    for fname, expected_hash in RAW_FILES.items():
        assert reference[fname] == expected_hash, (
            f"Checksum for {fname!r} in {REFERENCE_FILE} is "
            f"'{reference[fname]}', expected '{expected_hash}'."
        )


def test_actual_md5s_match_or_mismatch_as_expected():
    reference = read_reference_md5_file()
    ok_files = []
    corrupt_files = []

    for fname, ref_hash in reference.items():
        path = RAW_DIR / fname
        act_hash = md5_of_file(path)
        if act_hash == ref_hash:
            ok_files.append(fname)
        else:
            corrupt_files.append(fname)

    # According to the problem statement: customers.csv + transactions.csv OK,
    # products.csv CORRUPT.
    assert ok_files == ["customers.csv", "transactions.csv"], (
        "customers.csv and transactions.csv should already match their "
        "reference checksums."
    )
    assert corrupt_files == ["products.csv"], (
        "products.csv is expected to be corrupted initially."
    )


def test_cleaned_quarantine_and_log_absent():
    # Before student runs anything none of these should exist
    assert not CLEANED_DIR.exists(), f"Directory should not yet exist: {CLEANED_DIR}"
    assert not QUARANTINE_DIR.exists(), f"Directory should not yet exist: {QUARANTINE_DIR}"
    assert not AUDIT_LOG.exists(), f"Audit log should not yet exist: {AUDIT_LOG}"