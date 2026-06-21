# test_initial_state.py
"""
Pytest suite that validates the starting filesystem/OS state *before*
the student performs any actions for the “May-2023 log-archiving” task.

Only the prerequisites are verified here; no assertions about the
expected end-state (archive, error summary, cleanup, …) are made.
"""

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
APP_LOG_DIR = HOME / "app" / "logs"
BACKUP_DIR = HOME / "backup"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def read_lines(path):
    """Return the file’s contents as a list of strings *without* trailing NLs."""
    return path.read_text(encoding="utf-8").splitlines()


# ---------------------------------------------------------------------------
# Truth-data: exact contents of the pre-seeded log files
# ---------------------------------------------------------------------------

EXPECTED_LOG_CONTENTS = {
    APP_LOG_DIR / "app-2023-05-30.log": [
        "2023-05-30 10:00:00 INFO  Service started",
        "2023-05-30 10:05:00 WARN  Cache miss",
        "2023-05-30 10:10:00 ERROR Failed to connect to database",
        "2023-05-30 10:15:00 INFO  Service running",
        "2023-05-30 10:20:00 ERROR Timeout while reading from queue",
    ],
    APP_LOG_DIR / "app-2023-05-31.log": [
        "2023-05-31 09:00:00 INFO  Daily job started",
        "2023-05-31 09:05:00 ERROR Null pointer exception",
        "2023-05-31 09:10:00 WARN  Low disk space",
        "2023-05-31 09:15:00 ERROR Failed to send email",
        "2023-05-31 09:20:00 INFO  Daily job finished",
    ],
    APP_LOG_DIR / "app-2023-06-01.log": [
        "2023-06-01 08:00:00 INFO  Service started",
        "2023-06-01 08:10:00 INFO  Health check passed",
    ],
    APP_LOG_DIR / "app-2023-06-02.log": [
        "2023-06-02 11:00:00 INFO  Service started",
        "2023-06-02 11:05:00 ERROR Simulated June error",
    ],
}

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_app_log_directory_exists_and_is_directory():
    assert APP_LOG_DIR.exists(), f"Directory {APP_LOG_DIR} is missing."
    assert APP_LOG_DIR.is_dir(), f"{APP_LOG_DIR} exists but is not a directory."


def test_backup_directory_exists_and_is_writable(tmp_path):
    """
    The task will need to create files/sub-dirs inside /home/user/backup/.
    We check that the directory exists *and* we can write to it.
    """
    assert BACKUP_DIR.exists(), f"Directory {BACKUP_DIR} is missing."
    assert BACKUP_DIR.is_dir(), f"{BACKUP_DIR} exists but is not a directory."

    # Try to create & remove a temporary file to prove writability.
    test_file = BACKUP_DIR / ".__pytest_write_test__"
    try:
        test_file.write_text("can write", encoding="utf-8")
        assert test_file.exists(), f"Cannot write inside {BACKUP_DIR}."
    finally:
        test_file.unlink(missing_ok=True)


@pytest.mark.parametrize("path, expected_lines", EXPECTED_LOG_CONTENTS.items())
def test_each_expected_log_file_exists_with_exact_contents(path, expected_lines):
    assert path.exists(), f"Expected log file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."

    actual_lines = read_lines(path)
    assert (
        actual_lines == expected_lines
    ), f"Contents of {path} do not match the expected ground-truth."


def test_no_unexpected_shortfall_in_log_files():
    """
    There must be *at least* the four known log files.  We allow extra files
    because the application could have produced more, but we want to catch an
    accidental deletion of any May-2023 / June-2023 seed files.
    """
    present = {p.name for p in APP_LOG_DIR.iterdir() if p.is_file()}
    missing = {p.name for p in EXPECTED_LOG_CONTENTS} - present
    assert (
        not missing
    ), f"The following required log files are missing from {APP_LOG_DIR}: {', '.join(sorted(missing))}"