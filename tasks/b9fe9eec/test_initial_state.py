# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating-system /
# file-system before the student performs any work.  These checks guarantee
# that the environment matches the specification described in the task
# (“pre-existing data” as well as the *absence* of any artefacts the student
# is expected to create).

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")

# --- Paths that must ALREADY exist -----------------------------------------

APP_LOG_DIR = HOME / "app" / "logs"
APP_LOG_FILE = APP_LOG_DIR / "app.log"

# --- Paths that must NOT exist at the outset --------------------------------

BACKUPS_DIR           = HOME / "backups"
BACKUP_TAR_GZ         = BACKUPS_DIR / "logs_backup_2025-01-01.tar.gz"
BACKUP_CHECKSUM_FILE  = BACKUPS_DIR / "backup_checksums.log"

MONITORING_DIR        = HOME / "monitoring"
ALERTS_CONF_FILE      = MONITORING_DIR / "alerts.conf"

# ---------------------------------------------------------------------------

def test_app_log_directory_exists_and_is_directory():
    """The source directory /home/user/app/logs must already exist."""
    assert APP_LOG_DIR.is_dir(), (
        f"Expected directory {APP_LOG_DIR} to exist, "
        "but it was not found or is not a directory."
    )


def test_app_log_file_exists_with_expected_content():
    """The file app.log must exist and contain the initial sample lines."""
    assert APP_LOG_FILE.is_file(), (
        f"Expected file {APP_LOG_FILE} to exist, but it was not found."
    )

    expected_lines = [
        "2024-01-05 12:00:00 Application started",
        "2024-01-05 12:05:00 Application running",
    ]

    # Read in a memory-safe manner even for large files
    with APP_LOG_FILE.open("r", encoding="utf-8") as f:
        file_content = [line.rstrip("\n") for line in f]

    # The file may contain additional lines, but the first two lines must
    # match exactly.
    assert file_content[:2] == expected_lines, (
        f"The first two lines of {APP_LOG_FILE} do not match the expected "
        "pre-existing log content."
    )


@pytest.mark.parametrize(
    "path_to_check",
    [
        BACKUPS_DIR,
        BACKUP_TAR_GZ,
        BACKUP_CHECKSUM_FILE,
        MONITORING_DIR,
        ALERTS_CONF_FILE,
    ],
)
def test_backup_and_monitoring_artifacts_absent(path_to_check: Path):
    """
    None of the artefacts that the student is supposed to create should exist
    beforehand.  Their presence would indicate that the environment is not
    in the expected *initial* state.
    """
    assert not path_to_check.exists(), (
        f"Unexpected pre-existing path: {path_to_check}. "
        "The initial state should not contain any backup/monitoring artefacts."
    )