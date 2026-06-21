# test_initial_state.py
#
# Pytest suite to verify the **initial** state of the operating system
# before the student performs the backup-and-symlink task.
#
# IMPORTANT:  These tests assert that the starting filesystem matches the
# task description.  If any test here fails, the grading environment is
# mis-configured (or the student has modified the state **before** running
# the tests).

from pathlib import Path
import glob
import pytest


# --------------------------------------------------------------------------- #
# Constants describing the expected initial state
# --------------------------------------------------------------------------- #

# Home directory root
HOME = Path("/home/user")

# Backup directory that must NOT exist yet
BACKUP_DIR = HOME / "backups" / "2024-05-30"
MANIFEST_PATH = BACKUP_DIR / "backup_manifest.log"
SUMMARY_PATH = BACKUP_DIR / "summary.txt"

# Expected *.log files that must be moved later
EXPECTED_LOG_FILES = {
    HOME / "data" / "projectA" / "server.log": "server-log-A-1\nserver-log-A-2\n",
    HOME / "data" / "projectA" / "error.log":  "error-A-1\n",
    HOME / "data" / "projectB" / "access.log": "access-B-entry\n",
    HOME / "data" / "projectB" / "debug.log":  "debug-B-trace\n",
    HOME / "data" / "projectC" / "app.log":    "app-C-start\n",
}

# Non-log files that must remain untouched
EXPECTED_NON_LOG_FILES = {
    HOME / "data" / "projectA" / "readme.txt":  "README A\n",
    HOME / "data" / "projectB" / "config.yml":  "setting: B\n",
    HOME / "data" / "projectC" / "notes.md":    "Notes C\n",
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def read_text(path: Path) -> str:
    """
    Read the entire text content of *path* using UTF-8.
    The helper centralises the encoding choice and error handling.
    """
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_backup_directory_does_not_exist_yet():
    """
    The target backup directory MUST NOT exist before the student runs
    their solution.  (It's their job to create it.)
    """
    assert not BACKUP_DIR.exists(), (
        f"Expected backup directory {BACKUP_DIR} to NOT exist yet, "
        "but it is already present."
    )
    # Even if the parent /home/user/backups exists, the date-stamped
    # sub-directory must be absent.


def test_log_files_exist_and_are_regular_files():
    """
    All expected *.log files must exist, be **regular files**, and must
    NOT already be symbolic links.
    """
    for path, _content in EXPECTED_LOG_FILES.items():
        assert path.exists(), f"Expected log file {path} is missing."
        assert path.is_file(), f"Expected {path} to be a regular file."
        assert not path.is_symlink(), f"{path} should NOT be a symlink yet."


def test_no_additional_log_files_present():
    """
    Exactly the five *.log files listed in EXPECTED_LOG_FILES must be
    present under /home/user/data/*/*.log.  Having more or fewer would
    violate the declared initial state.
    """
    discovered = {Path(p) for p in glob.glob(str(HOME / "data" / "*" / "*.log"))}
    expected = set(EXPECTED_LOG_FILES.keys())
    missing = expected - discovered
    extra   = discovered - expected
    assert not missing, (
        "The following expected *.log files are missing:\n"
        + "\n".join(str(p) for p in sorted(missing))
    )
    assert not extra, (
        "Found unexpected *.log files that are NOT listed in the initial "
        "specification:\n"
        + "\n".join(str(p) for p in sorted(extra))
    )


def test_log_file_contents_match_specification():
    """
    Verify that each *.log file contains the exact content that the
    initial state promises.
    """
    for path, expected_content in EXPECTED_LOG_FILES.items():
        actual = read_text(path)
        assert actual == expected_content, (
            f"Content mismatch in {path}.\n"
            f"Expected:\n{expected_content!r}\n"
            f"Got:\n{actual!r}"
        )


def test_non_log_files_present_and_intact():
    """
    Non-log files must also exist and remain untouched; their presence
    helps ensure the test fixture was created correctly.
    """
    for path, expected_content in EXPECTED_NON_LOG_FILES.items():
        assert path.exists(), f"Expected file {path} is missing."
        assert path.is_file(), f"Expected {path} to be a regular file."
        actual = read_text(path)
        assert actual == expected_content, (
            f"Content mismatch in {path}. Expected {expected_content!r} "
            f"but got {actual!r}"
        )


def test_manifest_and_summary_do_not_exist_yet():
    """
    Neither the manifest nor the summary file should exist before the
    student runs their solution.
    """
    assert not MANIFEST_PATH.exists(), (
        f"Manifest {MANIFEST_PATH} should NOT exist yet."
    )
    assert not SUMMARY_PATH.exists(), (
        f"Summary file {SUMMARY_PATH} should NOT exist yet."
    )