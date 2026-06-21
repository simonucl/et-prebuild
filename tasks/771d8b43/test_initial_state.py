# test_initial_state.py
# Pytest suite to assert the *initial* filesystem / OS state
# BEFORE the student carries out the assignment.
#
# Rules:
#   • Nothing belonging to the cmtracker project should exist yet.
#   • The sqlite3 CLI utility must be available in PATH.
#
# Any failure means the workspace is not clean and will give the
# student misleading feedback once they start working.

import os
import shutil
import subprocess
from pathlib import Path

import pytest

# ---------- Constants ---------- #
HOME = Path("/home/user")
CMTRACKER_ROOT = HOME / "cmtracker"

# Directories that *must not* exist yet
ALL_DIRS = [
    CMTRACKER_ROOT,
    CMTRACKER_ROOT / "configs",
    CMTRACKER_ROOT / "db",
    CMTRACKER_ROOT / "reports",
    CMTRACKER_ROOT / "logs",
]

# Files that *must not* exist yet
ALL_FILES = [
    CMTRACKER_ROOT / "configs" / "ssh.cfg",
    CMTRACKER_ROOT / "configs" / "nginx.conf",
    CMTRACKER_ROOT / "configs" / "app.ini",
    CMTRACKER_ROOT / "db" / "config_changes.db",
    CMTRACKER_ROOT / "reports" / "changes_report.txt",
    CMTRACKER_ROOT / "logs" / "db_commands.log",
]


# ---------- Helpers ---------- #
def _exists(path: Path) -> bool:
    """
    Cross-platform helper to check for existence of a file system object.
    Using os.path.exists directly would be fine, but Path provides clearer
    semantics and types.
    """
    return path.exists()


# ---------- Tests ---------- #
def test_home_directory_exists():
    """Sanity-check that the base /home/user directory itself is present."""
    assert HOME.exists(), f"Expected home directory {HOME} to exist."


@pytest.mark.parametrize("dpath", ALL_DIRS)
def test_cmtracker_directories_do_not_exist_yet(dpath: Path):
    """
    No project-specific directories should pre-exist. Their presence would
    suggest that a previous attempt (or cached artefacts) pollute the
    clean slate required by the assignment.
    """
    assert not _exists(
        dpath
    ), f"Directory {dpath} should NOT exist prior to the student's actions."


@pytest.mark.parametrize("fpath", ALL_FILES)
def test_cmtracker_files_do_not_exist_yet(fpath: Path):
    """
    Likewise, none of the target files should be around beforehand.
    """
    assert not _exists(
        fpath
    ), f"File {fpath} should NOT exist prior to the student's actions."


def test_sqlite3_cli_is_available():
    """
    The assignment mandates using only the standard SQLite CLI (sqlite3).
    Verify that invoking `which sqlite3` or running `sqlite3 -version`
    succeeds so the student can rely on it.
    """
    # shutil.which is the most portable way in stdlib
    sqlite_path = shutil.which("sqlite3")
    assert sqlite_path, "sqlite3 CLI utility is not found in PATH."

    # Extra sanity check: ensure it runs without crashing
    try:
        completed = subprocess.run(
            ["sqlite3", "-version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        pytest.fail(f"sqlite3 CLI is installed but not executable: {exc}")

    assert (
        completed.stdout.strip() or completed.stderr.strip()
    ), "sqlite3 executed but produced no output; installation might be broken."