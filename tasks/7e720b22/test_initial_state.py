# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student performs any edits for the “monthly archive cycle”
# exercise.  If these tests fail it means the starting files/directories
# are not in the exact condition that the task description assumes.

import os
import re
import pytest
from pathlib import Path

HOME = Path("/home/user")
BACKUP_DIR = HOME / "backups"
CONF_DIR = BACKUP_DIR / "conf"

BACKUP_YAML = CONF_DIR / "backup.yaml"
STORAGE_TOML = CONF_DIR / "storage.toml"
EDIT_LOG = BACKUP_DIR / "backup_edit.log"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def read_text(path: Path) -> str:
    """Return the text content of *path* or raise an AssertionError if missing."""
    assert path.exists(), f"Required file is missing: {path}"
    assert path.is_file(), f"Expected a regular file but found something else: {path}"
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        raise AssertionError(f"Could not read {path}: {exc}") from exc


# ---------------------------------------------------------------------------
# Directory level checks
# ---------------------------------------------------------------------------

def test_required_directory_tree_exists():
    """
    The directory tree /home/user/backups/conf **must** exist before the
    student starts.  If this test fails the initial fixture is broken.
    """
    assert BACKUP_DIR.is_dir(), f"Missing directory: {BACKUP_DIR}"
    assert CONF_DIR.is_dir(), f"Missing directory: {CONF_DIR}"


# ---------------------------------------------------------------------------
# /home/user/backups/conf/backup.yaml
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "needle",
    [
        'schedule: "03:00"',
        "- /var/www",
        "- /home/projects",
        'compression: "lz4"',
        "retention_days: 30",
    ],
)
def test_backup_yaml_contains_expected_lines(needle):
    """
    backup.yaml must contain *exactly* the original values specified in the
    task description.  These assertions deliberately look for **lz4** and
    **30** so that the file is guaranteed to be in the pre-edited state.
    """
    content = read_text(BACKUP_YAML)
    assert needle in content, (
        f"File {BACKUP_YAML} should contain the line:\n    {needle}\n"
        "but it does not.  Ensure the initial backup.yaml is unmodified."
    )


def test_backup_yaml_has_not_been_edited_yet():
    """
    Ensure the student hasn’t already applied the required edits.
    """
    content = read_text(BACKUP_YAML)
    forbidden = [
        'compression: "zstd"',
        "retention_days: 45",
    ]
    for line in forbidden:
        assert line not in content, (
            f"File {BACKUP_YAML} already contains '{line}', "
            "but it should still be in its original state."
        )


# ---------------------------------------------------------------------------
# /home/user/backups/conf/storage.toml
# ---------------------------------------------------------------------------

def test_storage_toml_contains_expected_values():
    """
    storage.toml must still reference the original bucket name and placeholder
    credentials before any edits occur.
    """
    content = read_text(STORAGE_TOML)

    expected_pairs = {
        'bucket = "company-backups"': "original bucket setting",
        'access_key = "REPLACE_ME"': "placeholder access_key",
        'secret_key = "REPLACE_ME"': "placeholder secret_key",
    }

    for key, desc in expected_pairs.items():
        assert key in content, (
            f"{desc!s} is missing in {STORAGE_TOML}.  "
            "The initial file appears to have been modified."
        )

    # Sanity: make sure the target bucket name does NOT appear yet.
    assert 'bucket = "archive-backups"' not in content, (
        f"{STORAGE_TOML} already references 'archive-backups', "
        "but it should still be 'company-backups'."
    )


# ---------------------------------------------------------------------------
# /home/user/backups/backup_edit.log
# ---------------------------------------------------------------------------

def test_edit_log_is_untouched_or_absent():
    """
    The change-log might or might not exist initially.  If it exists, its last
    four lines must **not** already contain the final update messages.  This
    protects against pre-populated logs.
    """
    if not EDIT_LOG.exists():
        pytest.skip(f"{EDIT_LOG} does not exist yet – this is allowed.")
        return  # pragma: no cover

    assert EDIT_LOG.is_file(), f"{EDIT_LOG} exists but is not a regular file."

    # Read the last ~20 lines (more than enough) and look for any of the target sentences.
    tail_lines = read_text(EDIT_LOG).splitlines()[-20:]

    forbidden_sentences = [
        "compression field updated from lz4 to zstd",
        "retention_days updated from 30 to 45",
        "bucket updated from company-backups to archive-backups",
        "credentials updated",
    ]

    pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} - ")

    for sentence in forbidden_sentences:
        for line in tail_lines:
            # Remove a leading timestamp (if present) before comparison.
            cleaned = pattern.sub("", line, count=1)
            assert cleaned != sentence, (
                f"The log {EDIT_LOG} already contains a final update line "
                f"('{sentence}').  The initial log should *not* have those lines."
            )