# test_initial_state.py
"""
Pytest suite to verify the **initial** filesystem state before the student
creates the symbolic link and verification file.

Expected initial state
----------------------
1.  Directory     : /home/user/logs                         (must exist)
2.  Files         : /home/user/logs/uptime_2023-09-14_13-45-00.log  (must exist)
                    /home/user/logs/uptime_2023-09-15_13-45-00.log  (must exist)
3.  Must _NOT_ exist yet:
        /home/user/uptime_latest.log        (no file/symlink of any kind)
        /home/user/uptime_link_check.txt    (no file/symlink of any kind)

The tests below enforce that starting point so that any subsequent actions
performed by the student can be reliably validated.
"""

from pathlib import Path
import os
import stat
import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"

FILE_14 = LOG_DIR / "uptime_2023-09-14_13-45-00.log"
FILE_15 = LOG_DIR / "uptime_2023-09-15_13-45-00.log"

SYMLINK_LATEST = HOME / "uptime_latest.log"
VERIFICATION_FILE = HOME / "uptime_link_check.txt"


def _is_symlink(path: Path) -> bool:
    """
    Return True only if the given path exists and is a symbolic link.
    """
    try:
        return path.exists() and path.lstat().st_mode & stat.S_IFMT(path.lstat().st_mode) == stat.S_IFLNK
    except FileNotFoundError:
        return False


def test_logs_directory_exists():
    assert LOG_DIR.exists(), f"Required directory missing: {LOG_DIR}"
    assert LOG_DIR.is_dir(), f"Expected {LOG_DIR} to be a directory."


@pytest.mark.parametrize(
    "path",
    [FILE_14, FILE_15],
    ids=["uptime log 2023-09-14", "uptime log 2023-09-15"],
)
def test_required_log_files_exist(path: Path):
    assert path.exists(), f"Required log file missing: {path}"
    assert path.is_file(), f"Expected {path} to be a regular file."


@pytest.mark.parametrize(
    "path, description",
    [
        (SYMLINK_LATEST, "symbolic link /home/user/uptime_latest.log"),
        (VERIFICATION_FILE, "verification file /home/user/uptime_link_check.txt"),
    ],
)
def test_artifacts_do_not_preexist(path: Path, description: str):
    """
    Ensure the artifacts the student will create do NOT exist yet.
    They should neither be files nor symlinks nor directories.
    """
    assert not path.exists(), f"{description} already exists but should NOT be present before the task starts."
    # If the entry somehow exists as a broken symlink, lstat() succeeds but exists() is False.
    # Therefore also check lstat() via os.path.lexists() to catch that edge-case.
    assert not os.path.lexists(path), f"{description} exists (possibly as a broken symlink) but should NOT be present."


def test_latest_symlink_is_not_accidentally_present():
    """
    Explicitly guard against the corner-case where a dangling or
    mis-pointed symlink already exists.
    """
    assert not _is_symlink(SYMLINK_LATEST), (
        f"{SYMLINK_LATEST} is already a symbolic link, but the task "
        "requires creating it anew, so it must not be present initially."
    )