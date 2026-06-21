# test_initial_state.py
#
# This pytest suite validates that the **starting** filesystem state for the
# “secure_app” rotation exercise is correct.  It deliberately fails if any of
# the *post-rotation* artefacts already exist or if the vulnerable file is not
# in its expected world-readable form.

import os
import stat
from pathlib import Path

SECURE_APP_DIR = Path("/home/user/secure_app")
CONFIG_FILE    = SECURE_APP_DIR / "config.ini"
BACKUP_FILE    = SECURE_APP_DIR / "config.ini.bak"
ROT_LOG_FILE   = SECURE_APP_DIR / "rotation.log"

EXPECTED_CONFIG_CONTENT = "[credentials]\nAPI_KEY = OLDKEY-12345\n"
EXPECTED_DIR_MODE       = 0o755   # rwxr-xr-x
EXPECTED_CONFIG_MODE    = 0o644   # rw-r--r--

def _mode(path: Path) -> int:
    """Return permission bits (e.g., 0o644) for a filesystem object."""
    return stat.S_IMODE(path.stat().st_mode)

def test_secure_app_directory_exists_and_mode():
    assert SECURE_APP_DIR.exists(), f"Directory {SECURE_APP_DIR} is missing."
    assert SECURE_APP_DIR.is_dir(), f"{SECURE_APP_DIR} exists but is not a directory."
    actual_mode = _mode(SECURE_APP_DIR)
    assert actual_mode == EXPECTED_DIR_MODE, (
        f"{SECURE_APP_DIR} has mode {oct(actual_mode)}, expected {oct(EXPECTED_DIR_MODE)}."
    )

def test_config_ini_exists_mode_and_content():
    assert CONFIG_FILE.exists(), f"Config file {CONFIG_FILE} is missing."
    assert CONFIG_FILE.is_file(), f"{CONFIG_FILE} exists but is not a regular file."
    actual_mode = _mode(CONFIG_FILE)
    assert actual_mode == EXPECTED_CONFIG_MODE, (
        f"{CONFIG_FILE} has mode {oct(actual_mode)}, expected {oct(EXPECTED_CONFIG_MODE)}."
    )
    content = CONFIG_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_CONFIG_CONTENT, (
        f"{CONFIG_FILE} content mismatch.\nExpected:\n{EXPECTED_CONFIG_CONTENT!r}\nFound:\n{content!r}"
    )

def test_backup_file_should_not_exist_yet():
    assert not BACKUP_FILE.exists(), (
        f"Backup file {BACKUP_FILE} should NOT exist before rotation begins."
    )

def test_rotation_log_should_not_exist_yet():
    assert not ROT_LOG_FILE.exists(), (
        f"Rotation log {ROT_LOG_FILE} should NOT exist before rotation begins."
    )