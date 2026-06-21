# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem
# is in the expected “pre-rotation” state *before* the student carries
# out the credential-rotation procedure described in the assignment.
#
# IMPORTANT:  These tests purposefully look for the *old* state.  If they
#             pass, the student has not yet modified anything they were
#             asked to change.  The grader will run a *separate* test
#             suite afterwards to confirm that the student’s solution
#             brought the system to the required final state.
#
# Allowed imports: only stdlib + pytest
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
INFRA_DIR = HOME / "infra"

HOSTS_FILE = INFRA_DIR / "hosts.override"
README_FILE = INFRA_DIR / "README.txt"

BACKUP_FILE = INFRA_DIR / "hosts.override.bak.20240601"
AUDIT_DIR = HOME / "security" / "audit"
AUDIT_LOG = AUDIT_DIR / "20240601_rotation.log"

OLD_LINES = [
    "10.10.10.10 db.internal.example.com\n",
    "10.10.10.20 api.internal.example.com\n",
    "10.10.10.30 cache.internal.example.com\n",
]


def _read_file(path: Path) -> list[str]:
    """Return the file’s lines exactly as they are on disk."""
    with path.open("rt", encoding="utf-8") as fp:
        return fp.readlines()


# ---------------------------------------------------------------------------
# Positive-existence checks
# ---------------------------------------------------------------------------
def test_hosts_override_file_exists():
    assert HOSTS_FILE.is_file(), (
        f"Missing hosts file at {HOSTS_FILE}. "
        "It must exist *before* the rotation starts."
    )


def test_hosts_override_contents_are_old_and_complete():
    lines = _read_file(HOSTS_FILE)
    assert lines == OLD_LINES, (
        f"{HOSTS_FILE} does not contain the expected pre-rotation mappings.\n"
        f"Expected exactly:\n{''.join(OLD_LINES)!r}\n"
        f"Found:\n{''.join(lines)!r}"
    )
    # Also ensure the file ends with a single newline.
    assert lines[-1].endswith("\n"), (
        f"{HOSTS_FILE} must end with exactly one newline character."
    )


def test_readme_exists_and_is_not_empty():
    assert README_FILE.is_file(), (
        f"Missing README file at {README_FILE}. It should already be present."
    )
    size = README_FILE.stat().st_size
    assert size > 0, f"{README_FILE} should not be empty."


# ---------------------------------------------------------------------------
# Negative-existence checks (things that should *not* exist yet)
# ---------------------------------------------------------------------------
def test_backup_file_does_not_exist_yet():
    assert not BACKUP_FILE.exists(), (
        f"Backup file {BACKUP_FILE} already exists! "
        "It should only be created by the rotation script."
    )


def test_audit_log_does_not_exist_yet():
    assert not AUDIT_LOG.exists(), (
        f"Audit log {AUDIT_LOG} already exists! "
        "It should only be created by the rotation script."
    )


def test_audit_directory_absent_or_empty():
    """
    The audit directory may or may not exist yet.  If it does exist, it
    should be empty at this stage (no rotation log present).
    """
    if AUDIT_DIR.exists():
        assert AUDIT_DIR.is_dir(), f"{AUDIT_DIR} exists but is not a directory."
        # Exclude hidden files like .gitkeep if instructor pre-seeded any.
        visible_files = [p for p in AUDIT_DIR.iterdir() if not p.name.startswith(".")]
        assert not visible_files, (
            f"{AUDIT_DIR} should be empty prior to rotation; found: "
            f"{', '.join(p.name for p in visible_files)}"
        )