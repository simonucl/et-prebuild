# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student carries out the migration task.
#
# The tests deliberately fail fast and with clear, actionable
# messages so that any deviation from the expected starting point is
# obvious.

import os
import pathlib
import stat
import pytest

HOME = pathlib.Path("/home/user")

OLD_CONF_DIR = HOME / "old_service" / "conf"
NEW_SERVICE_DIR = HOME / "new_service"
BACKUP_DIR = HOME / "backup_old_conf"
MIGRATION_LOGS_DIR = HOME / "migration_logs"
SYMLINK_LOG = MIGRATION_LOGS_DIR / "symlink_audit.log"

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def is_regular_file(path: pathlib.Path) -> bool:
    """True if the path is a regular file (not a directory, not a symlink)."""
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return False
    return stat.S_ISREG(mode) and not path.is_symlink()


# --------------------------------------------------------------------------- #
# Expected ground-truth data for the initial state
# --------------------------------------------------------------------------- #
EXPECTED_FILES = {
    "a.conf": "alpha=1\nbeta=2\n",
    "b.conf": "gamma=3\ndelta=4\n",
    "c.conf": "[service]\nport=8080\n",
}


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_old_conf_directory_exists():
    assert OLD_CONF_DIR.exists(), (
        f"Required directory {OLD_CONF_DIR} is missing."
    )
    assert OLD_CONF_DIR.is_dir(), (
        f"{OLD_CONF_DIR} exists but is not a directory."
    )


def test_old_conf_contains_expected_regular_files_with_correct_contents():
    # 1. Names present
    actual_files = {p.name for p in OLD_CONF_DIR.iterdir() if p.is_file()}
    expected_files = set(EXPECTED_FILES.keys())
    missing = expected_files - actual_files
    extra   = actual_files - expected_files

    assert not missing, (
        f"{OLD_CONF_DIR} is missing expected file(s): {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"{OLD_CONF_DIR} contains unexpected file(s): {', '.join(sorted(extra))}"
    )

    # 2. Each is a regular file, not a symlink, and has the expected content
    for fname, expected_text in EXPECTED_FILES.items():
        path = OLD_CONF_DIR / fname
        assert is_regular_file(path), (
            f"{path} must be a *regular* file and not a symlink."
        )

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover
            pytest.fail(f"Could not read {path}: {exc!r}")

        assert content == expected_text, (
            f"Content of {path} does not match the expected initial text."
        )


def test_new_service_and_backup_directories_do_not_yet_exist():
    assert not NEW_SERVICE_DIR.exists(), (
        f"{NEW_SERVICE_DIR} should NOT exist before the migration begins."
    )
    assert not BACKUP_DIR.exists(), (
        f"{BACKUP_DIR} should NOT exist before the migration begins."
    )


def test_migration_logs_directory_exists_and_is_empty():
    assert MIGRATION_LOGS_DIR.exists(), (
        f"Directory {MIGRATION_LOGS_DIR} is required but missing."
    )
    assert MIGRATION_LOGS_DIR.is_dir(), (
        f"{MIGRATION_LOGS_DIR} exists but is not a directory."
    )

    # Directory should be empty (no log file yet)
    items = [p.name for p in MIGRATION_LOGS_DIR.iterdir()]
    assert SYMLINK_LOG.name not in items, (
        f"{SYMLINK_LOG} must not exist before migration—found one already."
    )
    # Ignore other dot-files that some systems create; ensure it has no
    # regular (non-dot) files.
    non_hidden_items = [n for n in items if not n.startswith(".")]
    assert not non_hidden_items, (
        f"{MIGRATION_LOGS_DIR} should be empty but contains: {', '.join(sorted(non_hidden_items))}"
    )