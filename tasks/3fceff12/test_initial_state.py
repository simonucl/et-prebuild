# test_initial_state.py
#
# This test-suite validates the machine *before* the student performs the
# assignment.  It checks that the two original log files are present with the
# exact expected contents and permissions, and that no output directory or CSV
# result file exists yet.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _assert_file_mode(path: Path, expected_oct_mode: int) -> None:
    """
    Assert that `path` has permissions `expected_oct_mode` (e.g. 0o644 or 0o755).

    Only the permission bits are compared; file type bits are ignored.
    """
    mode = path.stat().st_mode & 0o777
    assert mode == expected_oct_mode, (
        f"{path} has permissions {oct(mode)}, expected {oct(expected_oct_mode)}."
    )

# ---------------------------------------------------------------------------
# Directory & file paths
# ---------------------------------------------------------------------------

SERVICE_A_DIR = HOME / "serviceA" / "logs"
SERVICE_B_DIR = HOME / "serviceB" / "logs"
SERVICE_A_LOG = SERVICE_A_DIR / "serviceA.log"
SERVICE_B_LOG = SERVICE_B_DIR / "serviceB.log"

DEBUG_DIR = HOME / "debug"
SUMMARY_CSV = DEBUG_DIR / "correlation_summary.csv"

# ---------------------------------------------------------------------------
# Expected file contents (including final newline)
# ---------------------------------------------------------------------------

SERVICE_A_CONTENT = (
    "2024-04-10T10:00:00Z INFO correlation_id=abc123 Start request\n"
    "2024-04-10T10:00:01Z INFO correlation_id=abc123 End request\n"
    "2024-04-10T10:00:02Z INFO correlation_id=def456 Start request\n"
    "2024-04-10T10:00:03Z INFO correlation_id=ghi789 Start request\n"
    "2024-04-10T10:00:04Z INFO correlation_id=def456 End request\n"
)
SERVICE_B_CONTENT = (
    "2024-04-10T10:00:00Z INFO correlation_id=abc123 Processing request\n"
    "2024-04-10T10:00:01Z INFO correlation_id=abc123 Done\n"
    "2024-04-10T10:00:04Z INFO correlation_id=def456 Processing request\n"
    "2024-04-10T10:00:05Z INFO correlation_id=def456 Done\n"
    "2024-04-10T10:00:06Z INFO correlation_id=zzz999 Unknown request\n"
)

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_service_directories_exist_with_correct_permissions():
    for directory in (SERVICE_A_DIR, SERVICE_B_DIR):
        assert directory.is_dir(), f"Missing required directory: {directory}"
        _assert_file_mode(directory, 0o755)


@pytest.mark.parametrize(
    "log_path, expected_content",
    [
        (SERVICE_A_LOG, SERVICE_A_CONTENT),
        (SERVICE_B_LOG, SERVICE_B_CONTENT),
    ],
)
def test_log_files_exist_with_expected_content_and_permissions(log_path: Path, expected_content: str):
    assert log_path.is_file(), f"Required log file not found: {log_path}"
    _assert_file_mode(log_path, 0o644)

    content = log_path.read_text(encoding="utf-8")
    assert content == expected_content, (
        f"Contents of {log_path} do not match the expected initial log.\n"
        "If you have already modified the log files, restore them to the original "
        "state before running the solution."
    )


def test_debug_directory_does_not_exist_yet():
    """
    Before the student runs their solution, /home/user/debug/ should *not* exist.
    It must be created by the student's script.
    """
    assert not DEBUG_DIR.exists(), (
        f"The directory {DEBUG_DIR} already exists. "
        "The student script should create this directory; "
        "it must not be present beforehand."
    )


def test_summary_csv_does_not_exist_yet():
    """
    The correlation_summary.csv file must not exist before the student's work.
    """
    assert not SUMMARY_CSV.exists(), (
        f"The summary CSV {SUMMARY_CSV} is present before execution. "
        "The student solution should create this file."
    )