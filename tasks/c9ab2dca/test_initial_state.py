# test_initial_state.py
#
# Pytest suite that verifies the starting state of the filesystem
# BEFORE the student begins the restore exercise.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user").resolve()

BACKUP_ROOT = HOME / "backup_repo" / "daily_backups"
RESTORE_ROOT = HOME / "restore_test"

# ----------------------------------------------------------------------
# 1. Verify that all expected *.bak files exist and have exact contents
# ----------------------------------------------------------------------

EXPECTED_BAK_FILES = [
    (
        BACKUP_ROOT
        / "2023-07-14"
        / "files"
        / "config1.cfg.bak",
        "server=alpha\nport=8080\n",
    ),
    (
        BACKUP_ROOT
        / "2023-07-14"
        / "files"
        / "data1.sql.bak",
        "CREATE TABLE test1 (id INTEGER);\n",
    ),
    (
        BACKUP_ROOT
        / "2023-07-14"
        / "files"
        / "notes.txt.bak",
        "Backup note for July 14\n",
    ),
    (
        BACKUP_ROOT
        / "2023-07-15"
        / "files"
        / "config2.cfg.bak",
        "server=beta\nport=9090\n",
    ),
    (
        BACKUP_ROOT
        / "2023-07-15"
        / "files"
        / "data2.sql.bak",
        "CREATE TABLE test2 (id INTEGER);\n",
    ),
]

# ----------------------------------------------------------------------
# 2. Verify that non-backup “extra” files exist (content not inspected)
# ----------------------------------------------------------------------

NON_BAK_FILES = [
    BACKUP_ROOT / "2023-07-14" / "files" / "random.tmp",
    BACKUP_ROOT / "2023-07-15" / "files" / "readme.md",
]

# ----------------------------------------------------------------------
# 3. Paths that MUST NOT exist before the student runs the solution
# ----------------------------------------------------------------------

UNEXPECTED_OUTPUT_PATHS = [
    RESTORE_ROOT / "restored",  # directory that will be created later
    RESTORE_ROOT / "restore_report.log",  # report file generated later
]


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _read_text_exact(path: Path) -> str:
    """
    Read text from *path* using UTF-8 without newline translation so that the
    exact byte sequence can be compared.  Fails if file is unreadable.
    """
    with path.open("r", encoding="utf-8", newline="") as fp:
        return fp.read()


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize("path, expected_content", EXPECTED_BAK_FILES)
def test_expected_bak_files_present_with_correct_content(path: Path, expected_content: str):
    assert path.is_file(), (
        f"Required backup file is missing: {path}"
    )
    actual = _read_text_exact(path)
    assert actual == expected_content, (
        f"Content mismatch for {path}\n"
        f"Expected:\n{expected_content!r}\n"
        f"Got:\n{actual!r}"
    )


@pytest.mark.parametrize("path", NON_BAK_FILES)
def test_non_bak_files_present(path: Path):
    assert path.is_file(), (
        f"Required non-backup file is missing: {path}"
    )


def test_restore_test_directory_exists_and_is_empty():
    assert RESTORE_ROOT.is_dir(), (
        f"Directory {RESTORE_ROOT} is expected to exist and be empty."
    )
    contents = [p for p in RESTORE_ROOT.iterdir()]
    assert contents == [], (
        f"{RESTORE_ROOT} is expected to be empty before the exercise starts, "
        f"but contains: {', '.join(str(p) for p in contents)}"
    )


@pytest.mark.parametrize("path", UNEXPECTED_OUTPUT_PATHS)
def test_no_output_files_or_directories_exist_yet(path: Path):
    assert not path.exists(), (
        f"Output path {path} should NOT exist before the restore task begins."
    )


def test_backup_directory_structure_complete():
    """
    Sanity-check that the backup directory tree itself exists so that
    downstream tests have a solid foundation.
    """
    for subdir in ["2023-07-14", "2023-07-15"]:
        dir_path = BACKUP_ROOT / subdir / "files"
        assert dir_path.is_dir(), f"Expected directory is missing: {dir_path}"