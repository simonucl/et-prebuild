# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem
# state for the “backup_daemon” exercise.  It *must* be executed BEFORE the
# student carries out any actions.  The tests assert that no artefacts from a
# previous run are already present.
#
# Expectations (all paths are absolute):
#   1. /home/user/services/backup_daemon.conf       – must NOT exist
#   2. /home/user/task_logs/backup_daemon_setup.log – must NOT exist
#
# Directories (/home/user/services and /home/user/task_logs) may or may not
# exist; their presence is not relevant as long as the two files above are
# absent.
#
# Only stdlib + pytest are used.

import os
from pathlib import Path

CONF_FILE = Path("/home/user/services/backup_daemon.conf")
LOG_FILE = Path("/home/user/task_logs/backup_daemon_setup.log")


def _human_readable_absence(path: Path) -> str:
    """
    Helper that produces a clear, human-readable explanation if a path
    unexpectedly exists.
    """
    if path.is_symlink():
        return f"Symlink found at {path} -> {os.readlink(path)} (should not exist)"
    if path.is_file():
        return f"Unexpected file already exists at {path}"
    if path.is_dir():
        return f"Unexpected directory already exists at {path}"
    return f"Unexpected filesystem object already exists at {path}"


def test_configuration_file_is_absent():
    """
    The configuration file must NOT exist prior to the student action.
    """
    assert not CONF_FILE.exists(), _human_readable_absence(CONF_FILE)


def test_log_file_is_absent():
    """
    The audit / log file must NOT exist prior to the student action.
    """
    assert not LOG_FILE.exists(), _human_readable_absence(LOG_FILE)