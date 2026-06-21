# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student starts working on the “repeatable, timestamped backup
# procedure” task.  These tests assert that the required project files are
# present with the correct contents and that no backup artefacts or
# directories have been created yet.

import os
from pathlib import Path

# ---- Constants ----------------------------------------------------------------

HOME = Path("/home/user")

PROJECT_ROOT   = HOME / "projects" / "portfolio_site"
ASSETS_DIR     = PROJECT_ROOT / "assets"
SCRIPTS_DIR    = PROJECT_ROOT / "scripts"
STYLES_DIR     = PROJECT_ROOT / "styles"

ASSET_LOGO     = ASSETS_DIR   / "logo.png"
ASSET_HERO     = ASSETS_DIR   / "hero.jpg"
SCRIPT_APP     = SCRIPTS_DIR  / "app.js"
STYLE_CSS      = STYLES_DIR   / "style.css"

BACKUPS_DIR    = HOME / "backups"
BACKUP_FILE    = BACKUPS_DIR / "portfolio_site_backup_20240101_120000.tar.gz"

LOGS_DIR       = HOME / "backup_logs"
LOG_FILE       = LOGS_DIR / "portfolio_site_backup_20240101_120000.log"

# Expected raw file contents (exact, including trailing newline chars)
EXPECTED_CONTENTS = {
    ASSET_LOGO: b"PNGLOGO123\n",
    ASSET_HERO: b"JPGHERO123\n",
    SCRIPT_APP: b"console.log('hi');\n",
    STYLE_CSS:  b"body{background:#fff}\n",
}

# Expected byte sizes for each file
EXPECTED_SIZES = {path: len(content) for path, content in EXPECTED_CONTENTS.items()}

# ------------------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------------------

def _assert_file(path: Path, *, size: int, content: bytes) -> None:
    """
    Assert that `path` exists, is a regular file, and matches the provided
    `size` and `content`.
    """
    assert path.exists(), f"Required file missing: {path}"
    assert path.is_file(), f"Expected a regular file at {path} but found something else."
    actual_size = path.stat().st_size
    assert actual_size == size, (
        f"File {path} should be {size} bytes, found {actual_size} bytes."
    )
    actual_content = path.read_bytes()
    assert actual_content == content, (
        f"File {path} has unexpected contents.\n"
        f"Expected: {content!r}\nActual:   {actual_content!r}"
    )

# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------

def test_project_directories_exist_and_are_directories():
    """
    The project directory tree (/home/user/projects/portfolio_site) along with
    assets/, scripts/, and styles/ sub-directories must already exist.
    """
    for d in (PROJECT_ROOT, ASSETS_DIR, SCRIPTS_DIR, STYLES_DIR):
        assert d.exists(), f"Expected directory missing: {d}"
        assert d.is_dir(), f"Expected {d} to be a directory."

def test_project_files_exist_with_correct_sizes_and_contents():
    """
    Every source file must exist at task start with the exact byte content
    stipulated in the task description.
    """
    for path, expected_content in EXPECTED_CONTENTS.items():
        expected_size = EXPECTED_SIZES[path]
        _assert_file(path, size=expected_size, content=expected_content)

def test_backup_and_log_directories_do_not_exist_yet():
    """
    The backup and log root directories must NOT exist before the student
    performs any action.
    """
    assert not BACKUPS_DIR.exists(), f"Backup directory {BACKUPS_DIR} should NOT exist initially."
    assert not LOGS_DIR.exists(),    f"Log directory {LOGS_DIR} should NOT exist initially."

def test_archive_and_log_files_do_not_exist_yet():
    """
    No archive (.tar.gz) or log (.log) files should exist before the student
    runs their backup procedure.
    """
    assert not BACKUP_FILE.exists(), f"Archive file {BACKUP_FILE} should NOT exist initially."
    assert not LOG_FILE.exists(),   f"Log file {LOG_FILE} should NOT exist initially."