# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is still in its pristine, “pre-task” state.  In other words, the
# audit artefact required by the assignment must NOT exist yet.
#
# If any of these tests fail it means somebody (or something) has
# already created the artefact, which would invalidate the initial
# conditions that downstream tests rely on.

import os
from pathlib import Path
import stat

AUDIT_DIR = Path("/home/user/audit")
AUDIT_LOG = AUDIT_DIR / "network_audit.log"


def test_audit_directory_absent():
    """
    The audit directory should NOT exist before the student runs the task.
    If it does exist, we also need to make sure it is *not* a file or a
    symlink masquerading as the directory we expect to be created later.
    """
    assert not AUDIT_DIR.exists(), (
        f"The directory {AUDIT_DIR} already exists. "
        "The task instructions assume the student will create it."
    )


def test_audit_log_absent():
    """
    The network_audit.log file must not be present yet.  This guarantees
    the student actually captures live command output in a new file.
    """
    assert not AUDIT_LOG.exists(), (
        f"The file {AUDIT_LOG} already exists. "
        "It should be created only after the diagnostic commands are run."
    )


def test_parent_home_directory_is_writable():
    """
    Sanity-check the parent directory (/home/user) so that we can later
    create the audit artefact.  If /home/user is not writable, the
    assignment cannot be completed.
    """
    home_dir = Path("/home/user")
    assert home_dir.is_dir(), "/home/user is missing or not a directory."

    # The current process should have write permission to /home/user.
    mode = home_dir.stat().st_mode
    writable = bool(mode & stat.S_IWUSR)
    assert writable, (
        "/home/user exists but is not writable; cannot proceed with the task."
    )