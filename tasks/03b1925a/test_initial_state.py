# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the correct **initial** state _before_ the student performs
# any actions for the “FinOps analyst” assignment.
#
# Rules enforced here:
#   • The two source CSV files must exist with the exact, untampered
#     size and SHA-256 checksum given in the task description.
#   • No output artefacts (/home/user/checksums/*.txt or *.log) are
#     allowed to exist yet.
#   • There must be no extra “*.csv” files in /home/user/cloud_invoices.


import hashlib
import os
import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

CLOUD_DIR = Path("/home/user/cloud_invoices")
CHECKSUMS_DIR = Path("/home/user/checksums")

EXPECTED_FILES = {
    Path("/home/user/cloud_invoices/AWS_2023-07.csv"): {
        "size": 3,
        "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    },
    Path("/home/user/cloud_invoices/GCP_2023-07.csv"): {
        "size": 5,
        "sha256": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
    },
}


def sha256_hex(path: Path) -> str:
    """Calculate the SHA-256 of a file and return the lowercase hex digest."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_cloud_invoices_directory_exists_and_is_directory():
    assert CLOUD_DIR.exists(), f"Required directory {CLOUD_DIR} is missing."
    assert CLOUD_DIR.is_dir(), f"{CLOUD_DIR} exists but is not a directory."


def test_exact_set_of_csv_files_present_and_no_extras():
    csv_files_on_disk = sorted(CLOUD_DIR.glob("*.csv"))
    expected_files_sorted = sorted(EXPECTED_FILES.keys())

    assert (
        csv_files_on_disk == expected_files_sorted
    ), (
        "Mismatch in CSV files present.\n"
        f"Expected exactly:\n  {expected_files_sorted}\n"
        f"But found:\n  {csv_files_on_disk}"
    )


@pytest.mark.parametrize("file_path,meta", EXPECTED_FILES.items())
def test_each_csv_has_correct_size_and_sha256(file_path: Path, meta: dict):
    assert file_path.exists(), f"Required file {file_path} is missing."

    # Size check (raw bytes, no separators/units)
    size_on_disk = file_path.stat().st_size
    expected_size = meta["size"]
    assert (
        size_on_disk == expected_size
    ), f"{file_path} has size {size_on_disk} but expected {expected_size} bytes."

    # SHA-256 check
    digest = sha256_hex(file_path)
    expected_digest = meta["sha256"]
    assert (
        digest == expected_digest
    ), f"{file_path} SHA-256 mismatch: got {digest}, expected {expected_digest}."


def test_no_output_files_exist_yet():
    """
    Prior to the student's action there must be NO output artefacts such as:
      • /home/user/checksums/invoice_checksums_July2023.txt
      • /home/user/checksums/verification_July2023.log
    The directory /home/user/checksums itself should also not exist yet
    (or at least be empty), ensuring a clean slate.
    """
    checksum_txt = CHECKSUMS_DIR / "invoice_checksums_July2023.txt"
    log_file = CHECKSUMS_DIR / "verification_July2023.log"

    assert not checksum_txt.exists(), (
        f"Output file {checksum_txt} should not exist before the task starts."
    )
    assert not log_file.exists(), (
        f"Output file {log_file} should not exist before the task starts."
    )

    # If the directory exists already for some reason, verify it is empty
    # so that stale files cannot interfere with grading.
    if CHECKSUMS_DIR.exists():
        unexpected_entries = [p for p in CHECKSUMS_DIR.iterdir()]
        assert (
            len(unexpected_entries) == 0
        ), f"{CHECKSUMS_DIR} should be empty but contains: {unexpected_entries}"