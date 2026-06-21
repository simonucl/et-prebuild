# test_initial_state.py
#
# Pytest suite that validates the expected *initial* state of the
# filesystem before the student’s solution runs.
#
# What is checked
# ---------------
# 1. Presence of the expected directory tree under /home/user/data_cluster
# 2. Presence and contents (via MD5) of each individual file
# 3. Presence and exact contents of the shipping manifest
# 4. Absence of any pre-existing integrity report directory or file
#
# Only stdlib + pytest are used.

import hashlib
from pathlib import Path

import pytest

# ---------- CONSTANTS ---------------------------------------------------------

HOME = Path("/home/user")
DATA_CLUSTER = HOME / "data_cluster"
BACKUP_MANIFESTS = HOME / "backup_manifests"
MANIFEST_FILE = BACKUP_MANIFESTS / "daily_20240515.md5"
INTEGRITY_REPORTS_DIR = HOME / "integrity_reports"
REPORT_FILE = INTEGRITY_REPORTS_DIR / "daily_20240515_integrity.log"

# Expected files with their *actual* current MD5 hashes on disk
FILE_EXPECTATIONS = {
    DATA_CLUSTER / "node1" / "users.db": "acbd18db4cc2f85cedef654fccc4a4d8",
    DATA_CLUSTER / "node2" / "transactions.db": "37b51d194a7513e45b56f6524f2d51f2",
    DATA_CLUSTER / "node2" / "corrupt.txt": "5d41402abc4b2a76b9719d911017c592",  # intentionally differs from manifest
    DATA_CLUSTER / "node3" / "logs.log": "73feffa4b7f6bb68e44cf984c85f6e88",
}

# Manifest lines in the *exact* order & format that should already exist in the file.
MANIFEST_EXPECTED_LINES = [
    "acbd18db4cc2f85cedef654fccc4a4d8  node1/users.db",
    "37b51d194a7513e45b56f6524f2d51f2  node2/transactions.db",
    "73feffa4b7f6bb68e44cf984c85f6e88  node3/logs.log",
    "acbd18db4cc2f85cedef654fccc4a4d8  node2/corrupt.txt",
]

# ---------- HELPERS -----------------------------------------------------------


def md5sum(path: Path) -> str:
    """Return the hex MD5 digest of the given file."""
    h = hashlib.md5()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- TESTS -------------------------------------------------------------


def test_required_directories_exist():
    """Check that the main data directories are present."""
    assert DATA_CLUSTER.is_dir(), f"Expected directory {DATA_CLUSTER} is missing."
    assert BACKUP_MANIFESTS.is_dir(), f"Expected directory {BACKUP_MANIFESTS} is missing."

    # Check the three node sub-directories
    for node in ("node1", "node2", "node3"):
        node_dir = DATA_CLUSTER / node
        assert node_dir.is_dir(), f"Expected directory {node_dir} is missing."


def test_files_present_with_expected_md5():
    """Verify that every file exists and matches its expected on-disk MD5."""
    for path, expected_md5 in FILE_EXPECTATIONS.items():
        assert path.is_file(), f"Expected file {path} is missing."
        actual_md5 = md5sum(path)
        assert (
            actual_md5 == expected_md5
        ), f"File {path} MD5 mismatch: expected {expected_md5}, got {actual_md5}"


def test_manifest_exists_and_content_is_correct():
    """Validate that the shipping manifest exists and is byte-for-byte correct (ignoring trailing newlines)."""
    assert MANIFEST_FILE.is_file(), f"Manifest file {MANIFEST_FILE} is missing."

    with MANIFEST_FILE.open("r", encoding="utf-8") as fp:
        lines = [ln.rstrip("\n") for ln in fp.readlines()]

    assert (
        lines == MANIFEST_EXPECTED_LINES
    ), (
        "Manifest content does not match the expected reference.\n"
        "Expected (line-by-line, order matters):\n"
        f"{MANIFEST_EXPECTED_LINES}\n"
        "Found:\n"
        f"{lines}"
    )


def test_no_integrity_report_preexists():
    """Ensure that the integrity_reports directory or report file does not yet exist."""
    assert (
        not INTEGRITY_REPORTS_DIR.exists()
    ), f"Directory {INTEGRITY_REPORTS_DIR} should NOT exist before the exercise starts."
    assert (
        not REPORT_FILE.exists()
    ), f"Report file {REPORT_FILE} should NOT exist before the exercise starts."


# -----------------------------------------------------------------------------#
# End of test_initial_state.py