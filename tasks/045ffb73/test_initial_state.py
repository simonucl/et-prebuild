# test_initial_state.py
#
# This pytest suite verifies the **initial** state of the system,
# i.e. *before* the learner performs any of the steps described in
# the assignment.  Nothing related to the backup environment should
# exist yet.

import os
import stat
import pytest

HOME_DIR = "/home/user"
BACKUP_DIR = os.path.join(HOME_DIR, "db_backups")
BACKUP_SCRIPT = os.path.join(BACKUP_DIR, "pg_backup.sh")
BACKUP_LOG = os.path.join(BACKUP_DIR, "backup_setup.log")
BASHRC = os.path.join(HOME_DIR, ".bashrc")
EXPORT_LINE = "export PG_BACKUP_DIR=/home/user/db_backups"


def _path_state(path):
    """
    Return a string describing whether the path currently exists and,
    if so, what type it is.
    """
    if not os.path.exists(path):
        return "does not exist"
    if os.path.isfile(path):
        return "is a file"
    if os.path.isdir(path):
        return "is a directory"
    return "exists but is neither a regular file nor directory"


def test_backup_directory_absent():
    """The main backup directory must NOT exist yet."""
    assert not os.path.exists(
        BACKUP_DIR
    ), f"Pre-task check failed: {BACKUP_DIR} already exists—it {_path_state(BACKUP_DIR)}."


def test_backup_script_absent():
    """The shell script must NOT exist yet."""
    assert not os.path.exists(
        BACKUP_SCRIPT
    ), f"Pre-task check failed: {BACKUP_SCRIPT} already exists—it {_path_state(BACKUP_SCRIPT)}."


def test_backup_log_absent():
    """The log file must NOT exist yet."""
    assert not os.path.exists(
        BACKUP_LOG
    ), f"Pre-task check failed: {BACKUP_LOG} already exists—it {_path_state(BACKUP_LOG)}."


def test_bashrc_not_already_configured():
    """
    If ~/.bashrc exists, its final line must NOT already be the
    export PG_BACKUP_DIR line—students are supposed to append this.
    """
    if not os.path.exists(BASHRC):
        # No ~/.bashrc is acceptable at this stage.
        pytest.skip(f"{BASHRC} does not exist—nothing to verify.")
    else:
        with open(BASHRC, encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()

        # Remove any trailing blank lines before checking the last
        # non-blank line (common in skeleton images).
        stripped_lines = [ln.rstrip("\n") for ln in lines]
        while stripped_lines and stripped_lines[-1].strip() == "":
            stripped_lines.pop()

        if not stripped_lines:
            # An empty file is also fine.
            return

        last_line = stripped_lines[-1]
        assert (
            last_line != EXPORT_LINE
        ), (
            f"Pre-task check failed: {BASHRC} already ends with\n"
            f'    "{EXPORT_LINE}"\n'
            "but it should NOT be present before the student edits the file."
        )