# test_initial_state.py
#
# Pytest suite that checks the machine’s state **before** the student’s
# provisioning script is executed.  None of the artefacts that the student
# is supposed to create (directory, log file, backups, etc.) should be
# present at this point.

import os
import glob
from pathlib import Path

LOGS_DIR = Path("/home/user/provisioning/logs")
LOG_FILE = LOGS_DIR / "network_diagnostics.log"
LOG_GLOB = str(LOG_FILE) + "*"   # catches backups such as *.log~, *.log.bak …

def _human(path: Path) -> str:
    """Return a nice printable representation for assertion messages."""
    return f"‘{path.as_posix()}’"

def test_log_file_must_not_exist():
    """
    The main log file must be absent before the student runs their script.
    """
    assert not LOG_FILE.exists(), (
        f"{_human(LOG_FILE)} already exists but should not be present "
        "before the provisioning script is executed."
    )

def test_no_matching_backup_or_temp_files():
    """
    No file matching /home/user/provisioning/logs/network_diagnostics.log*
    may exist yet—this prevents stray backups or temp files from interfering
    with later grading.
    """
    offenders = [Path(p) for p in glob.glob(LOG_GLOB)]
    assert offenders == [] or offenders == [LOG_FILE] and not LOG_FILE.exists(), (
        "Found unexpected file(s) that match the diagnostic-log pattern:\n  "
        + "\n  ".join(p.as_posix() for p in offenders)
        + "\nRemove these before running your provisioning script."
    )

def test_logs_directory_may_exist_but_must_not_contain_log():
    """
    The directory /home/user/provisioning/logs may or may not exist at this
    stage.  If it does exist, it must not yet contain the target log file.
    """
    if LOGS_DIR.exists():
        assert LOGS_DIR.is_dir(), (
            f"{_human(LOGS_DIR)} exists but is not a directory."
        )
        assert LOG_FILE not in LOGS_DIR.iterdir(), (
            f"{_human(LOG_FILE)} already present inside {_human(LOGS_DIR)}; "
            "remove it before starting the task."
        )