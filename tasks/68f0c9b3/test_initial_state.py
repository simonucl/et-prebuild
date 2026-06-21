# test_initial_state.py
#
# Pytest suite that validates the pristine operating-system state
# *before* the student writes any code.  These tests confirm that the
# nightly restore data are present and untouched, and that no output
# artefacts have been created yet.

import os
from pathlib import Path

# Constants ------------------------------------------------------------------

RESTORE_DIR = Path("/home/user/restores/2024-06-10")
RESTORE_LOG = RESTORE_DIR / "daily_filelist.log"
BACKUP_REPORTS_DIR = Path("/home/user/backup_reports")

EXPECTED_LINES = [
    "docs/finance/report1.pdf\n",
    "docs/hr/policy.docx\n",
    "media/photos/img001.jpg\n",
    "docs/finance/report1.pdf\n",
    "media/photos/img002.jpg\n",
    "docs/finance/report1.pdf\n",
    "media/photos/img001.jpg\n",
    "docs/hr/policy.docx\n",
    "scripts/backup.sh\n",
    "scripts/backup.sh\n",
    "scripts/backup.sh\n",
    "media/photos/img002.jpg\n",
    "media/photos/img002.jpg\n",
]

EXPECTED_CONTENT = "".join(EXPECTED_LINES)


# Helper ---------------------------------------------------------------------

def read_file(path: Path) -> str:
    with path.open("rb") as fh:
        return fh.read().decode("utf-8", errors="strict")


# Tests ----------------------------------------------------------------------

def test_restore_directory_exists_and_is_correct():
    """
    Ensure /home/user/restores/2024-06-10/ exists, is a directory,
    and contains exactly one file: daily_filelist.log.
    """
    assert RESTORE_DIR.exists(), f"Expected directory {RESTORE_DIR} to exist."
    assert RESTORE_DIR.is_dir(), f"{RESTORE_DIR} exists but is not a directory."

    contents = sorted(p.name for p in RESTORE_DIR.iterdir())
    assert contents == ["daily_filelist.log"], (
        f"{RESTORE_DIR} should contain only "
        "'daily_filelist.log' but instead contains: {contents}"
    )


def test_daily_filelist_log_exists_and_content_is_exact():
    """
    Validate that the log file exists, is a regular file, and its
    byte-for-byte content matches the specification (13 newline-terminated lines,
    no extra blank line).
    """
    assert RESTORE_LOG.exists(), f"Expected file {RESTORE_LOG} to exist."
    assert RESTORE_LOG.is_file(), f"{RESTORE_LOG} exists but is not a regular file."

    actual_content = read_file(RESTORE_LOG)

    # Length check first to provide clear diff if sizes differ.
    assert len(actual_content) == len(EXPECTED_CONTENT), (
        f"{RESTORE_LOG} content length mismatch: "
        f"expected {len(EXPECTED_CONTENT)} bytes, got {len(actual_content)} bytes."
    )

    # Exact byte-for-byte comparison.
    assert actual_content == EXPECTED_CONTENT, (
        f"Content of {RESTORE_LOG} does not match the expected fixture.\n"
        f"--- Expected (first 500 chars) ---\n{EXPECTED_CONTENT[:500]}"
        f"\n--- Actual (first 500 chars) ---\n{actual_content[:500]}"
    )


def test_no_backup_reports_directory_yet():
    """
    The student has not run the reporting step; therefore
    /home/user/backup_reports/ must NOT exist.
    """
    assert not BACKUP_REPORTS_DIR.exists(), (
        f"Directory {BACKUP_REPORTS_DIR} should not exist before the task is run."
    )