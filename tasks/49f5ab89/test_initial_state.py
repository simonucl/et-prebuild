# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system state for the
“deployment script” exercise **before** the student starts working.

The checks are based strictly on the specification that the automated
test harness guarantees to set up.  Any deviation indicates that the
environment is incorrect *before* the student’s solution is run.
"""

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
BASE = HOME / "deployment"

CONFIG_DIR = BASE / "config"
CURRENT_DIR = CONFIG_DIR / "current"
NEW_DIR = CONFIG_DIR / "new"
LOGS_DIR = BASE / "logs"
SCRIPTS_DIR = BASE / "scripts"

CURRENT_FILES = {
    CURRENT_DIR / "app.conf": "version=1.0\n",
    CURRENT_DIR / "db.conf": "version=1.0\n",
    CURRENT_DIR / "cache.conf": "version=1.0\n",
}

NEW_FILES = {
    NEW_DIR / "app.conf": "version=2.0\n",
    NEW_DIR / "db.conf": "version=2.0\n",
    NEW_DIR / "cache.conf": "version=2.0\n",
}


@pytest.mark.parametrize("path", [BASE, CONFIG_DIR, CURRENT_DIR, NEW_DIR, LOGS_DIR, SCRIPTS_DIR])
def test_required_directories_exist(path: Path):
    assert path.is_dir(), f"Expected directory {path} to exist."


@pytest.mark.parametrize("file_path,expected_content", CURRENT_FILES.items())
def test_current_conf_files_exist_and_content(file_path: Path, expected_content: str):
    assert file_path.is_file(), f"Expected current config file {file_path} to exist."
    data = file_path.read_text(encoding="utf-8")
    assert data == expected_content, (
        f"{file_path} should contain exactly {expected_content!r} "
        f"but contains {data!r}"
    )


@pytest.mark.parametrize("file_path,expected_content", NEW_FILES.items())
def test_new_conf_files_exist_and_content(file_path: Path, expected_content: str):
    assert file_path.is_file(), f"Expected new config file {file_path} to exist."
    data = file_path.read_text(encoding="utf-8")
    assert data == expected_content, (
        f"{file_path} should contain exactly {expected_content!r} "
        f"but contains {data!r}"
    )


def test_no_backup_files_yet():
    """No *.bak files should exist in the current/ directory yet."""
    bak_files = list(CURRENT_DIR.glob("*.bak*"))
    assert not bak_files, (
        f"Found unexpected backup files in {CURRENT_DIR}: {', '.join(map(str, bak_files))}"
    )


def test_log_file_absent():
    log_file = LOGS_DIR / "update.log"
    assert not log_file.exists(), f"{log_file} should not exist before the script is run."


def test_scripts_directory_empty_and_script_absent():
    """scripts/ exists but contains no update_configs.sh yet."""
    script_file = SCRIPTS_DIR / "update_configs.sh"
    assert not script_file.exists(), (
        f"{script_file} should not exist before the student creates it."
    )

    # If any files exist in scripts/, list them for diagnostic purposes.
    remaining = [p.name for p in SCRIPTS_DIR.iterdir()]
    assert remaining == [], f"The scripts directory should be empty, found: {remaining}"