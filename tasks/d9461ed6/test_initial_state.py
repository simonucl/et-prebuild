# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state required by the “configuration-file audit” assignment.
#
# IMPORTANT: These tests ONLY verify what must already exist **before**
# the student issues their one-liner `find | xargs` pipeline.  They do **not**
# check for any artifacts that should be produced by the student (e.g.
# /home/user/audit/config_line_report.txt).

import os
import stat
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# General constants used by several tests
# ---------------------------------------------------------------------------

HOME = Path("/home/user").expanduser().resolve()
BACKUP_ROOT = HOME / "config_backups"
AUDIT_DIR = HOME / "audit"

# Expected set of .conf files (absolute paths) and their line counts.
EXPECTED_CONF_FILES = {
    BACKUP_ROOT / "sshd.conf": 5,
    BACKUP_ROOT / "nginx.conf": 9,
    BACKUP_ROOT / "app.conf": 4,
    BACKUP_ROOT / "old" / "legacy.conf": 3,
}

# A non-.conf file that must also pre-exist (should be ignored by the task).
EXPECTED_MISC_FILE = BACKUP_ROOT / "readme.txt"
EXPECTED_MISC_LINES = 2


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _is_writable_dir(path: Path) -> bool:
    """
    Return True if *path* exists, is a directory and is writable
    by the current process.
    """
    return (
        path.exists()
        and path.is_dir()
        and os.access(str(path), os.W_OK)
    )


def _count_text_lines(path: Path) -> int:
    """
    Return the number of text lines (split by universal newlines)
    in the file located at *path*.
    """
    with path.open("r", encoding="utf-8") as fh:
        # str.splitlines() avoids counting an extra blank line
        # if the file happens to end with a trailing newline.
        return len(fh.read().splitlines())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_backup_root_directory_exists_and_is_directory():
    assert BACKUP_ROOT.exists(), (
        f"Required directory {BACKUP_ROOT} is missing."
    )
    assert BACKUP_ROOT.is_dir(), (
        f"{BACKUP_ROOT} exists but is not a directory."
    )


def test_audit_directory_exists_and_is_writable():
    assert AUDIT_DIR.exists(), (
        f"Required directory {AUDIT_DIR} is missing."
    )
    assert AUDIT_DIR.is_dir(), (
        f"{AUDIT_DIR} exists but is not a directory."
    )
    assert _is_writable_dir(AUDIT_DIR), (
        f"Directory {AUDIT_DIR} is not writable by the current user."
    )


@pytest.mark.parametrize("file_path,line_count", EXPECTED_CONF_FILES.items())
def test_expected_conf_files_exist_with_correct_line_counts(file_path: Path, line_count: int):
    assert file_path.exists(), (
        f"Configuration file {file_path} is missing."
    )
    assert file_path.is_file(), (
        f"{file_path} exists but is not a regular file."
    )
    actual = _count_text_lines(file_path)
    assert actual == line_count, (
        f"{file_path} should contain {line_count} lines but actually has {actual}."
    )


def test_misc_readme_file_exists_and_has_expected_content():
    path = EXPECTED_MISC_FILE
    assert path.exists(), f"Miscellaneous file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."
    actual = _count_text_lines(path)
    assert actual == EXPECTED_MISC_LINES, (
        f"{path} should contain {EXPECTED_MISC_LINES} lines but actually has {actual}."
    )


def test_no_extra_conf_files_are_present():
    """
    Ensure there are no unexpected *.conf files under /home/user/config_backups/.
    The assignment relies on exactly the four known configuration files.
    """
    discovered = {
        p.resolve()
        for p in BACKUP_ROOT.rglob("*.conf")
        if p.is_file()
    }
    expected = set(EXPECTED_CONF_FILES.keys())
    missing = expected - discovered
    extra = discovered - expected

    assert not missing, (
        f"The following expected .conf files are missing: {', '.join(map(str, missing))}"
    )
    assert not extra, (
        "Unexpected .conf files found (the initial state must not contain these): "
        f"{', '.join(map(str, extra))}"
    )


def test_old_subdirectory_exists():
    old_dir = BACKUP_ROOT / "old"
    assert old_dir.exists(), f"Sub-directory {old_dir} is missing."
    assert old_dir.is_dir(), f"{old_dir} exists but is not a directory."