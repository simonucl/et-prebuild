# test_initial_state.py
"""
Pytest suite validating the initial filesystem state *before* the learner
performs any action for the “symlink update” task.

Only the prerequisite path(s)—never the paths the learner is expected to
create—are checked.

Expected pre-state (truth value supplied by the task description):
1.  /home/user/www/releases/2023-01-15  MUST exist and be a directory.
2.  No assumptions are made about any other path (the symlink, log
    directory, and log file are **not** tested here by design).

If the mandatory “releases” directory is missing or not a directory, the
tests will fail with clear, actionable messages.
"""

import os
from pathlib import Path

RELEASE_DIR = Path("/home/user/www/releases/2023-01-15")


def test_release_dir_exists():
    """
    The directory that will become the symlink target must already exist.
    """
    assert RELEASE_DIR.exists(), (
        f"Required directory '{RELEASE_DIR}' is missing.\n"
        "Create it (containing the release assets) before running the task."
    )


def test_release_dir_is_directory():
    """
    The path exists but must specifically be a directory—not a file, link, etc.
    """
    assert RELEASE_DIR.is_dir(), (
        f"Path '{RELEASE_DIR}' exists but is not a directory.\n"
        "Ensure it is a real directory holding the release contents."
    )