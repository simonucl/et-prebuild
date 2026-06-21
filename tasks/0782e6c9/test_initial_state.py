# test_initial_state.py
#
# This test-suite validates that the **initial** operating-system / filesystem
# state is exactly as expected *before* the student performs any actions for
# the “checksum audit trail” task.
#
# WHAT IS VERIFIED
# ----------------
# 1. Existence and emptiness of the two quarterly finance CSV files.
# 2. Existence, permissions and correct contents of the reference hash file.
# 3. Existence and permissions of the audit/ directory (the destination for
#    the future log file – the log file itself must **not** be tested here).
#
# IMPORTANT:  The tests deliberately avoid looking for
#             /home/user/audit/checksum_audit.log
#             or any other post-execution artefacts.

import hashlib
import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
DOCUMENTS_DIR = HOME / "documents"
REFERENCE_DIR = HOME / "reference"
AUDIT_DIR = HOME / "audit"

Q1_FILE = DOCUMENTS_DIR / "finance_Q1_2024.csv"
Q2_FILE = DOCUMENTS_DIR / "finance_Q2_2024.csv"
REFERENCE_FILE = REFERENCE_DIR / "hashes.sha256"

EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------


def sha256_file(path: Path) -> str:
    """Return the SHA-256 hex digest of *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def file_mode(path: Path) -> int:
    """Return the numeric (octal) mode bits of *path* (e.g. 0o644)."""
    return os.stat(path).st_mode & 0o777


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("file_path", [Q1_FILE, Q2_FILE])
def test_finance_files_exist_and_are_empty(file_path: Path):
    assert file_path.exists(), f"Expected file {file_path} to exist."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."
    size = file_path.stat().st_size
    assert size == 0, f"{file_path} should be empty (size 0), but is {size} bytes."
    digest = sha256_file(file_path)
    assert (
        digest == EMPTY_SHA256
    ), f"SHA-256 of {file_path} should be {EMPTY_SHA256}, got {digest}."


def test_reference_hash_file_exists_and_has_correct_permissions():
    assert REFERENCE_FILE.exists(), f"Reference file {REFERENCE_FILE} is missing."
    assert REFERENCE_FILE.is_file(), f"{REFERENCE_FILE} exists but is not a file."
    mode = file_mode(REFERENCE_FILE)
    assert (
        mode == 0o644
    ), f"{REFERENCE_FILE} should have mode 0644; found {oct(mode)} instead."


def test_reference_hash_file_contents_are_correct():
    expected_lines = {
        f"{EMPTY_SHA256}  finance_Q1_2024.csv\n",
        f"{EMPTY_SHA256}  finance_Q2_2024.csv\n",
    }

    with REFERENCE_FILE.open("r", encoding="utf-8") as fp:
        lines = fp.readlines()

    # Check line count
    assert (
        len(lines) == 2
    ), f"{REFERENCE_FILE} should contain exactly 2 lines, found {len(lines)}."

    # Check contents match exactly (order agnostic)
    missing = expected_lines - set(lines)
    unexpected = set(lines) - expected_lines

    assert not missing, f"Missing line(s) in {REFERENCE_FILE}: {missing}"
    assert not unexpected, f"Unexpected line(s) in {REFERENCE_FILE}: {unexpected}"


def test_audit_directory_exists_with_correct_permissions():
    assert AUDIT_DIR.exists(), f"Audit directory {AUDIT_DIR} is missing."
    assert AUDIT_DIR.is_dir(), f"{AUDIT_DIR} exists but is not a directory."
    mode = file_mode(AUDIT_DIR)
    assert (
        mode == 0o755
    ), f"{AUDIT_DIR} should have mode 0755 (world-readable/executable); found {oct(mode)}."