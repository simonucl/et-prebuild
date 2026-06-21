# test_initial_state.py
#
# Pytest suite that validates the clean starting state of the
# operating system / file-system before the student performs
# any work for the “Create and Maintain a Build-Artifacts SQLite
# Inventory” task.
#
# A *clean* state means:
#   • The working directory /home/user exists, but the dedicated
#     build workspace (/home/user/builds) has not been created yet.
#   • Therefore no database, report, or log files from a prior run
#     should be present.
#   • The system-provided sqlite3 CLI must be discoverable so the
#     student can rely on it later.
#
# If any assertion here fails, the failure message will explicitly
# tell what pre-existing item must be removed or what core component
# is missing.

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HOME = Path("/home/user")
BUILDS_DIR = HOME / "builds"
DB_FILE = BUILDS_DIR / "artifacts.db"
REPORT_CSV = BUILDS_DIR / "build_artifact_report.csv"
EXPORT_LOG = BUILDS_DIR / "export.log"


def test_home_directory_exists_and_is_directory():
    assert HOME.exists(), f"The home directory {HOME} must exist."
    assert HOME.is_dir(), f"The path {HOME} exists but is not a directory."


def test_builds_directory_does_not_yet_exist():
    # The student must create /home/user/builds themselves.
    assert not BUILDS_DIR.exists(), (
        f"The directory {BUILDS_DIR} already exists. "
        "Start with a clean slate: remove it before beginning the task."
    )


def test_no_residual_artifacts():
    # None of the task output files should pre-exist.
    residuals = [p for p in (DB_FILE, REPORT_CSV, EXPORT_LOG) if p.exists()]
    assert not residuals, (
        "Found pre-existing build artifacts that should NOT be present yet:\n"
        + "\n".join(str(p) for p in residuals)
    )


def test_sqlite3_cli_available():
    sqlite_path = shutil.which("sqlite3")
    assert sqlite_path, (
        "The sqlite3 CLI binary could not be found in $PATH. "
        "It must be available so the student can run the required commands."
    )

    # Additionally, confirm that the binary is executable.
    st_mode = os.stat(sqlite_path).st_mode
    assert bool(st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), (
        f"The sqlite3 binary at {sqlite_path} is not marked as executable."
    )

    # Finally, ensure invoking `sqlite3 -version` returns exit code 0.
    try:
        subprocess.run([sqlite_path, "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        pytest.fail(f"Running '{sqlite_path} -version' failed: {exc}")