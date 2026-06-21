# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem
# state for the “Infrastructure Provisioning” exercise **before** the
# student performs any actions.
#
# It asserts that:
#   • The expected provisioning directory tree and files exist.
#   • The exact byte contents of the three source files are correct.
#   • No archive, recovery, or logs directories (or related files) exist yet.
#
# All failures include precise, actionable messages.
#
# NOTE: Uses only Python’s stdlib + pytest as required.

import hashlib
from pathlib import Path

import pytest

HOME = Path("/home/user")

# ---------- Expected paths ----------------------------------------------------

PROVISIONING_DIR = HOME / "provisioning"
CONFIG_DIR       = PROVISIONING_DIR / "config"
SCRIPTS_DIR      = PROVISIONING_DIR / "scripts"
DOCS_DIR         = PROVISIONING_DIR / "docs"

APP_CONF   = CONFIG_DIR / "app.conf"
DEPLOY_SH  = SCRIPTS_DIR / "deploy.sh"
README_MD  = DOCS_DIR / "readme.md"

ARCHIVES_DIR       = HOME / "archives"
RECOVERY_DIR       = HOME / "recovery"
LOGS_DIR           = PROVISIONING_DIR / "logs"
ARCHIVE_FILE       = ARCHIVES_DIR / "infra_provisioning_backup.tar.gz"

# ---------- Expected byte contents -------------------------------------------

EXPECTED_CONTENT = {
    APP_CONF:  b"port=8080\nmode=production\n",
    DEPLOY_SH: b"#!/bin/bash\necho Deploying...\n",
    README_MD: b"# Infrastructure Provisioning\nThis directory contains scripts.\n",
}

# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------

def md5sum(data: bytes) -> str:
    """Return the hex MD5 checksum of *data* (for debugging messages)."""
    return hashlib.md5(data).hexdigest()


# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------

def test_directory_structure_exists():
    """
    Verify that the provisioning directory and its immediate sub-directories
    exist, and that unrelated directories do *not* exist yet.
    """
    # Existing directories
    for directory in (PROVISIONING_DIR, CONFIG_DIR, SCRIPTS_DIR, DOCS_DIR):
        assert directory.is_dir(), f"Expected directory {directory} is missing."

    # Directories that must **not** pre-exist
    for directory in (ARCHIVES_DIR, RECOVERY_DIR, LOGS_DIR):
        assert not directory.exists(), (
            f"Directory {directory} should NOT exist before the student acts."
        )


def test_required_files_present_with_correct_contents():
    """
    Ensure the three required files exist with the exact expected byte contents
    (including trailing newlines).
    """
    for filepath, expected_bytes in EXPECTED_CONTENT.items():
        assert filepath.is_file(), f"Expected file {filepath} is missing."

        actual_bytes = filepath.read_bytes()
        assert actual_bytes == expected_bytes, (
            f"File {filepath} has unexpected contents.\n"
            f"Expected MD5: {md5sum(expected_bytes)}\n"
            f"Actual   MD5: {md5sum(actual_bytes)}"
        )


def test_archive_does_not_exist_yet():
    """
    Sanity-check that the backup archive does not exist before the student
    creates it.
    """
    assert not ARCHIVE_FILE.exists(), (
        f"Archive {ARCHIVE_FILE} should NOT exist at the initial state."
    )