# test_initial_state.py
#
# This pytest suite validates the **initial** state of the filesystem
# before the student performs any work on the “quick network-diagnostics”
# task.  It purposefully checks for the *absence* of the artefact that
# the student is expected to create later on.

import os
import stat
from pathlib import Path

ARCHIVE_DIR = Path("/home/user/archive_logs")
LOG_FILE = ARCHIVE_DIR / "backup_server_netcheck.log"


def test_log_file_does_not_exist():
    """
    The network-diagnostic log MUST NOT exist before the student
    runs their solution script.
    """
    assert not LOG_FILE.exists(), (
        f"Found unexpected file at {LOG_FILE}. "
        "The diagnostic routine has apparently already been executed. "
        "Remove the file before running the student solution."
    )


def test_archive_dir_state_before_execution():
    """
    The archive directory either must not exist at all, or—if it does—must be
    empty.  This ensures the student can create/populate it without collision.
    """
    if not ARCHIVE_DIR.exists():
        # Directory absent: perfectly fine for the initial state.
        return

    # Directory exists: make sure it is actually a directory…
    assert ARCHIVE_DIR.is_dir(), (
        f"{ARCHIVE_DIR} exists but is not a directory. "
        "Please remove or rename it before the exercise."
    )

    # …and that it is empty.
    contents = list(ARCHIVE_DIR.iterdir())
    assert len(contents) == 0, (
        f"{ARCHIVE_DIR} is expected to be empty before the task starts, "
        f"but it already contains: {', '.join(str(p) for p in contents)}"
    )


def test_home_directory_permissions():
    """
    Sanity-check that /home/user exists and is accessible.
    The grader relies on being able to create files beneath it.
    """
    home = Path("/home/user")
    assert home.exists() and home.is_dir(), (
        "/home/user does not exist or is not a directory; "
        "the testing environment is not set up correctly."
    )

    # /home/user should at least allow read & execute bits for the owner.
    st = home.stat()
    mode = stat.S_IMODE(st.st_mode)
    owner_perms = (mode & 0o700) >> 6  # shift owner bits to lowest
    assert owner_perms & 0b101 == 0b101, (
        "/home/user must be readable and executable by its owner "
        "so that subsequent steps can create files inside it."
    )