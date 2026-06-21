# test_initial_state.py
#
# This test-suite validates the _initial_ operating-system / filesystem
# state that must be present **before** the student starts working on the
# “backup-and-restore” task.
#
# DO NOT modify these tests.  They deliberately check for
#   • presence and *exact* contents/permissions of the pre-created files
#   • absence of files that the student must later create
#
# A failing test indicates that the grading environment itself is broken,
# not that the student made a mistake.

import os
import stat
from pathlib import Path

BACKUP_DIR = Path("/home/user/backup")
DAT_FILE = BACKUP_DIR / "weekly_backup.dat"
SHA_FILE = BACKUP_DIR / "weekly_backup.sha256"
INTEGRITY_LOG = BACKUP_DIR / "integrity_check.log"
FIREWALL_CONF = BACKUP_DIR / "firewall_rules.backup.conf"

EXPECTED_SHA_LINE = (
    "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb  "
    "weekly_backup.dat\n"
)


def _mode(path: Path) -> int:
    """Return the permission bits (e.g. 0o644) of *path*."""
    return stat.S_IMODE(path.stat().st_mode)


# ---------------------------------------------------------------------------
# Positive checks (things that MUST already exist)
# ---------------------------------------------------------------------------

def test_backup_directory_exists_with_correct_permissions():
    assert BACKUP_DIR.exists(), f"Required directory missing: {BACKUP_DIR}"
    assert BACKUP_DIR.is_dir(), f"{BACKUP_DIR} exists but is not a directory"
    assert _mode(BACKUP_DIR) == 0o755, (
        f"{BACKUP_DIR} must have permissions 0755, "
        f"but has {oct(_mode(BACKUP_DIR))}"
    )


def test_weekly_backup_dat_exists_with_correct_content_and_permissions():
    assert DAT_FILE.exists(), f"Required file missing: {DAT_FILE}"
    assert DAT_FILE.is_file(), f"{DAT_FILE} exists but is not a regular file"
    assert _mode(DAT_FILE) == 0o644, (
        f"{DAT_FILE} must have permissions 0644, "
        f"but has {oct(_mode(DAT_FILE))}"
    )

    data = DAT_FILE.read_bytes()
    assert data == b"a", (
        f"{DAT_FILE} must contain exactly one byte 'a' (0x61) with no newline. "
        f"Found {len(data)} bytes: {data!r}"
    )


def test_weekly_backup_sha256_exists_with_correct_content_and_permissions():
    assert SHA_FILE.exists(), f"Required file missing: {SHA_FILE}"
    assert SHA_FILE.is_file(), f"{SHA_FILE} exists but is not a regular file"
    assert _mode(SHA_FILE) == 0o644, (
        f"{SHA_FILE} must have permissions 0644, "
        f"but has {oct(_mode(SHA_FILE))}"
    )

    content = SHA_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_SHA_LINE, (
        f"{SHA_FILE} must contain exactly:\n{EXPECTED_SHA_LINE!r}\n"
        f"but contains:\n{content!r}"
    )


# ---------------------------------------------------------------------------
# Negative checks (things that MUST NOT exist yet)
# ---------------------------------------------------------------------------

def test_integrity_log_does_not_exist_yet():
    assert not INTEGRITY_LOG.exists(), (
        f"{INTEGRITY_LOG} must NOT exist before the student runs their solution"
    )


def test_firewall_conf_does_not_exist_yet():
    assert not FIREWALL_CONF.exists(), (
        f"{FIREWALL_CONF} must NOT exist before the student runs their solution"
    )