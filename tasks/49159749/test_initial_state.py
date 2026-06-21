#!/usr/bin/env python3
# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem **before**
# the student performs the move-operation requested in the task description.
#
# The checks performed are:
# 1. /home/user/staging_rules/            exists and is a directory.
# 2. It contains **exactly one** file named critical_load.rule.
# 3. /home/user/staging_rules/critical_load.rule exists, is a regular file,
#    and its content matches the three lines specified in the task—byte for byte.
# 4. /home/user/monitoring/rules/enabled/ exists, is a directory,
#    is writable, and is initially empty.
# 5. /home/user/monitoring/rules/enabled/critical_load.rule must **not** exist yet.
#
# Any deviation from these pre-conditions will cause a failing test with a
# detailed error message.

import os
from pathlib import Path
import stat
import pytest

# Full paths used throughout the tests
STAGING_DIR = Path("/home/user/staging_rules")
STAGING_FILE = STAGING_DIR / "critical_load.rule"

ENABLED_DIR = Path("/home/user/monitoring/rules/enabled")
ENABLED_FILE = ENABLED_DIR / "critical_load.rule"

EXPECTED_CONTENT = (
    b"alert: cpu_load\n"
    b"severity: critical\n"
    b"threshold: 0.85\n"
)


def assert_regular_file(path: Path, msg: str) -> None:
    """Helper to assert that `path` is a regular (non-symlink) file."""
    assert path.exists(), f"{msg}: path does not exist -> {path}"
    assert path.is_file(), f"{msg}: path exists but is not a regular file -> {path}"
    # Disallow symlinks: lstat and test for S_ISREG
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"{msg}: path exists but is not a regular file (maybe symlink) -> {path}"


def test_staging_directory_exists_and_is_correct() -> None:
    # 1. Directory presence
    assert STAGING_DIR.exists(), f"Staging directory missing: expected at {STAGING_DIR}"
    assert STAGING_DIR.is_dir(), f"Staging path exists but is not a directory: {STAGING_DIR}"

    # 2. Directory must contain exactly one file named 'critical_load.rule'
    contents = sorted(p.name for p in STAGING_DIR.iterdir())
    assert contents == ["critical_load.rule"], (
        "Staging directory must contain exactly one file named 'critical_load.rule'. "
        f"Found: {contents or '<<EMPTY>>'}"
    )


def test_staging_file_content_is_exact() -> None:
    # 3. File presence & content
    assert_regular_file(STAGING_FILE, "Expected staging rule file not found or invalid")

    content = STAGING_FILE.read_bytes()
    assert content == EXPECTED_CONTENT, (
        "Content of /home/user/staging_rules/critical_load.rule differs from the expected "
        "three-line definition.\n\n"
        f"Expected bytes:\n{EXPECTED_CONTENT!r}\n\nActual bytes:\n{content!r}"
    )


def test_enabled_directory_preconditions() -> None:
    # 4. Target directory presence
    assert ENABLED_DIR.exists(), f"Enabled rules directory missing: expected at {ENABLED_DIR}"
    assert ENABLED_DIR.is_dir(), f"Enabled path exists but is not a directory: {ENABLED_DIR}"

    # 4a. Directory must be writable
    assert os.access(ENABLED_DIR, os.W_OK), (
        f"Enabled directory exists but is not writable by current user: {ENABLED_DIR}"
    )

    # 4b. Directory must be empty before move
    enabled_contents = sorted(p.name for p in ENABLED_DIR.iterdir())
    assert not enabled_contents, (
        "Enabled directory should be empty before activating the rule.\n"
        f"Currently contains: {enabled_contents}"
    )

    # 5. The destination file must *not* exist yet
    assert not ENABLED_FILE.exists(), (
        f"Destination rule file already exists before move: {ENABLED_FILE}"
    )