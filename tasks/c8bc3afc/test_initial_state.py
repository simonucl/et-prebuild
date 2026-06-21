# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating system
# before the student performs any actions required by the assignment.
#
# The checks performed here assert that:
#   • The staging directory (/home/user/hardening) already exists and contains
#     exactly the three expected files.
#   • No artefacts that the student is supposed to create (archives,
#     recovery_test directory, operation_logs directory or the log/archive
#     files themselves) are present yet.
#
# Only Python's standard library and pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")

HARDENING_DIR = HOME / "hardening"
ARCHIVES_DIR = HOME / "archives"
RECOVERY_DIR = HOME / "recovery_test"
LOGS_DIR = HOME / "operation_logs"

ARCHIVE_FILE = ARCHIVES_DIR / "hardening_backup_2024Q2.tar.gz"
LOG_FILE = LOGS_DIR / "backup_audit.log"

EXPECTED_HARDENING_FILES = {
    HARDENING_DIR / "sysctl_hardened.conf",
    HARDENING_DIR / "sshd_hardened.conf",
    HARDENING_DIR / "pam_hardened.conf",
}


def _read_text_snippet(path: Path, max_chars: int = 200) -> str:
    """
    Read up to max_chars from a text file for use in assertion
    messages.  Falls back to empty string on any exception.
    """
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fp:
            return fp.read(max_chars)
    except Exception:
        return ""


def test_hardening_directory_exists_and_has_correct_files():
    """Verify /home/user/hardening contains exactly the three expected files."""
    assert HARDENING_DIR.exists(), (
        f"Expected directory {HARDENING_DIR} to exist, but it is missing."
    )
    assert HARDENING_DIR.is_dir(), (
        f"Expected {HARDENING_DIR} to be a directory, but it's not."
    )

    # Collect all *regular files* directly inside /home/user/hardening
    actual_files = {p for p in HARDENING_DIR.iterdir() if p.is_file()}

    missing = EXPECTED_HARDENING_FILES - actual_files
    unexpected = actual_files - EXPECTED_HARDENING_FILES

    assert not missing, (
        f"The following expected file(s) are missing from {HARDENING_DIR}: "
        f"{', '.join(str(p) for p in missing)}"
    )
    assert not unexpected, (
        f"The following unexpected file(s) are present in {HARDENING_DIR}: "
        f"{', '.join(str(p) for p in unexpected)}"
    )

    # Ensure each expected file is non-empty text
    for file_path in EXPECTED_HARDENING_FILES:
        size = file_path.stat().st_size
        assert size > 0, f"File {file_path} should not be empty."
        snippet = _read_text_snippet(file_path)
        assert snippet.strip(), f"File {file_path} appears to be empty or binary."


@pytest.mark.parametrize(
    "path",
    [
        ARCHIVES_DIR,
        RECOVERY_DIR,
        LOGS_DIR,
    ],
)
def test_directories_not_yet_created(path: Path):
    """
    The directories that the student must create (archives, recovery_test,
    operation_logs) must *not* exist at the start.
    """
    assert not path.exists(), (
        f"The directory {path} already exists, but it should not be present "
        "before the student performs the assignment."
    )


@pytest.mark.parametrize(
    "file_path",
    [
        ARCHIVE_FILE,
        LOG_FILE,
    ],
)
def test_files_not_yet_created(file_path: Path):
    """
    The archive and log files that the student must create must *not* exist
    at the start.
    """
    assert not file_path.exists(), (
        f"The file {file_path} already exists, but it should not be present "
        "before the student performs the assignment."
    )