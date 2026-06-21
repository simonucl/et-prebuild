# test_initial_state.py
#
# This test-suite validates the operating-system / filesystem *before* the
# student’s automation commands are executed.  It asserts that the initial
# set-up exactly matches the specification given in the task description.

import os
import stat
import pytest

BASE_DIR = "/home/user/automation_logs"
REPORT_FILE = os.path.join(BASE_DIR, "system_report.txt")

# Paths that must *not* exist yet
OUTPUT_FILES = [
    os.path.join(BASE_DIR, "errors_only.txt"),
    os.path.join(BASE_DIR, "cleaned_report.txt"),
    os.path.join(BASE_DIR, "severity_summary.csv"),
    os.path.join(BASE_DIR, "process.log"),
]

EXPECTED_LINES = [
    "2023-09-14 10:00:01 [INFO] System boot",
    "2023-09-14 10:01:15 [WARN] Disk space low",
    "2023-09-14 10:05:42 [ERROR] Failed to start service A",
    "2023-09-14 10:10:30 [INFO] Service B started",
    "2023-09-14 10:15:00 [WARN] High memory usage",
    "2023-09-14 10:20:20 [ERROR] Unhandled exception",
    "2023-09-14 10:25:55 [INFO] Health check passed",
]


def _mode_bits(path):
    """Return permission bits of a file or directory (`stat.S_IMODE`)."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_directory_exists_and_is_accessible():
    assert os.path.isdir(BASE_DIR), (
        f"Required directory {BASE_DIR!r} does not exist or is not a directory."
    )

    mode = _mode_bits(BASE_DIR)
    # Expect at least 0o755 (rwxr-xr-x): world-readable & executable.
    assert mode & 0o555 == 0o555, (
        f"{BASE_DIR!r} permissions too restrictive: "
        f"expected world-readable & executable (>= 755), got {oct(mode)}."
    )


def test_directory_contains_exactly_system_report():
    contents = sorted(os.listdir(BASE_DIR))
    assert contents == ["system_report.txt"], (
        f"{BASE_DIR!r} must contain exactly one file 'system_report.txt'. "
        f"Found: {contents}"
    )


def test_system_report_file_exists_and_permissions():
    assert os.path.isfile(REPORT_FILE), f"Missing {REPORT_FILE!r}."
    mode = _mode_bits(REPORT_FILE)
    # Expect at least 0o644 (rw-r--r--): world-readable.
    assert mode & 0o444 == 0o444, (
        f"{REPORT_FILE!r} is not world-readable. Current mode: {oct(mode)}"
    )


def test_system_report_content_exact():
    with open(REPORT_FILE, "r", encoding="utf-8") as fp:
        lines = [ln.rstrip("\n") for ln in fp.readlines()]

    assert lines == EXPECTED_LINES, (
        f"Content of {REPORT_FILE!r} does not match specification.\n"
        f"Expected ({len(EXPECTED_LINES)} lines):\n{EXPECTED_LINES}\n\n"
        f"Got ({len(lines)} lines):\n{lines}"
    )


@pytest.mark.parametrize("path", OUTPUT_FILES)
def test_no_output_files_yet(path):
    assert not os.path.exists(path), (
        f"Output file {path!r} should NOT exist before the automation runs."
    )