# test_initial_state.py
"""
Pytest suite that validates the **initial** filesystem state before the
student carries out the credential-rotation task.

Checks performed:
1. /home/user/app/config exists and is a directory.
2. The directory contains **exactly** one file named credentials.env.
3. /home/user/app/config/credentials.env exists, is a regular file, and its
   contents match the expected legacy credentials *byte-for-byte* with NO
   trailing newline at EOF.

Nothing related to the files that will be created later
(credentials_legacy.env, rotation.log, etc.) is tested here.
"""

import os
from pathlib import Path

import pytest


CONFIG_DIR = Path("/home/user/app/config")
CREDENTIALS_FILE = CONFIG_DIR / "credentials.env"

# Expected bytes (3 lines, the final line has **no** trailing newline)
EXPECTED_CREDENTIALS_BYTES = (
    b"DB_USER=legacyuser\n"
    b"DB_PASSWORD=L0ngOldPass\n"
    b"API_TOKEN=oldtoken999"
)


def test_config_directory_exists_and_only_contains_credentials_env():
    assert CONFIG_DIR.exists(), f"Missing directory: {CONFIG_DIR}"
    assert CONFIG_DIR.is_dir(), f"{CONFIG_DIR} exists but is not a directory"

    # List non-hidden entries in the directory
    entries = [p.name for p in CONFIG_DIR.iterdir() if not p.name.startswith(".")]
    assert (
        entries == ["credentials.env"]
    ), f"{CONFIG_DIR} should contain only 'credentials.env'; found: {entries}"


def test_credentials_env_exists_and_matches_expected_content():
    assert CREDENTIALS_FILE.exists(), f"Missing file: {CREDENTIALS_FILE}"
    assert CREDENTIALS_FILE.is_file(), f"{CREDENTIALS_FILE} exists but is not a regular file"

    file_bytes = CREDENTIALS_FILE.read_bytes()

    # Verify byte-for-byte equality
    assert (
        file_bytes == EXPECTED_CREDENTIALS_BYTES
    ), (
        f"Contents of {CREDENTIALS_FILE} do not match the expected legacy "
        "credentials. Ensure the file has exactly the three legacy lines with "
        "no extra whitespace or trailing newline."
    )

    # Explicitly ensure there is no trailing newline at EOF
    assert not file_bytes.endswith(
        b"\n"
    ), f"{CREDENTIALS_FILE} must NOT have a trailing newline at EOF"