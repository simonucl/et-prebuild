# test_initial_state.py
#
# Pytest suite that asserts the **initial** state of the operating-system
# before the learner carries out any steps described in the prompt.
#
# The environment should be “clean”, i.e. none of the goal artefacts
# the student is asked to create should already be present or correctly
# configured.  These tests fail early ‑ giving clear, actionable error
# messages ‑ if something is pre-populated (which would render the task
# meaningless).

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
BACKUP_DIR = HOME / "db_backups"
BASHRC = HOME / ".bashrc"
AUDIT_LOG = HOME / "backup_setup.log"
EXPORT_LINE = 'export BACKUP_DIR="/home/user/db_backups"'
AUDIT_CONTENT = "BACKUP_DIR set to /home/user/db_backups\n"


def test_backup_directory_does_not_preexist():
    """
    The directory /home/user/db_backups must **not** exist yet.
    It will be created by the student.
    """
    assert not BACKUP_DIR.exists(), (
        f"The directory {BACKUP_DIR} already exists. "
        "The task requires the learner to create it."
    )


def test_bashrc_does_not_yet_contain_export_line():
    """
    .bashrc should either be missing or *not* already contain the exact
    expected export directive as its final non-empty line.
    """
    if not BASHRC.exists():
        # Perfectly acceptable: the student will create/append to it.
        return

    try:
        lines = BASHRC.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {BASHRC}: {exc}")

    # Strip trailing empty lines and inspect the last non-empty one.
    meaningful_lines = [ln for ln in lines if ln.strip()]
    if not meaningful_lines:
        return  # File is empty/blank → definitely no export line yet.

    last_line = meaningful_lines[-1]
    assert last_line != EXPORT_LINE, (
        f"{BASHRC} already ends with the required export line:\n"
        f"    {EXPORT_LINE}\n"
        "The learner must add this themselves; remove it for a clean slate."
    )


def test_audit_log_not_prepopulated():
    """
    The audit log should *not* yet exist with the final expected content.
    It is the learner's responsibility to create it.
    """
    if not AUDIT_LOG.exists():
        return  # Log does not exist → this is the desired clean state.

    # If it *does* exist, ensure the content is *not* already correct.
    try:
        content = AUDIT_LOG.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {AUDIT_LOG}: {exc}")

    assert content != AUDIT_CONTENT, (
        f"{AUDIT_LOG} already contains the final expected audit line:\n"
        f"    {content!r}\n"
        "Remove or alter the file so the learner can generate it."
    )