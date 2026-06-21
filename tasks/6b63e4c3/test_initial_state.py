# test_initial_state.py
#
# This pytest suite verifies that the starting filesystem is in the **pristine**
# state expected **before** the student runs any command.
#
# Expected initial layout
#
# /home/user/data_pipeline/               (dir,  0o755)
# ├── config.yaml                         (file, 0 bytes, 0o644, empty SHA-256)
# └── logs/                               (dir,  0o755)
#
# The audit file that the assignment asks the student to create
# (/home/user/data_pipeline/logs/config_audit.log) must **NOT** be present yet.
#
# The tests deliberately fail fast with clear, actionable messages if anything
# in the initial state is missing or has been modified.

import hashlib
import os
import stat
import pytest
from pathlib import Path

# Canonical paths used throughout the test suite
DP_ROOT      = Path("/home/user/data_pipeline")
CFG_FILE     = DP_ROOT / "config.yaml"
LOG_DIR      = DP_ROOT / "logs"
AUDIT_FILE   = LOG_DIR / "config_audit.log"

EXPECTED_CFG_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)

def _get_mode_bits(path: Path) -> int:
    """Return the permission bits (e.g. 0o644) for the given path."""
    return stat.S_IMODE(path.stat().st_mode)

@pytest.mark.order(1)
def test_root_directory_exists_and_has_correct_permissions():
    assert DP_ROOT.is_dir(), (
        f"Required directory {DP_ROOT} is missing or not a directory."
    )
    mode = _get_mode_bits(DP_ROOT)
    assert mode == 0o755, (
        f"Directory {DP_ROOT} should have permissions 755; found {oct(mode)}."
    )

@pytest.mark.order(2)
def test_config_yaml_exists_empty_and_correct_permissions():
    assert CFG_FILE.exists(), (
        f"Required file {CFG_FILE} is missing."
    )
    assert CFG_FILE.is_file(), (
        f"{CFG_FILE} exists but is not a regular file."
    )

    size = CFG_FILE.stat().st_size
    assert size == 0, (
        f"{CFG_FILE} should be 0 bytes to begin with; found {size} bytes."
    )

    mode = _get_mode_bits(CFG_FILE)
    assert mode == 0o644, (
        f"{CFG_FILE} permissions should be 644; found {oct(mode)}."
    )

    # Verify SHA-256 of the empty file
    sha256 = hashlib.sha256(CFG_FILE.read_bytes()).hexdigest()
    assert sha256 == EXPECTED_CFG_SHA256, (
        f"{CFG_FILE} digest mismatch.\n"
        f"Expected: {EXPECTED_CFG_SHA256}\nFound:    {sha256}"
    )

@pytest.mark.order(3)
def test_logs_directory_exists_and_has_correct_permissions():
    assert LOG_DIR.exists(), (
        f"Required directory {LOG_DIR} is missing."
    )
    assert LOG_DIR.is_dir(), (
        f"{LOG_DIR} exists but is not a directory."
    )
    mode = _get_mode_bits(LOG_DIR)
    assert mode == 0o755, (
        f"Directory {LOG_DIR} should have permissions 755; found {oct(mode)}."
    )

@pytest.mark.order(4)
def test_audit_log_does_not_exist_yet():
    assert not AUDIT_FILE.exists(), (
        f"{AUDIT_FILE} should NOT exist before the student runs any commands."
    )