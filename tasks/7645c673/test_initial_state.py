# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating system /
# filesystem before the student starts solving the task.  If any of these
# tests fail, the exercise environment is corrupt or has been modified
# unexpectedly.
#
# Requirements verified here:
#   • /home/user/logs/ exists and contains exactly the expected log files
#   • Each log file’s contents match the specification *byte-for-byte*
#   • No unexpected extra files are present in /home/user/logs/
#   • No /home/user/output/ directory (or the final CSV) exists yet
#
# Only stdlib + pytest are used.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"
OUTPUT_DIR = HOME / "output"
OUTPUT_CSV = OUTPUT_DIR / "error_ip_summary.csv"

# ---------------------------------------------------------------------------
# Expected files and their exact byte contents (including trailing newlines)
# ---------------------------------------------------------------------------
EXPECTED_FILES = {
    LOG_DIR / "web-2023-09-10.log": (
        b"2023-09-10T10:15:21Z INFO  Request OK            client_ip=192.168.0.10\n"
        b"2023-09-10T10:17:50Z ERROR Failed login          client_ip=192.168.0.10\n"
        b"2023-09-10T11:05:52Z ERROR Timeout               client_ip=10.0.0.5\n"
        b"2023-09-10T12:45:03Z ERROR Session aborted       client_ip=192.168.0.10\n"
    ),
    LOG_DIR / "web-2023-09-11.log": (
        b"2023-09-11T09:25:42Z ERROR Database err          client_ip=192.168.0.10\n"
        b"2023-09-11T10:00:01Z INFO  Request OK            client_ip=192.168.0.20\n"
    ),
    LOG_DIR / "web-2023-09-12.log": (
        b"2023-09-12T08:14:22Z ERROR Service overload      client_ip=10.0.0.5\n"
        b"2023-09-12T09:00:42Z ERROR Upsstream reset        client_ip=172.16.1.9\n"
    ),
    LOG_DIR / "web-2023-09-13.log": (
        b"2023-09-13T07:55:11Z INFO  Healthcheck OK        client_ip=127.0.0.1\n"
    ),
}

# Handy constant for clearer test messages
EXPECTED_PATHS = list(EXPECTED_FILES.keys())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_logs_directory_exists():
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_no_output_directory_yet():
    assert not OUTPUT_DIR.exists(), (
        f"{OUTPUT_DIR} should NOT exist before the student runs the solution."
    )
    # If someone pre-created the CSV file, also complain explicitly.
    assert not OUTPUT_CSV.exists(), (
        f"{OUTPUT_CSV} already exists; the student must generate it."
    )


def test_expected_log_file_set():
    """Ensure *exactly* the expected log files are present and no others."""
    present_files = sorted(p for p in LOG_DIR.iterdir() if p.is_file())
    expected_files_sorted = sorted(EXPECTED_PATHS)

    # Human-readable assertion message:
    assert present_files == expected_files_sorted, (
        "The contents of /home/user/logs/ do not match the specification.\n"
        f"Expected files:\n  " + "\n  ".join(map(str, expected_files_sorted)) + "\n"
        f"Found files:\n  " + "\n  ".join(map(str, present_files)) + "\n"
    )


@pytest.mark.parametrize("path, expected_bytes", EXPECTED_FILES.items())
def test_each_log_file_content(path: Path, expected_bytes: bytes):
    assert path.exists(), f"Expected file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."

    actual_bytes = path.read_bytes()
    assert (
        actual_bytes == expected_bytes
    ), (
        f"File {path} does not match the expected contents.\n"
        "If the difference is only line endings, verify that each line ends "
        "with a single newline (\\n) and that the final line also ends with one."
    )


def test_permissions_are_reasonable():
    """Quick sanity check on permissions (not strict, just must be readable)."""
    for path in EXPECTED_PATHS:
        mode = path.stat().st_mode & 0o777
        assert mode & 0o444, f"File {path} is not readable (mode {oct(mode)})"