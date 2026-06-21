# test_initial_state.py
"""
Pytest suite that validates the PRE-update filesystem state for the
“web-app backup” exercise.

Expected ground truth before the student’s action:
1.  /home/user/deploy/app/ exists and is a directory.
    ├── index.html   … contains the single line:  “Hello World v1”
    └── config.yaml  … contains exactly two lines: “version: 1.0\n”
2.  /home/user/deploy/backups/ exists and is an EMPTY directory.
3.  No pre-existing backup artefacts:
      /home/user/deploy/backups/app_backup.tgz   MUST NOT exist
      /home/user/deploy/backups/backup_log.json  MUST NOT exist
"""

from pathlib import Path
import pytest

HOME = Path("/home/user")
APP_DIR = HOME / "deploy" / "app"
BACKUPS_DIR = HOME / "deploy" / "backups"
ARCHIVE_PATH = BACKUPS_DIR / "app_backup.tgz"
LOG_PATH = BACKUPS_DIR / "backup_log.json"


def test_app_directory_exists():
    """The live application directory must exist and be a directory."""
    assert APP_DIR.is_dir(), (
        f"Required directory {APP_DIR} is missing. "
        "Create it before continuing."
    )


def test_app_directory_contents():
    """
    The application directory must contain exactly the two expected files
    (no more, no less).
    """
    expected = {"index.html", "config.yaml"}
    actual = {p.name for p in APP_DIR.iterdir() if p.is_file()}
    assert actual == expected, (
        f"{APP_DIR} should contain ONLY {sorted(expected)}, "
        f"but actually has {sorted(actual)}."
    )

    # Verify file contents are as specified
    index_path = APP_DIR / "index.html"
    cfg_path = APP_DIR / "config.yaml"

    index_content = index_path.read_text(encoding="utf-8").rstrip("\n")
    cfg_content = cfg_path.read_text(encoding="utf-8")

    assert index_content == "Hello World v1", (
        f"{index_path} must contain exactly 'Hello World v1' "
        f"but contains: {index_content!r}"
    )

    assert cfg_content == "version: 1.0\n", (
        f"{cfg_path} must contain exactly two lines: "
        "'version: 1.0' followed by a newline. "
        f"Found content: {cfg_content!r}"
    )


def test_backups_directory_exists_and_empty():
    """The sibling backups directory must exist and be empty."""
    assert BACKUPS_DIR.is_dir(), (
        f"Backups directory {BACKUPS_DIR} is missing. "
        "Create it before proceeding."
    )

    contents = [p.name for p in BACKUPS_DIR.iterdir()]
    assert contents == [], (
        f"{BACKUPS_DIR} must be empty before the backup runs, "
        f"but it currently contains: {contents}"
    )


def test_no_preexisting_backup_or_log():
    """Ensure no leftover archive or log files exist before the task starts."""
    assert not ARCHIVE_PATH.exists(), (
        f"Unexpected archive file {ARCHIVE_PATH} already exists. "
        "Remove or rename it before creating a fresh backup."
    )
    assert not LOG_PATH.exists(), (
        f"Unexpected log file {LOG_PATH} already exists. "
        "Remove or rename it before creating a fresh log."
    )