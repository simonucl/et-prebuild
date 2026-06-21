# test_initial_state.py
#
# This test-suite validates the *initial* operating-system / filesystem
# state **before** the student carries out any actions.  It ensures that
# all prerequisite files and directories exist and contain the expected
# data.  No tests are performed on the *output* files that the student is
# asked to create or modify.

import os
import stat
import hashlib
import pytest
from pathlib import Path

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
ALERTS_DIR = HOME / "alerts"
CONFIG_FILE = DATA_DIR / "critical_config.cfg"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _mode(path: Path) -> int:
    """Return the permission bits (e.g. 0o644) of a file or directory."""
    return stat.S_IMODE(path.stat().st_mode)

def _file_sha256(path: Path) -> str:
    """Return the hexadecimal SHA-256 digest of a file's contents."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# Expected file content, line-by-line (each must end with '\n')
EXPECTED_LINES = [
    "DB_HOST=localhost\n",
    "DB_PORT=5432\n",
    "DB_USER=monitor\n",
    "DB_PASS=monitor123\n",
]

EXPECTED_CONTENT = "".join(EXPECTED_LINES)
EXPECTED_DIGEST = hashlib.sha256(EXPECTED_CONTENT.encode()).hexdigest()

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_data_directory_exists_and_has_correct_perms():
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."
    expected_mode = 0o755
    actual_mode = _mode(DATA_DIR)
    assert actual_mode == expected_mode, (
        f"{DATA_DIR} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}"
    )

def test_alerts_directory_exists_and_has_correct_perms():
    assert ALERTS_DIR.exists(), f"Required directory {ALERTS_DIR} is missing."
    assert ALERTS_DIR.is_dir(), f"{ALERTS_DIR} exists but is not a directory."
    expected_mode = 0o755
    actual_mode = _mode(ALERTS_DIR)
    assert actual_mode == expected_mode, (
        f"{ALERTS_DIR} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}"
    )

def test_critical_config_file_exists_permissions_and_content():
    # Existence and type
    assert CONFIG_FILE.exists(), f"Required file {CONFIG_FILE} is missing."
    assert CONFIG_FILE.is_file(), f"{CONFIG_FILE} exists but is not a regular file."

    # Permissions
    expected_mode = 0o644
    actual_mode = _mode(CONFIG_FILE)
    assert actual_mode == expected_mode, (
        f"{CONFIG_FILE} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}"
    )

    # Content
    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_CONTENT, (
        f"{CONFIG_FILE} content is not exactly as expected.\n"
        f"Expected:\n{EXPECTED_CONTENT!r}\nGot:\n{content!r}"
    )

def test_critical_config_file_sha256_digest_matches_expected():
    actual_digest = _file_sha256(CONFIG_FILE)
    assert actual_digest == EXPECTED_DIGEST, (
        f"SHA-256 digest mismatch for {CONFIG_FILE}.\n"
        f"Expected: {EXPECTED_DIGEST}\nGot     : {actual_digest}"
    )