# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in a clean state **before** the student starts the exercise.
#
# Specifically, we assert that:
#   •  /home/user/diagnostics does NOT yet exist.
#   •  Therefore, the two required artefacts
#       - /home/user/diagnostics/engine_metrics.db
#       - /home/user/diagnostics/sqlite_session.log
#     also do NOT exist.
#   •  The `sqlite3` command-line client is available on PATH; the
#     student must use it later.
#
# If any of these assertions fail, the starting environment is not
# suitable for the exercise and must be fixed before the student
# proceeds.

import os
import shutil
from pathlib import Path

DIAG_DIR = Path("/home/user/diagnostics")
DB_PATH = DIAG_DIR / "engine_metrics.db"
LOG_PATH = DIAG_DIR / "sqlite_session.log"


def test_sqlite_cli_available():
    """
    Verify that the `sqlite3` CLI tool is installed and discoverable on PATH.
    """
    sqlite_path = shutil.which("sqlite3")
    assert sqlite_path is not None, (
        "The `sqlite3` command-line tool is required for this exercise but "
        "was not found on the system PATH."
    )


def test_diagnostics_directory_absent():
    """
    The diagnostics directory should NOT exist before the student starts.
    Its absence guarantees the exercise begins from a clean slate.
    """
    assert not DIAG_DIR.exists(), (
        f"The directory {DIAG_DIR} already exists. "
        "The exercise expects the student to create it from scratch."
    )


def test_engine_metrics_db_absent():
    """
    The SQLite database must not exist yet.
    """
    assert not DB_PATH.exists(), (
        f"The file {DB_PATH} is present, but it should be created by the "
        "student during the exercise."
    )


def test_sqlite_session_log_absent():
    """
    The session log must not exist yet.
    """
    assert not LOG_PATH.exists(), (
        f"The file {LOG_PATH} is present, but it should be created by the "
        "student during the exercise."
    )