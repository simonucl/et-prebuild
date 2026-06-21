# test_initial_state.py
# -*- coding: utf-8 -*-
#
# Pytest suite that verifies the filesystem *before* the student begins the
# “disaster-recovery” exercise.  These tests must pass only for the pristine,
# unmodified environment created by the grader.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
BACKUP_DIR = PROJECT_DIR / "data_backup" / "20230115"
LINK_DIR = PROJECT_DIR / "data_links"
RESTORE_LOG_DIR = HOME / "restore_logs"
RESTORE_LOG = RESTORE_LOG_DIR / "restore_20230115.log"

BACKUP_FILES = {
    "report.txt": "Quarterly report – 2022 Q4\n",
    "stats.csv": "year,quarter,revenue\n2022,4,12345\n",
    "image.png": "PNGDATA\n",
}

OLD_BACKUP_BASE = HOME / "old_backups"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _assert_is_regular_file(path: Path, *, msg: str = "") -> None:
    assert path.is_file(), msg or f"Expected regular file at {path!s}."


def _assert_is_symlink(path: Path, *, msg: str = "") -> None:
    assert path.is_symlink(), msg or f"Expected symlink at {path!s}."


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_required_directories_exist():
    """
    Verify that the main directory skeleton is in place.
    """
    for directory in (PROJECT_DIR, BACKUP_DIR, LINK_DIR):
        assert directory.is_dir(), f"Missing directory: {directory!s}"


@pytest.mark.parametrize("filename,expected_content", BACKUP_FILES.items())
def test_backup_files_exist_and_content_intact(filename, expected_content):
    """
    The three validated backup files must be present, readable,
    and byte-for-byte identical to the reference content.
    """
    fpath = BACKUP_DIR / filename
    _assert_is_regular_file(fpath)

    with fpath.open("r", encoding="utf-8") as fh:
        data = fh.read()
    assert data == expected_content, (
        f"Content of {fpath!s} differs from the canonical data. "
        "Do not modify these files."
    )

    # Permissions: must be world-readable; anything 644…666 is fine.
    st_mode = fpath.stat().st_mode
    perm = stat.S_IMODE(st_mode)
    assert perm & stat.S_IROTH, f"{fpath!s} is not world-readable."


@pytest.mark.parametrize("filename", BACKUP_FILES.keys())
def test_broken_symlinks_point_to_old_backups(filename):
    """
    Each link in data_links/ must currently be a *broken* symlink that points
    somewhere under /home/user/old_backups/.
    """
    link_path = LINK_DIR / filename
    _assert_is_symlink(link_path)

    # The symlink should resolve (without following) to the old-backups path.
    target = os.readlink(link_path)
    assert str(target).startswith(str(OLD_BACKUP_BASE)), (
        f"{link_path!s} does not point to the expected old_backups directory "
        f"(got {target!r})."
    )

    # The link must be broken: its resolved absolute path must NOT exist.
    resolved = (link_path.parent / target).resolve()
    assert not resolved.exists(), (
        f"{link_path!s} is expected to be a broken link, but "
        f"{resolved!s} unexpectedly exists."
    )


def test_restore_log_absent():
    """
    Before the student starts, no restore_logs/ directory or log file should exist.
    """
    assert not RESTORE_LOG.exists(), (
        "restore_20230115.log already exists. The exercise should start "
        "with no such file."
    )
    if RESTORE_LOG_DIR.exists():
        # Directory may or may not be present; if it is, it must be empty.
        unexpected = [p for p in RESTORE_LOG_DIR.iterdir() if p.name != RESTORE_LOG.name]
        assert not unexpected, (
            f"Unexpected files found in {RESTORE_LOG_DIR!s}: "
            f"{', '.join(p.name for p in unexpected)}"
        )