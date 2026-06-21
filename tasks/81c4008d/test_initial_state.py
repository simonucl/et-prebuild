# test_initial_state.py
#
# This pytest suite validates the *initial* state of the VM **before**
# the student begins implementing the Makefile-based workflow.  It proves
# that only the two raw CSV files are present with the exact expected
# contents and that *none* of the derived artefacts (Makefile, cleaned
# data, logs, stats, archive, etc.) exist yet.
#
# If any of these tests fail it means the VM was not provisioned in the
# pristine state that the assignment assumes, so the student must not be
# penalised—fix the environment first!

import os
import tarfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
PROJECT = HOME / "project"

RAW_DIR = PROJECT / "data" / "raw"
CUSTOMERS_RAW = RAW_DIR / "customers.csv"
TRANSACTIONS_RAW = RAW_DIR / "transactions.csv"

# Artefacts that **must NOT** exist yet
MAKEFILE = PROJECT / "Makefile"
CLEAN_DIR = PROJECT / "data" / "cleaned"
LOG_FILE = PROJECT / "logs" / "cleanup.log"
SUMMARY_DIR = PROJECT / "summary"
ARCHIVE_FILE = PROJECT / "archive" / "cleaned_archive.tar.gz"

CUSTOMERS_CLEAN = CLEAN_DIR / "customers.csv"
TRANSACTIONS_CLEAN = CLEAN_DIR / "transactions.csv"
CUSTOMERS_STATS = SUMMARY_DIR / "customers_stats.txt"
TRANSACTIONS_STATS = SUMMARY_DIR / "transactions_stats.txt"

# Expected raw file contents (text after final newline intentionally kept)
CUSTOMERS_EXPECTED = (
    "id,name,email\n"
    "1,Alice,alice@example.com\n"
    "2,Bob,\n"
    "3,,charlie@example.com\n"
    "4,David,david@example.com\n"
)

TRANSACTIONS_EXPECTED = (
    "tid,customer_id,amount\n"
    "1001,1,23.50\n"
    "1002,2,\n"
    "1003,3,100.00\n"
    "1004,4,55.25\n"
)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_text(path: Path) -> str:
    """Read file as UTF-8 text; raise a helpful error if it cannot be read."""
    assert path.exists(), f"Required raw file missing: {path}"
    try:
        with path.open("r", encoding="utf-8") as fh:
            return fh.read()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_raw_directory_structure():
    """The /home/user/project/data/raw directory must exist."""
    assert RAW_DIR.is_dir(), f"Directory missing: {RAW_DIR}"


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (CUSTOMERS_RAW, CUSTOMERS_EXPECTED),
        (TRANSACTIONS_RAW, TRANSACTIONS_EXPECTED),
    ],
)
def test_raw_files_exist_with_exact_content(path: Path, expected: str):
    """Raw CSVs must be present *and* contain the exact expected content."""
    content = read_text(path)
    # Compare after stripping a single trailing newline for leniency.
    assert content.rstrip("\n") == expected.rstrip("\n"), (
        f"Content of {path} does not match expected seed data.\n"
        "If this file was edited, restore the original."
    )


def test_makefile_not_present_yet():
    """Student has not authored the Makefile yet."""
    assert not MAKEFILE.exists(), (
        f"{MAKEFILE} should NOT exist prior to the student's work."
    )


@pytest.mark.parametrize(
    "path",
    [
        CLEAN_DIR,
        CUSTOMERS_CLEAN,
        TRANSACTIONS_CLEAN,
        SUMMARY_DIR,
        CUSTOMERS_STATS,
        TRANSACTIONS_STATS,
        LOG_FILE,
        ARCHIVE_FILE,
    ],
)
def test_no_derived_artefacts_present(path: Path):
    """No cleaned data, logs, stats, or archive should exist yet."""
    assert not path.exists(), (
        f"Derived artefact {path} exists prematurely.\n"
        "The environment must start in a clean state."
    )


def test_archive_is_not_a_leftover_tar():
    """Even if the archive directory exists, ensure the tarball is absent."""
    if ARCHIVE_FILE.exists():
        # If a stray tarball exists, ensure it is empty or warn.
        with tarfile.open(ARCHIVE_FILE, "r:gz") as tf:
            pytest.fail(
                f"Unexpected archive {ARCHIVE_FILE} already present with members: "
                f"{tf.getnames()}"
            )