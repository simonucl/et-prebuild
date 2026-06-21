# test_initial_state.py
#
# Pytest suite that validates the VM *before* the student performs any
# backup-related actions.  It asserts that the “infrastructure” tree is in
# place and that *nothing* backup-related exists yet.

import os
import stat
from pathlib import Path
import pytest

HOME = Path("/home/user")

INFRA_ROOT = HOME / "infrastructure"
BACKUP_ROOT = HOME / "backup_archives"

EXPECTED_DIRS = [
    INFRA_ROOT,
    INFRA_ROOT / "configs",
    INFRA_ROOT / "scripts",
    INFRA_ROOT / "tmp",
]

EXPECTED_FILES = [
    INFRA_ROOT / "configs" / "app.conf",
    INFRA_ROOT / "configs" / "db.conf",
    INFRA_ROOT / "scripts" / "deploy.sh",
    INFRA_ROOT / "tmp"    / "cache.tmp",
]


def _mode_to_str(mode: int) -> str:
    """Return a string such as 0755 for a stat.st_mode value."""
    return oct(mode & 0o777)


@pytest.mark.parametrize("directory", EXPECTED_DIRS)
def test_required_directories_exist_with_reasonable_permissions(directory: Path):
    assert directory.exists(), f"Missing directory: {directory}"
    assert directory.is_dir(), f"{directory} is expected to be a directory"

    # Check that the directory is at least world-readable (0755 or looser).
    mode = directory.stat().st_mode
    assert mode & stat.S_IROTH, f"{directory} should be world-readable (current mode {_mode_to_str(mode)})"


@pytest.mark.parametrize("filepath", EXPECTED_FILES)
def test_required_files_exist_and_are_regular(filepath: Path):
    assert filepath.exists(), f"Missing file: {filepath}"
    assert filepath.is_file(), f"{filepath} exists but is not a regular file"

    # Basic sanity: file should not be empty
    size = filepath.stat().st_size
    assert size > 0, f"{filepath} is unexpectedly empty (0 bytes)"


def test_no_unexpected_files_in_infrastructure():
    """The infrastructure folder should contain exactly the expected files plus directories."""
    found_regular_files = [p for p in INFRA_ROOT.rglob("*") if p.is_file()]
    expected_set = set(EXPECTED_FILES)
    extra_files = [p for p in found_regular_files if p not in expected_set]
    missing_files = [p for p in expected_set if p not in found_regular_files]

    assert not missing_files, f"Missing expected files: {missing_files}"
    assert not extra_files, (
        "There are unexpected files under /home/user/infrastructure that the "
        f"task description did not mention: {extra_files}"
    )


def test_backup_archives_directory_does_not_exist_yet():
    """Before the student starts, /home/user/backup_archives should not exist (or be empty)."""
    if not BACKUP_ROOT.exists():
        # Ideal case: directory absent.
        return

    # If it does exist for some reason, it must be completely empty.
    assert BACKUP_ROOT.is_dir(), f"{BACKUP_ROOT} exists but is not a directory"
    contents = list(BACKUP_ROOT.iterdir())
    assert not contents, (
        f"{BACKUP_ROOT} already exists and is expected to be empty before the task starts; "
        f"found: {contents}"
    )