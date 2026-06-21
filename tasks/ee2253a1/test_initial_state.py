# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating
# system / filesystem before the student starts the hardening task.
#
# PRE-CONDITIONS THAT **MUST** BE PRESENT
# ---------------------------------------
# 1.  Directory  /home/user/service_configs                must exist
# 2.  File       /home/user/service_configs/httpd.conf.orig must exist
#     and contain the exact insecure sample configuration
#
# PRE-CONDITIONS THAT **MUST NOT** YET EXIST
# ------------------------------------------
# 1.  Directory  /home/user/service_configs/backup
# 2.  File       /home/user/service_configs/backup/httpd.conf.orig.bak
# 3.  File       /home/user/service_configs/httpd_hardened.conf
# 4.  File       /home/user/service_configs/hardening.log
#
# Any divergence from these expectations should cause a clear test failure.

import hashlib
import os
from pathlib import Path
import textwrap
import pytest

# CONSTANTS -------------------------------------------------------------------

BASE_DIR = Path("/home/user/service_configs")
ORIG_FILE = BASE_DIR / "httpd.conf.orig"
BACKUP_DIR = BASE_DIR / "backup"
BACKUP_FILE = BACKUP_DIR / "httpd.conf.orig.bak"
HARDENED_FILE = BASE_DIR / "httpd_hardened.conf"
LOG_FILE = BASE_DIR / "hardening.log"

EXPECTED_ORIG_CONTENT = textwrap.dedent("""\
    # Example Apache HTTPD Configuration
    ServerRoot "/usr/local/apache2"
    Listen 80
    LoadModule mpm_event_module modules/mod_mpm_event.so
    User daemon
    Group daemon
    ServerTokens Full
    ServerSignature On
    Options Indexes FollowSymLinks
    AllowOverride All
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1
    Timeout 300
    """)  # NOTE: final newline intentionally omitted here; we add it below
# Ensure the expected content ends with a single newline so comparisons are exact.
EXPECTED_ORIG_CONTENT += "\n"

# HELPERS ---------------------------------------------------------------------


def sha256_of_path(path: Path) -> str:
    """Return the hex-encoded SHA-256 of a file (or raise FileNotFoundError)."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# TESTS -----------------------------------------------------------------------


def test_base_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Required directory {BASE_DIR} is missing. "
        "The starting skeleton must include this directory."
    )


def test_original_file_exists():
    assert ORIG_FILE.is_file(), (
        f"Required original configuration file {ORIG_FILE} is missing. "
        "Students must start from this insecure sample."
    )


def test_original_file_content_exact_match():
    actual = ORIG_FILE.read_text(encoding="utf-8")
    # Show a diff-style output if mismatch occurs (pytest will display it).
    assert actual == EXPECTED_ORIG_CONTENT, (
        f"The file {ORIG_FILE} does not match the expected insecure sample "
        "configuration. Do not modify this file before hardening."
    )


def test_backup_directory_does_not_exist_yet():
    assert not BACKUP_DIR.exists(), (
        f"Backup directory {BACKUP_DIR} should NOT exist yet. "
        "It must be created by the student during the task, not beforehand."
    )


def test_backup_file_does_not_exist_yet():
    assert not BACKUP_FILE.exists(), (
        f"Backup file {BACKUP_FILE} should NOT exist yet. "
        "It must be created by the student during the task, not beforehand."
    )


def test_hardened_file_does_not_exist_yet():
    assert not HARDENED_FILE.exists(), (
        f"Hardened configuration {HARDENED_FILE} should NOT exist yet. "
        "It will be produced by the student as part of the task."
    )


def test_log_file_does_not_exist_yet():
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} should NOT exist yet. "
        "It will be produced by the student as part of the task."
    )